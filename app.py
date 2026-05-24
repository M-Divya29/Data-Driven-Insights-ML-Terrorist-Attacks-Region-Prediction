from flask import Flask, render_template, request, jsonify
import sqlite3
import joblib
import numpy as np
import os
import requests
import bcrypt
import logging
from RouteMap import GetMap
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------
# BASIC CONFIG
# ---------------------
app = Flask(__name__)

# ---------------------
# MODEL CONFIG (Dropbox Hosting)
# ---------------------
model_path = "model/last.pkl"
os.makedirs("model", exist_ok=True)

# Load Dropbox URL from environment variable (NEVER hardcode URLs with tokens!)
dropbox_url = os.environ.get("DROPBOX_MODEL_URL")
if not dropbox_url:
    logger.warning("DROPBOX_MODEL_URL not set in environment. Model download will fail.")
    dropbox_url = None

if not os.path.exists(model_path):
    if not dropbox_url:
        logger.error("DROPBOX_MODEL_URL not set. Cannot download model.")
        raise Exception("DROPBOX_MODEL_URL environment variable must be set.")
    
    logger.info("Downloading model from Dropbox...")
    try:
        response = requests.get(dropbox_url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(model_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        if os.path.getsize(model_path) < 1000000:
            os.remove(model_path)
            raise Exception("Downloaded file is too small. Possible corruption.")
        
        logger.info("Model download complete.")
    except Exception as e:
        logger.error(f"Failed to download model: {e}")
        raise

# Load model safely
try:
    rfc = joblib.load(model_path)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise e

# ---------------------
# DATABASE INITIALIZATION
# ---------------------
def init_db():
    """Initialize database schema on startup"""
    try:
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS user(
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT UNIQUE NOT NULL,
                          password TEXT NOT NULL,
                          mobile TEXT NOT NULL,
                          email TEXT UNIQUE NOT NULL,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )""")
        connection.commit()
        connection.close()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")

init_db()

# ---------------------
# UTILITY FUNCTIONS
# ---------------------
def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_email(email):
    """Basic email validation"""
    return '@' in email and '.' in email.split('@')[1]

def validate_phone(phone):
    """Validate phone number (basic)"""
    return phone.isdigit() and len(phone) >= 10

# ---------------------
# WEATHER API (Optional)
# ---------------------
api_key = os.environ.get("WEATHER_API_KEY")

def get_weather(api_key, location):
    """Fetch weather and coordinates from API"""
    try:
        if not api_key:
            logger.warning("Weather API key not configured")
            return None
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['location']['lat'], data['location']['lon']
    except Exception as e:
        logger.error(f"Weather API error: {e}")
    return None

# ---------------------
# ROUTES
# ---------------------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            password = request.form.get('password', '').strip()
            
            if not name or not password:
                return render_template('index.html', msg='Name and password are required')
            
            connection = sqlite3.connect('user_data.db')
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM user WHERE name=?", (name,))
            result = cursor.fetchone()
            connection.close()
            
            if result and verify_password(password, result[0]):
                return render_template('fetal.html')
            else:
                return render_template('index.html', 
                                     msg='Sorry, Incorrect Credentials Provided, Try Again')
        except Exception as e:
            logger.error(f"Login error: {e}")
            return render_template('index.html', msg='An error occurred during login')
    
    return render_template('index.html')

@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            password = request.form.get('password', '').strip()
            phone = request.form.get('phone', '').strip()
            email = request.form.get('email', '').strip()
            
            # Validation
            if not all([name, password, phone, email]):
                return render_template('index.html', msg='All fields are required')
            
            if len(password) < 6:
                return render_template('index.html', msg='Password must be at least 6 characters')
            
            if not validate_email(email):
                return render_template('index.html', msg='Invalid email format')
            
            if not validate_phone(phone):
                return render_template('index.html', msg='Invalid phone number')
            
            if len(name) < 3:
                return render_template('index.html', msg='Name must be at least 3 characters')
            
            # Hash password
            hashed_password = hash_password(password)
            
            connection = sqlite3.connect('user_data.db')
            cursor = connection.cursor()
            
            try:
                cursor.execute("INSERT INTO user (name, password, mobile, email) VALUES (?, ?, ?, ?)",
                             (name, hashed_password, phone, email))
                connection.commit()
                logger.info(f"User registered: {name}")
                return render_template('index.html', msg='Successfully Registered! Please Login.')
            except sqlite3.IntegrityError:
                return render_template('index.html', msg='Username or Email already exists')
            finally:
                connection.close()
        
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return render_template('index.html', msg='An error occurred during registration')
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html', msg='Successfully Logged Out')

@app.route('/fetalPage', methods=['GET', 'POST'])
def fetalPage():
    return render_template('fetal.html')

@app.route('/predict', methods=['POST', 'GET'])
def predictPage():
    if request.method == 'POST':
        try:
            # Input validation and conversion
            year = int(request.form.get('year', 0))
            month = int(request.form.get('month', 0))
            date = int(request.form.get('date', 0))
            
            location = request.form.get('location', '').strip()
            tolocation = request.form.get('tolocation', '').strip()
            
            if not location or not tolocation:
                return render_template('predict.html', 
                                     status='Location data is required')
            
            coord = location.split(',')
            tocoord = tolocation.split(',')
            
            if len(coord) != 2 or len(tocoord) != 2:
                return render_template('predict.html',
                                     status='Invalid coordinate format')
            
            lat = float(coord[0])
            lon = float(coord[1])
            
            # Validate ranges
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                return render_template('predict.html',
                                     status='Invalid coordinates')
            
            if not (1 <= month <= 12 and 1 <= date <= 31):
                return render_template('predict.html',
                                     status='Invalid date')
            
            multiple = int(request.form.get('multiple', 0))
            attack = int(request.form.get('attack', 0))
            target = int(request.form.get('target', 0))
            ind = int(request.form.get('ind', 0))
            casualties = int(request.form.get('casualties', 0))
            weapon = int(request.form.get('weapon', 0))
            
            # Generate map
            map_var = GetMap(coord, tocoord)
            
            # Prepare prediction data
            data = np.array([[
                year,
                month,
                date,
                lat,
                lon,
                multiple,
                attack,
                target,
                ind,
                weapon,
                casualties
            ]])
            
            prediction = rfc.predict(data)[0]
            
            if prediction == 1:
                result_text = "The attack based on these features would be successful."
            else:
                result_text = "The attack based on these features would NOT be successful."
            
            logger.info(f"Prediction made: {result_text}")
            
        except ValueError as e:
            logger.error(f"Value conversion error: {e}")
            result_text = "Invalid input data. Please check your entries."
            map_var = None
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            result_text = "The attack based on these features is non-predictable."
            map_var = None
        
        return render_template('predict.html',
                             status=result_text,
                             map_var=map_var)
    
    return render_template('predict.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {error}")
    return render_template('index.html', msg='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    return render_template('index.html', msg='Internal server error'), 500

# ---------------------
# ENTRY POINT
# ---------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

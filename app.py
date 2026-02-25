from flask import Flask, render_template, request
import sqlite3
import joblib
import numpy as np
import os
import requests
from RouteMap import GetMap

# -----------------------------
# BASIC CONFIG
# -----------------------------
app = Flask(__name__)
dsatm = [12.825251, 77.514417]

# -----------------------------
# MODEL CONFIG (Dropbox Hosting)
# -----------------------------
model_path = "model/last.pkl"
os.makedirs("model", exist_ok=True)

dropbox_url = "https://dl.dropboxusercontent.com/scl/fi/i48njjh7la8i7dvygv5j2/last.pkl?rlkey=pw8hrowbugyzlmc7s84wp4j4w"

if not os.path.exists(model_path):
    print("Downloading model from Dropbox...")

    response = requests.get(dropbox_url, stream=True)

    if response.status_code != 200:
        raise Exception("Failed to download model from Dropbox.")

    with open(model_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    # Validate file size to avoid corrupted HTML downloads
    if os.path.getsize(model_path) < 1000000:
        raise Exception("Downloaded file is too small. Possible corruption.")

    print("Model download complete.")

# Load model safely
try:
    rfc = joblib.load(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print("Error loading model:", e)
    raise e

# -----------------------------
# WEATHER API (Optional)
# -----------------------------
api_key = os.environ.get("WEATHER_API_KEY")

def get_weather(api_key, location):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['location']['lat'], data['location']['lon']
    return None


# -----------------------------
# ROUTES
# -----------------------------
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        cursor.execute("SELECT name, password FROM user WHERE name=? AND password=?",
                       (name, password))
        result = cursor.fetchall()
        connection.close()

        if result:
            return render_template('fetal.html')
        else:
            return render_template('index.html',
                                   msg='Sorry, Incorrect Credentials Provided, Try Again')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']

        cursor.execute("""CREATE TABLE IF NOT EXISTS user(
                          name TEXT, password TEXT, mobile TEXT, email TEXT)""")

        cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?)",
                       (name, password, mobile, email))

        connection.commit()
        connection.close()

        return render_template('index.html', msg='Successfully Registered')

    return render_template('index.html')


@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route('/fetalPage', methods=['GET', 'POST'])
def fetalPage():
    return render_template('fetal.html')


@app.route('/predict', methods=['POST', 'GET'])
def predictPage():
    if request.method == 'POST':
        try:
            year = int(request.form['year'])
            month = int(request.form['month'])
            date = int(request.form['date'])

            location = request.form['location']
            tolocation = request.form['tolocation']

            coord = location.split(',')
            tocoord = tolocation.split(',')

            lat = float(coord[0])
            lon = float(coord[1])

            multiple = int(request.form['multiple'])
            attack = int(request.form['attack'])
            target = int(request.form['target'])
            ind = int(request.form['ind'])
            casualties = int(request.form['casualties'])
            weapon = int(request.form['weapon'])

            map_var = GetMap(coord, tocoord)

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

        except Exception:
            result_text = "The attack based on these features is non predictable."
            map_var = None

        return render_template('predict.html',
                               status=result_text,
                               map_var=map_var)

    return render_template('predict.html')


# -----------------------------
# RENDER COMPATIBLE ENTRY POINT
# -----------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
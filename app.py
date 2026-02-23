from flask import Flask, render_template, request
import sqlite3
import joblib
import numpy as np
import os
import requests
from RouteMap import GetMap

dsatm = [12.825251, 77.514417]

app = Flask(__name__)

# Path to store the model
model_path = "model/last.pkl"
os.makedirs("model", exist_ok=True)

# Google Drive direct download link
gdrive_url = "https://drive.google.com/uc?export=download&id=1QceHdIh6PGpQdNZBSP6bwMDuvqOhOiON"

# Download the model if it doesn't exist
if not os.path.exists(model_path):
    print("Model not found. Downloading from Google Drive...")
    r = requests.get(gdrive_url)
    if r.status_code == 200:
        with open(model_path, "wb") as f:
            f.write(r.content)
        print("Model downloaded successfully.")
    else:
        raise Exception(f"Failed to download model. Status code: {r.status_code}")

# Load the trained model
rfc = joblib.load(model_path)

api_key = os.environ.get("WEATHER_API_KEY")

def get_weather(api_key, location):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['location']['lat'], data['location']['lon']
    else:
        return None

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
        cursor.execute("SELECT name, password FROM user WHERE name = ? AND password = ?", (name, password))
        result = cursor.fetchall()
        connection.close()
        if result:
            return render_template('fetal.html')
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided, Try Again')
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
        cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (name, password, mobile, email))
        connection.commit()
        connection.close()
        return render_template('index.html', msg='Successfully Registered')
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route("/fetalPage", methods=['GET', 'POST'])
def fetalPage():
    return render_template('fetal.html')

@app.route("/predict", methods=['POST', 'GET'])
def predictPage():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        date = request.form['date']
        location = request.form['location']
        tolocation = request.form['tolocation']

        coord = location.split(',')
        tocoord = tolocation.split(',')
        lat, long = coord[0], coord[1]

        multiple = request.form['multiple']
        attack = request.form['attack']
        target = request.form['target']
        ind = request.form['ind']
        casualties = request.form['casualties']
        weapon = request.form['weapon']

        map_var = GetMap(coord, tocoord)

        try:
            data = np.array([[ 
                int(year),
                int(month),
                int(date),
                float(lat),
                float(long),
                int(multiple),
                int(attack),
                int(target),
                int(ind),
                int(weapon),
                int(casualties)
            ]])
            my_prediction = rfc.predict(data)
            result = my_prediction[0]
            if result == 1:
                res = "The attack based on these features would be successful."
            elif result == 0:
                res = "The attack based on these features would NOT be successful."
        except:
            res = "The attack based on these features is non predictable."

        return render_template('predict.html', status=res, map_var=map_var)

    return render_template('predict.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
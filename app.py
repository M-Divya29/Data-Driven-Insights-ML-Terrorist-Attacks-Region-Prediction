from flask import Flask, render_template, request, flash, redirect
import sqlite3
import pickle
import numpy as np
import os
import requests
from RouteMap import GetMap
dsatm=[12.825251, 77.514417]


app = Flask(__name__)

import joblib

# Load the trained model from the file
model_path = os.path.join(os.path.dirname(__file__), 'model', 'last.pkl')
rfc = joblib.load(model_path)
    
api_key = os.environ.get("WEATHER_API_KEY")

def get_weather(api_key, location):
    print("ENTERED API")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
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

        query = "SELECT name, password FROM user WHERE name = ? AND password = ?"
        cursor.execute(query, (name, password))

        result = cursor.fetchall()

        if result:
            return render_template('fetal.html') 
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

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
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute(
    "INSERT INTO user VALUES (?, ?, ?, ?)",
    (name, password, mobile, email)
)
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route("/fetalPage", methods=['GET', 'POST'])
def fetalPage():
    return render_template('fetal.html') 




@app.route("/predict", methods = ['POST', 'GET'])
def predictPage():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        date = request.form['date']
        location = request.form['location']
        tolocation = request.form['tolocation']
        coord=location.split(',')
        tocoord=tolocation.split(',')
        lat,long=coord[0],coord[1]
        

        

        multiple = request.form['multiple']
        attack = request.form['attack']
        target = request.form['target']
        ind = request.form['ind']
        casualties = request.form['casualties']
        weapon = request.form['weapon']
        map_var = GetMap(coord,tocoord)

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
            
            if result ==1:
                res="The attack based on these features would be successful."
            elif result ==0:
                res="The attack based on these features would NOT be successful."
        except:
            res="The attack based on these features is non predictable."
           
        return render_template('predict.html',status=res,map_var=map_var)

    return render_template('predict.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
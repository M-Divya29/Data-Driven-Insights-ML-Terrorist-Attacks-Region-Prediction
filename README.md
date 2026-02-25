# 🌍 Data-Driven Insights: ML-Based Terrorist Attack Region Prediction

## 📌 Project Overview

This project presents a Machine Learning–powered web application that predicts the likelihood of a terrorist attack being successful based on historical and contextual input features.

The system integrates:

- Supervised Machine Learning (Random Forest Classifier)
- Flask Web Framework
- SQLite Database (User Authentication)
- Interactive Map Visualization (Folium)
- Cloud Deployment using Render

The application provides an intuitive interface for users to input event-related parameters and receive predictive insights.

---

## 🚀 Live Application

🔗 **Live Demo:**  
https://data-driven-insights-ml-terrorist-omqn.onrender.com

---

## 🧠 Machine Learning Model

- Algorithm Used: **Random Forest Classifier**
- Library: `scikit-learn`
- Model File: `last.pkl`
- Frameworks: NumPy, Joblib

The model predicts whether an attack would likely be successful based on features such as:

- Year, Month, Date
- Latitude & Longitude
- Attack Type
- Target Type
- Weapon Type
- Casualties
- Multiple Attack Indicator
- Industry Indicator

---

## 🏗️ Tech Stack

### 🔹 Backend
- Python 3.10
- Flask
- SQLite
- Joblib
- Requests

### 🔹 Machine Learning
- Scikit-learn
- NumPy
- SciPy

### 🔹 Frontend
- HTML
- CSS
- Jinja2 Templates

### 🔹 Visualization
- Folium (Interactive Maps)

### 🔹 Deployment
- Gunicorn
- Render Cloud Platform

---

## 📂 Project Structure
├── app.py
├── requirements.txt
├── model/
│ └── last.pkl (downloaded automatically)
├── templates/
│ ├── home.html
│ ├── index.html
│ ├── fetal.html
│ └── predict.html
├── RouteMap.py
└── README.md


---

## 📥 Model File Access

Due to GitHub file size limitations, the trained ML model (`last.pkl`) is hosted externally.

You can download it manually from:

🔹 **Google Drive:**  
https://drive.google.com/file/d/1QceHdIh6PGpQdNZBSP6bwMDuvqOhOiON/view?usp=sharing  

🔹 **Dropbox (Direct Download):**  
https://www.dropbox.com/s/i48njjh7la8i7dvygv5j2/last.pkl?dl=1  

⚙️ The application automatically downloads the model during deployment if it is not found locally.

---

## ⚙️ Local Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/M-Divya29/Data-Driven-Insights-ML-Terrorist-Attacks-Region-Prediction.git
cd Data-Driven-Insights-ML-Terrorist-Attacks-Region-Prediction
2️⃣ Create Virtual Environment
python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run Application
python app.py

Open in browser:

http://127.0.0.1:5000
☁️ Deployment (Render)

Build Command:

pip install -r requirements.txt

Start Command:

gunicorn app:app

The service runs on:

0.0.0.0:$PORT
🔐 Features

✔ User Registration & Login
✔ Secure SQLite Database
✔ ML-Based Prediction
✔ Interactive Route Mapping
✔ Cloud Deployment
✔ Automatic Model Download

📊 Future Enhancements

Model retraining with updated dataset

Advanced feature engineering

REST API support

Docker containerization

CI/CD pipeline integration

Role-based authentication

Data visualization dashboard

👩‍💻 Author

M Divya Lalitha
Machine Learning & Web Application Developer

📜 License

This project is for academic and research purposes.
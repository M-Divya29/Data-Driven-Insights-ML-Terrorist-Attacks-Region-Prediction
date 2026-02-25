# 🌍 Data-Driven Insights: ML-Based Terrorist Attack Region Prediction

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.0.2-orange?logo=scikitlearn)
![Deployment](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render)
![Status](https://img.shields.io/badge/Status-Live-success)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

---

## 📌 Project Overview

This project presents a Machine Learning-powered web application that predicts the likelihood of a terrorist attack being successful based on historical and contextual input features.

The system integrates:

- Supervised Machine Learning (Random Forest Classifier)
- Flask Web Framework
- SQLite Database (User Authentication)
- Interactive Map Visualization using Folium
- Cloud Deployment via Render

The application provides an intuitive user interface where users can input event-related parameters and receive predictive insights instantly.

---

## 🚀 Live Application

🔗 Live Demo:  
https://data-driven-insights-ml-terrorist-omqn.onrender.com

---

## 🧠 Machine Learning Model

Algorithm Used: Random Forest Classifier  
Library: Scikit-learn  
Model File: `last.pkl`

### 🔎 Input Features

- Year  
- Month  
- Date  
- Latitude  
- Longitude  
- Multiple Attack Indicator  
- Attack Type  
- Target Type  
- Industry Indicator  
- Weapon Type  
- Casualties Count  

### 🎯 Output

- ✅ Successful  
- ❌ Not Successful  

---

## 🏗️ Technology Stack

### Backend
- Python 3.10
- Flask
- SQLite
- Joblib
- Requests

### Machine Learning
- Scikit-learn
- NumPy
- SciPy

### Frontend
- HTML
- CSS
- Jinja2 Templates

### Visualization
- Folium (Interactive Maps)

### Deployment
- Gunicorn
- Render Cloud Platform

---

## 📂 Project Structure

```
Data-Driven-Insights-ML-Terrorist-Attacks-Region-Prediction/
│
├── app.py
├── RouteMap.py
├── requirements.txt
├── README.md
│
├── model/
│   └── last.pkl
│
├── templates/
│   ├── home.html
│   ├── index.html
│   ├── fetal.html
│   └── predict.html
│
└── user_data.db
```

---

## 📥 Model File Access

Due to GitHub's 100MB file limit, the trained model is hosted externally.

### Google Drive
https://drive.google.com/file/d/1QceHdIh6PGpQdNZBSP6bwMDuvqOhOiON/view?usp=sharing

### Dropbox (Direct Download)
https://www.dropbox.com/scl/fi/i48njjh7la8i7dvygv5j2/last.pkl?rlkey=pw8hrowbugyzlmc7s84wp4j4w&st=0pn9gty4&dl=0

or

https://www.dropbox.com/s/i48njjh7la8i7dvygv5j2/last.pkl?dl=1

The application automatically downloads the model if it does not exist locally.

---

## ⚙️ Local Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/M-Divya29/Data-Driven-Insights-ML-Terrorist-Attacks-Region-Prediction.git
cd Data-Driven-Insights-ML-Terrorist-Attacks-Region-Prediction
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## ☁️ Deployment Configuration (Render)

Build Command:
```
pip install -r requirements.txt
```

Start Command:
```
gunicorn app:app
```

Application runs on:
```
0.0.0.0:$PORT
```

---

## 🔐 Application Features

- User Registration & Login System
- SQLite Database Integration
- ML-Based Prediction Engine
- Interactive Route Mapping
- Automatic Model Download
- Cloud Deployment Ready
- Production Gunicorn Setup

---

## 📊 Future Enhancements

- Model retraining with updated datasets
- REST API development
- Role-based authentication
- Docker containerization
- CI/CD integration
- Advanced analytics dashboard

---

## 👩‍💻 Author

M Divya Lalitha  
Machine Learning & Full Stack Developer  

---

## 📜 License

Developed for academic and research purposes only.
import pandas as pd 
import numpy as np
import dash
import matplotlib.pyplot as plt
from scipy.special import inv_boxcox
import seaborn as sns
import pickle
from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap
from dash_application import create_dash_app
application = Flask(__name__)
Bootstrap(application)

create_dash_app(application)

def load_object(name):
    pickle_obj = open(f"{name}.pck","rb")
    obj = pickle.load(pickle_obj)
    return obj
@application.route('/')
def index():
    return render_template('index.html')

@application.route('/home')
def home():
    return render_template('home.html')

@application.route('/contact')
def contact():
    return render_template('contact.html')

@application.route('/signup')
def signup():
    return render_template('signup.html')

@application.route('/recruitment')
def recruitment():
    return render_template('recruitment.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =="POST":
        user= request.form.get("username")
        password= request.form.get("password")
        if user=='Lhen' and password=='Lhen@123':
            return render_template('home.html')
        return '<h1>Invalid username or password</h1>'
@application.route('/predict',methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        gender= request.form.get("gender")
        highest_educ= request.form.get("education")
        status= request.form.get("status")
        experience= request.form.get("experience")
        year= request.form.get("year")
        age= request.form.get("age")
        resilience= request.form.get("resilience")
        online= request.form.get("online")
        csa= request.form.get("csa")
        Dict = {'gender': gender, 'highest_educ': highest_educ,'status':status,'experience':experience,'year':year,'age':age,'resilience':resilience,'online':online,'csa':csa}
        Dict["gender"] = load_object("Label_Encoder_gender").transform(np.array(Dict["gender"]).reshape(-1,))[0]
        Dict["online"] = load_object("Label_Encoder_online_la").transform(np.array(Dict["online"]).reshape(-1,))[0]
        Dict["experience"] = load_object("Label_Encoder_prio_experience_call_center").transform(np.array(Dict["experience"]).reshape(-1,))[0]
        Dict["highest_educ"] = load_object("OneHotEncoder_educ").transform(highest_educ.reshape(-1, 1)).toarray()[0]
        Dict["status"] = load_object("OneHotEncoder_status").transform(Dict["status"].reshape(-1,1)).toarray()[0]
        Dict["year"] = load_object("OneHotEncoder_year").transform(Dict["year"].reshape(-1,1)).toarray()[0]
        Dict["lob"] = load_object("OneHotEncoder_lob").transform(Dict["lob"].reshape(-1,1)).toarray()[0]
        col_sequence = load_object("columns")
        array = []
        for col_name in col_sequence :
            array.append(Dict[col_name])
        array = np.array(array)
        array1 = load_object("Scaler").transform(array.reshape(1,-1))
        array2 = load_object("PCA").transform(array1)
        prediction = load_object("MyModel").predict(array2)
        AHT= inv_boxcox(prediction , load_object("boxcox_lambda"))
        array3 = load_object("Scaler1").transform(array.reshape(1,-1))
        array4 = load_object("PCA1").transform(array3)
        prediction1 = load_object("MyModel1").predict(array4)
        Accuracy= inv_boxcox(prediction1 , load_object("boxcox_lambda1"))
        AHT=float(np.asarray(AHT))
        AHT=round(AHT,1)
        Accuracy=float(np.asarray(Accuracy))
        return render_template('recruitment.html', AHT="{0}".format(AHT),Accuracy="{:.2%}".format(Accuracy))
if __name__ == "__main__":
    application.run(debug=False)
    

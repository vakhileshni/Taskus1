import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import inv_boxcox
import seaborn as sns
import pickle
from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap
application = Flask(__name__)
Bootstrap(application)

def load_object(name):
    pickle_obj = open(f"{name}.pck","rb")
    obj = pickle.load(pickle_obj)
    return obj
@application.route('/')
def home():
    return render_template('index.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =="POST":
        user= request.form.get("username")
        password= request.form.get("password")
        if user=='Lhen' or password=='Lhen@123':
            return render_template('ml.html')
        return '<h1>Invalid username or password</h1>'
@application.route('/predict',methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        gender= request.form.get("gender")
        highest_educ_bg= request.form.get("highest_educ_bg")
        age= request.form.get("age")
        assessment= request.form.get("assessment")
        week_in_dmr= request.form.get("week_in_dmr")
        weeks_to_graduate= request.form.get("weeks_to_graduate")
        first_month_accuracy_hitting_goal= request.form.get("first_month_accuracy_hitting_goal")
        speed_to_prof= request.form.get("speed_to_prof")
        Dict = {'gender': gender, 'highest_educ_bg': highest_educ_bg,'age':age,'assessment':assessment,'week_in_dmr':week_in_dmr,'weeks_to_graduate':weeks_to_graduate,'first_month_accuracy_hitting_goal':first_month_accuracy_hitting_goal,'speed_to_prof':speed_to_prof}
        Dict["gender"] = load_object("Label_Encoder_gender").transform(np.array(Dict["gender"]).reshape(-1,))[0]
        Dict["highest_educ_bg"] = load_object("Label_Encoder_highest_educ_bg").transform(np.array(Dict["highest_educ_bg"]).reshape(-1,))
        Dict["highest_educ_bg_ohe"] = load_object("OneHotEncoder_educ").transform(Dict["highest_educ_bg"].reshape(-1,1)).toarray()[0]
        del Dict["highest_educ_bg"]
        for e , i in enumerate(Dict["highest_educ_bg_ohe"]):
            Dict["highest_educ_bg" + str(e)] = i
        del Dict["highest_educ_bg_ohe"]
        col_sequence = load_object("columns")
        array = []
        for col_name in col_sequence :
            array.append(Dict[col_name])
        array = np.array(array)
        array1 = load_object("Scaler").transform(array.reshape(1,-1))
        array2 = load_object("PCA").transform(array1)
        prediction = load_object("MyModel").predict(array2)
        output= inv_boxcox(prediction , load_object("boxcox_lambda"))
        array3 = load_object("Scaler1").transform(array.reshape(1,-1))
        array4 = load_object("PCA1").transform(array3)
        prediction1 = load_object("MyModel1").predict(array4)
        output1= inv_boxcox(prediction1 , load_object("boxcox_lambda1"))
        return render_template('home.html', prediction_text='Employee AHT should be {0} and Accuarcy {1}'.format(output,output1))
if __name__ == "__main__":
    application.run(host='0.0.0.0',port=80)

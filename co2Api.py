from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import *


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='', server='localhost', database='co2_tracker')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app=app
db.init_app(app)



@app.route('/register',methods=['GET','POST'])
def RegisterUser():
    username = request.get_json()['UserName']
    password = request.get_json()['Password']
    phone = request.get_json()['Phone']
    email = request.get_json()['Email']
    location = request.get_json()['Location']
    try:
        userObject = users(uname=username,email=email,phone=phone,password=password,location=location)
        db.session.add(userObject)
        db.session.commit()
        return jsonify({"result":{"message":"successfully registered","status":1}})   
    except Exception as e:
        print("something went wrong error message is ",e)
        return jsonify({"result":"failed to register","status":0})

@app.route('/login', methods=['GET', 'POST'])
def LoginUser():
    username = request.get_json()['UserName']
    password = request.get_json()['Password']
    print(username)
    print(password)
    try:
        result=db.session.query(users).filter_by(uname=username,password=password)
        if result!= None:
           return jsonify({"result":{"message":"successfully logged in","status":1,"token":"324frwf43ghi"}})   
        else:
           return jsonify({"result":{"message":"invalid username or password ","status":0,"token":""}})
    except Exception as e:
        print("something went wrong error message is ",e)
        return jsonify({"result":"failed to register","status":0})


@app.route('/saveSensorValues', methods=['GET', 'POST'])
def saveSensorValues():
    tempValue = request.get_json()['TempValue']
    co2Value = request.get_json()['Co2Value']
    location = request.get_json()['Location']
    timeStamp = request.get_json()['TimeStamp']

    try:
        sensorValuesObject = sensor_values(temp_values=tempValue,co2_values=co2Value,location=location,time_stamp=timeStamp)
        db.session.add(sensorValuesObject)
        db.session.commit()
        return jsonify({"result":{"message":"successfully saved sensor values","status":1}})   
    except Exception as e:
        print("something went wrong error message is ",e)
        return jsonify({"result":"failed to save sensor values","status":0})


@app.route('/getSensorValues',methods=['POST'])
def getSesnorValues():
   location = request.get_json()['Location']
   try:
       result=db.session.query(sensor_values).filter_by(location=location).order_by(sensor_values.id.desc()).first()
       
       co2_value = result.co2_values
       temp_value = result.temp_values
       return jsonify({"result":"successfully fetched sensor values","status":1,"co2Value":co2_value,"tempValue":temp_value})

   except Exception as e:
       print("failed to fetch values :",e)
       return jsonify({"result":"failed to get sensor values","status":0,"co2Value":0,"tempValue":0})

    
if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')
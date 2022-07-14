from flask import Flask, json,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy import func
from datetime import datetime
from config import *
import smtplib



app = Flask('__name__')

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='', server='localhost', database='co2_tracker')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)


class users(db.Model):
    uname = db.Column(db.String(20))
    email = db.Column(db.String(30),primary_key=True)
    phone = db.Column(db.String(10))
    password = db.Column(db.String(80))
    location = db.Column(db.String(80))

class sensor_values(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    temp_values = db.Column(db.Integer)
    co2_values = db.Column(db.Integer)
    location = db.Column(db.String(80))
    time_stamp = db.Column(db.DateTime)


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
        return jsonify({"result":{"message":"failed to register","status":0}})

@app.route('/login', methods=['GET', 'POST'])
def LoginUser():
    username = request.get_json()['UserName']
    password = request.get_json()['Password']
    print(username)
    print(password)
    try:
        result=db.session.query(users).filter_by(uname=username,password=password).first()
        
        if result!= None:
           return jsonify({"result":{"message":"successfully logged in","status":1,"token":"324frwf43ghi"}})   
        else:
           return jsonify({"result":{"message":"invalid username or password ","status":0,"token":""}})
    except Exception as e:
        print("something went wrong error message is ",e)
        return jsonify({"result":"failed to register","status":0})


@app.route('/saveSensorValues', methods=['GET'])
def saveSensorValues():
    tempValue = float(request.args.get('TempValue'))
    co2Value = float(request.args.get('Co2Value'))
    location = request.args.get('Location')
    timeStamp = datetime.now()

    if (co2Value > MAX_CO2_Value):
        print('sending email....')
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login(LOGIN_EMAIL, LOGIN_EMAIL_PASSWORD)
        # message to be sent
        message = "Alert co2 value is high."
  
        # sending the mail
        s.sendmail(FROM_EMAIL, TO_EMAIL, message)
        # terminating the session
        s.quit()
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
       return jsonify({"result":{"message":"successfully fetched sensor values","status":1,"co2Value":co2_value,"tempValue":temp_value}})

   except Exception as e:
       print("failed to fetch values :",e)
       return jsonify({"result":"failed to get sensor values","status":0,"co2Value":0,"tempValue":0})


@app.route('/dashboard', methods=['POST'])
def Dashboard():
    date = request.get_json()['Date']
    location = request.get_json()['Location']
    response = {}
    x_values = []
    y_values = []
    result ={}
    try:
        sensor_data = db.session.query(sensor_values).filter(func.DATE(sensor_values.time_stamp) == date , sensor_values.location == location).order_by(sensor_values.id.asc())
        for data in sensor_data:
            y_value =  data.co2_values
            x_value =  str(data.time_stamp.time())
            x_values.append(x_value)
            y_values.append(y_value)
        overall_minvalue=db.session.query(sensor_values).filter_by(location=location).order_by(sensor_values.co2_values.asc()).first()
        overall_maxvalue=db.session.query(sensor_values).filter_by(location=location).order_by(sensor_values.co2_values.desc()).first()
        overall_extremes ={ 
            'mindate': overall_minvalue.time_stamp,
            'minvalue': overall_minvalue.co2_values,
            'maxdate': overall_maxvalue.time_stamp ,
            'maxvalue' : overall_maxvalue.co2_values
        }

        today_minvalue=db.session.query(sensor_values).filter(func.DATE(sensor_values.time_stamp) == date , sensor_values.location == location).order_by(sensor_values.co2_values.asc()).first()
        today_maxvalue=db.session.query(sensor_values).filter(func.DATE(sensor_values.time_stamp) == date , sensor_values.location == location).order_by(sensor_values.co2_values.desc()).first()
        
        today_extremes ={ 
            'mindate': today_minvalue.time_stamp,
            'minvalue': today_minvalue.co2_values,
            'maxdate': today_maxvalue.time_stamp ,
            'maxvalue' : today_maxvalue.co2_values
        }
        response['x_values'] =  x_values 
        response['y_values'] = y_values 
        response['today_extremes'] = today_extremes
        response['overall_extremes'] = overall_extremes
        result['status'] = 1
        result['data'] = response
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({"result":{"status":0,"data":{}}})    
   


if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')

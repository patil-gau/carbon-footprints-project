from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class users(db.Model):
    uname = db.Column(db.String)
    email = db.Column(db.String,primary_key=True)
    phone = db.Column(db.String)
    password = db.Column(db.String)
    location = db.Column(db.String)

class sensor_values(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    temp_values = db.Column(db.Integer)
    co2_values = db.Column(db.Integer)
    location = db.Column(db.String)
    time_stamp = db.Column(db.String)
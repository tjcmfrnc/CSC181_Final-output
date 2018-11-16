from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy  import SQLAlchemy
from flask import Flask, render_template, redirect, url_for
import sqlalchemy
from flask_bootstrap import Bootstrap
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/testdb3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)



def createDB():
    engine = sqlalchemy.create_engine('mysql://root:password@localhost')# connects to server
    engine.execute("CREATE DATABASE IF NOT EXISTS testdb") #create db
    engine.execute("USE testdb3") # select new

def createTables():
    db.create_all()
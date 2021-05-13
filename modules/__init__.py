from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import logging
import json
import socket

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
logging.basicConfig(filename='record.log', level=logging.DEBUG)
logging.basicConfig(filename='fatal.log', level=logging.FATAL)
with open('modules/config.json') as configFile:
    config_data = json.load(configFile)
app = Flask(__name__)
app.secret_key = "5791628bb0b13ce0c676dfde280ba245"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SERVER_NAME'] = get_ip_address()+':5000'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = 'modules/downloadReports'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config.update(config_data)

from modules import routes
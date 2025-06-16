from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '3f66e1ab593dce6105b2f7e86db63831'
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///site.db"
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
from flaskblog import route
from flaskblog.database import userdata,posts
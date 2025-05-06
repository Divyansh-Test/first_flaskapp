from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '3f66e1ab593dce6105b2f7e86db63831'
from flaskblog import route
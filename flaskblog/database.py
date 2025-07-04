from flaskblog import db
from datetime import datetime


class userdata (db.Model):

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    dob=db.Column(db.DateTime,nullable=True)
    posts=db.relationship('posts',backref='author',lazy=True)
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('userdata.id'),nullable=False)



class admin(db.Model):
  admin_id=db.Column(db.Integer,primary_key=True)
  username=db.Column(db.String(20),unique=True,nullable=False)
  email=db.Column(db.String(120),unique=True,nullable=False)
  password=db.Column(db.String(60),nullable=False)

  
  
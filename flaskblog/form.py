from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, PasswordField, BooleanField 
from wtforms.validators import DataRequired, Length, Email,EqualTo
class register(FlaskForm):
	username=StringField("username",
	validators=[DataRequired(),Length(min=2,max=20)])
	email=StringField("email",validators=[DataRequired(),Email()])
	password=PasswordField("password",validators=[DataRequired()])
	confirm_password=PasswordField("confirm_password",validators=[DataRequired(),EqualTo('password')])
	cache=BooleanField("remember me")
	submit=SubmitField("Sign-up")
class login(FlaskForm):
	email=StringField("email",validators=[DataRequired(),Email()])
	password=PasswordField("password",validators=[DataRequired()])
	cache=BooleanField("remember me")
	submit=SubmitField("login")
	


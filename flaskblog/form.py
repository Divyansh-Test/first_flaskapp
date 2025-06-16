from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo,Optional
from datetime import date


class Register(FlaskForm):
	username = StringField("username",
	                       validators=[DataRequired(),
	                                   Length(min=2, max=20)])
	email = StringField("email", validators=[DataRequired(), Email()])
	password = PasswordField("password", validators=[DataRequired()])
	confirm_password = PasswordField(
	    "confirm password", validators=[DataRequired(),
	                                    EqualTo('password')])
	cache = BooleanField("remember me")
	submit = SubmitField("Sign-up")


class Login(FlaskForm):
	email = StringField("email", validators=[DataRequired(), Email()])
	password = PasswordField("password", validators=[DataRequired()])
	cache = BooleanField("remember me")
	submit = SubmitField("login")


class Update(FlaskForm):
	
	
	username = StringField("UserName:",
	                       validators=[Optional(),
	                                   Length(min=2, max=20)])

	
	email = StringField("email", validators=[Optional(),Email()])

	
	Dob = DateField("Date of Birth",validators=[Optional()],render_kw={"placeholder": "2022-00-97"},	                
	                format='%Y-%m-%d')
	
	submit = SubmitField("Update")
	cancel = SubmitField("Cancel")

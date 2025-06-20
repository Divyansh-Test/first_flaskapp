from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField,RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo,Optional, ValidationError
from flaskblog.database import userdata


class Register(FlaskForm):
	username = StringField("UserName",
	                       validators=[DataRequired(),
	                                   Length(min=2, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField(
	    "Confirm Password", validators=[DataRequired(),
	                                    EqualTo('password')])
	cache = BooleanField("remember me")
	submit = SubmitField("Sign-up")
	post_user = RadioField("post_user", choices=[('user', 'user'),('admin', 'admin')],default="user")
	def validate_username(self, username):
		user = userdata.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one.')
	def validate_email(self, email):
		user = userdata.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one.')


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

class otp_form(FlaskForm):
	Otp=StringField("otp",validators=[DataRequired()])
	submit=SubmitField("Check otp")
			

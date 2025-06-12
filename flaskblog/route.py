from flask import render_template, url_for, redirect, flash, request,session
from flaskblog.form import Register,Login
from functools import wraps
from flaskblog import app,db,bcrypt
from flaskblog.database import userdata,posts

def check_login(func):
	@wraps(func)
	def check(*args,**kwarg):
		if "username" in session:
			return func(*args,**kwarg)
		else:
			return redirect(url_for("login"))
	return check


@app.route("/")
@app.route("/home")
@check_login
def home():
	return render_template("home.html")

@app.route("/about")
@check_login
def about():
    return "This is about page"
    #return render_template("about.html", title="About")

@app.route("/register", methods=['GET', 'POST'])

def register():
    db.create_all()
    form = Register()
    name = form.username.data
    if form.validate_on_submit():
        flash(f'Account created for {name}!', 'success')
        
        user=userdata(username=form.username.data,email=form.email.data,password=bcrypt.generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            print("Form did not validate:")
            print(form.errors)
            flash(f'Error in creating account for {name}!', 'danger')
    
    
    
    return render_template('register.html', form=form, title="Register")

@app.route("/help")
def help():
    return render_template("help.html", title="Help")

@app.route("/login",methods=["GET","POST"])
def login():
    form=Login()
    if form.validate_on_submit():
        try:
            if form.email.data == userdata.query.filter_by(email=form.email.data).first().email and bcrypt.check_password_hash(userdata.query.filter_by(email=form.email.data).first().password,form.password.data):
                session["username"]=form.email.data
                flash(f'Login successful for {userdata.query.filter_by(email=form.email.data).first().username}!', 'success')
                return redirect(url_for("home"))
            else:
                
                
                flash(f'Login unsuccessful for {form.email.data}!', 'danger')
        except:
               flash(f'Login unsuccessful for {form.email.data}!', 'danger')
         
            
     
    return render_template("login.html",form=form,title="login")
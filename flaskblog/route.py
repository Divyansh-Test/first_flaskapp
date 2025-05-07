from flask import render_template, url_for, redirect, flash, request,session
from flaskblog.form import Register,Login
from functools import wraps
from flaskblog import app
che={}
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
    form = Register()
    name = form.username.data
    if form.validate_on_submit():
        flash(f'Account created for {name}!', 'success')
        print(f'{name} successfully created')
        che[form.email.data]=[form.password.data,name]
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            print("Form did not validate:")
            print(form.errors)
    return render_template('register.html', form=form, title="Register")

@app.route("/help")
def help():
    return render_template("help.html", title="Help")

@app.route("/login",methods=["GET","POST"])
def login():
    form=Login()
    if form.validate_on_submit():
        
        if form.email.data in che:
            
            if che[form.email.data][0]==form.password.data:
                session["username"]=form.email.data
                print("successfully login")
                flash(f"Successfully Log-in as {che[form.email.data][1]}","success")
                return redirect(url_for("home"))
            else:
                flash("INCORRECT PASSWORD","danger")
        else:
            flash("email is not registered! Please Register","danger")       
    return render_template("login.html",form=form,title="login")
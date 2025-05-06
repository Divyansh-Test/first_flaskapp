from flask import Flask, render_template, url_for, redirect, flash, request,session
from flaskblog.form import register
from functools import wraps
from flaskblog import app
def check_login(func):
	@wraps(func)
	def check(*args,**kwarg):
		if "username" in session:
			return func(*args,**kwarg)
		else:
			return redirect(url_for("register1"))
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

@app.route("/register1", methods=['GET', 'POST'])

def register1():
    form = register()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        print(f'{form.username.data} successfully created')
        session['username'] = form.username.data
        session.permanant=False
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            print("Form did not validate:")
            print(form.errors)
    return render_template('register.html', form=form, title="Register")

@app.route("/help")
def help():
    return render_template("help.html", title="Help")
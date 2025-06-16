from flask import render_template, url_for, redirect, flash, request,session
from sqlalchemy.orm.attributes import get_attribute
from flaskblog.form import Register,Login,Update
from functools import wraps
from flaskblog import app,db,bcrypt
from flaskblog.database import userdata,posts



def place_holder(Form,name):
    form=Form
    form.username.render_kw = {"placeholder": name}


    form.email.render_kw = {"placeholder": userdata.query.filter_by(username=name).first().email}
    form.Dob.render_kw = {"placeholder": userdata.query.filter_by(username=name).first().dob}


def check_login(func):
	@wraps(func)
	def funct(*args,**kwarg):
			
		if session["username"] !=None:
			return func(*args,**kwarg)
		else:
				
			return redirect(url_for("login"))
	
		return redirect(url_for("login"))
	return funct

@app.route("/")
@app.route("/home")
@check_login
def home():
    db.create_all()
    print(userdata.query.all())
    print(session["username"])

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

    if form.validate_on_submit():
        name = form.username.data
        flash(f'Account created for {name}!', 'success')

        user=userdata(username=form.username.data,email=form.email.data,password=bcrypt.generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))


    else:
        name = form.username.data
        flash(f'Error in creating account for {name}!', 'danger')



    return render_template('register.html', form=form, title="Register")

@app.route("/help")
def help():
    return render_template("help.html", title="Help")



@app.route("/login",methods=["GET","POST"])
def login():
    db.create_all()
    form=Login()
    if form.validate_on_submit():
        name=form.email.data
        passw=form.password.data
        check=userdata.query.filter_by(email=form.email.data).first()
        if check is None:
            flash(f'Login Unsuccessful. Please Register on Below Link or Check Your Username', 'danger')
            redirect(url_for('login'))
        elif bcrypt.check_password_hash(check.password,passw):
            session["username"]=check.username
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check your password', 'danger')







    return render_template("login.html",form=form,title="login")

@app.route("/update",methods=["GET","POST"])


@check_login

def update():
    print(session["username"])
    db.create_all() 
    form=Update()
    place_holder(form,session["username"])
    
    
    

    
    
    
    if form.cancel.data:
        return redirect(url_for("home"))
    elif form.submit.data and  form.validate_on_submit():
        print("submit pressed  ",session["username"])
        username=form.username.data
        email=form.email.data
        dob=form.Dob.data
        print('########',type(username))
 
            
        user=userdata.query.filter_by(username=session['username']).first()
        uname=session['username']
        
        print(session["username"],"\n",user)
        
            
        
            
        
            
        
        lst={'username':username.lower().strip(),'email':email,'dob':dob}
        for j in lst:
            if lst[j]!="":
                if j=='username':
                    if userdata.query.filter_by(username=lst[j]).first() is None:
                        user.username=lst[j].lower().strip()
                        db.session.commit()
                        session['username']=username.lower().strip()
                    else:
                        flash(f'Username already exist', 'danger')
                        return redirect(url_for("update"))
                    
                    
                        
                    
                elif j=='email':
                    if userdata.query.filter_by(email=lst[j]).first() is None:
                        user.email=lst[j]
                        db.session.commit()
                    else:
                        flash(f'Email already exist', 'danger')
                elif j=='dob':
                    user.dob=lst[j]
                    db.session.commit()
            







    return(render_template("update.html",form=form,title="update"))

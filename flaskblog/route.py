from flask import render_template, url_for, redirect, flash, session,request
import json

from flaskblog.form import Register,Login,Update,otp_form
from functools import wraps
from flaskblog import app,db,bcrypt
from flaskblog.database import userdata,admin
from flaskblog.send_mail import send_mail

session={"username":None,"otp":None,"role":None} #this is written because home is throwing an error and later none is converted to username
db.create_all()
def after_otp(a):
    dct={}
    for i in a:
        if i=="role":
            role=a[i]
            continue
        dct[i]=a[i]
    fnl=session["role"](**dct)
    session["role"]=None
    db.session.add(fnl)
    db.session.commit()



def place_holder(Form,name):
    form=Form
    form.username.render_kw = {"placeholder": name}


    form.email.render_kw = {"placeholder": userdata.query.filter_by(username=name).first().email}
    form.Dob.render_kw = {"placeholder": userdata.query.filter_by(username=name).first().dob}


def check_login(func):
    @wraps(func)
    def check(*args,**kwarg):
        if session["username"] is not None :
            return func(*args,**kwarg)
        else:
            return redirect(url_for("login"))
    return check


@app.route("/")
@app.route("/home")
@check_login
def home():
    
    
    
    print(session["username"])

    return render_template("home.html")

@app.route("/about")


@app.route("/register", methods=['GET', 'POST'])

def register():


    form = Register()

    if form.validate_on_submit():
        name = form.username.data
        flash(f'Account created for {name}!', 'success')
        if form.post_user.data=="user":
            role=userdata
        else:
            role=admin
        dict={"username":form.username.data,"email":form.email.data,"password":bcrypt.generate_password_hash(form.password.data).decode('utf-8')}
        
        
        session["role"]=role
        return redirect(url_for("otp_page",cpage="register",section="login",uemail=form.email.data,dict=json.dumps(dict)))


    else:
        name = form.username.data
        flash(f'Error in creating account for {name}!', 'danger')



    return render_template('register.html', form=form, title="Register")

@app.route("/help")
def help():
    return render_template("help.html", title="Help")



@app.route("/login",methods=["GET","POST"])
def login():
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
    
 
    form=Update()
    place_holder(form,session["username"])
    
    
    

    
    
    
    if form.cancel.data:
        return redirect(url_for("home"))
    elif form.submit.data and  form.validate_on_submit():
        
        
        
        username=form.username.data
        email=form.email.data
        dob=form.Dob.data
        
 
            
        user=userdata.query.filter_by(username=session['username']).first()
        uname=session['username']
        
        
        
            
        
            
        
            
        
        lst={'username':username,'email':email,'dob':dob}
        for j in lst:
            if lst[j]!="":
                if j=='username':
                    if userdata.query.filter_by(username=lst[j]).first() is None:
                        user.username=lst[j].lower().strip()
                        db.session.commit()
                        session['username']=username
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
            







    return(render_template("update.html",form=form,title="update"))


@app.route("/otp/<cpage>", methods=['GET', 'POST'])
def otp_page(*args,**kwargs):
    form = otp_form()
    uemail = request.args.get('uemail')
    page = request.args.get('section')
    dplay=request.args.get("cpage")
    dict = json.loads(request.args.get('dict'))
        

    # Store the OTP in session so it persists between requests
    if not session["otp"]:
        eotp = send_mail(receiver=uemail)
        session["otp"] = eotp
        print(eotp)
    

    if form.validate_on_submit():
        
        
        
        if int(form.Otp.data) == int(session["otp"]):
            
            after_otp(dict)
            session["otp"] = None
             # Clear the OTP after successful verification
            return redirect(url_for(page))
        else:
            flash('OTP is wrong', 'danger')

    return render_template("otp.html", title=f"otp/{dplay}", form=form)
    

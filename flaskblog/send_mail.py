import smtplib
import random
from email.message import EmailMessage
from flaskblog.secret_keys import email,passw
def send_mail(receiver,email=email,passw=passw):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email,passw)
    msg=EmailMessage()
    msg['From']="First Website Teams"
    msg['To']=receiver
    msg['Subject']="otp for login"
    otpm=random.randint(100000,999999)
    msg.set_content(f"Your otp for login is {otpm}")
    #server.send_message(msg)
    server.close()
    return otpm
if __name__=="__main__":
    send_mail(receiver="vampire02112006@gmail.com")
    
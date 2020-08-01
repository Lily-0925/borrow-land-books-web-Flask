from app import mail
from flask_mail import Message
from flask import current_app,render_template,current_app
import threading

def send_mail_sypotaniously(app,msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e

def send_mail(to,object,template,**kwargs):
    #msg = Message("test mail", sender="2711279210@qq.com", body="test", recipients = ["2711279210@qq.com"])
    msg = Message(object, sender=current_app.config["MAIL_USERNAME"], recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    thr = threading.Thread(target=send_mail_sypotaniously, args=[app.msg])
    thr.start()

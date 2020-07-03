from flask_mail import Mail, Message
from flask import render_template
from threading import Thread

mail = Mail()

def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def sendPasswordResetMail(app, user, reset_token):
    msg = Message(
        subject="[INTERMINE CLOUD] Password Reset",
        recipients=[user.data["email"]],
        sender=("Intermine","admin@cloud.intermine.eu"),
    )
    msg.html = render_template(
        "emails/reset_password_mail.html",
        name=user.data["first_name"],
        reset_token=reset_token
    )
    # Use a separate thread to send emails
    Thread(target=async_send_mail, args=(app, msg)).start()
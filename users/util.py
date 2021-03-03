import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskapp import  mail

#This subroutine allows the the picture inserted by the user for the profile to be saved as a result
def save_pic(form_picture):
    rand_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = rand_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/webby_pics', picture_fn)
    
    size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(size)

    i.save(picture_path)

    return picture_fn

#This allows the request email to be sent to the user . 
def send_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender = current_app.config.get("MAIL_USERNAME"), recipients = [user.email])
    msg.body = f''' To reset your password, visit the following link:
    {url_for('users.reset_tpassword', token = token, _external = True)}

    If you did not make this request , simply ignore this email and no change will be made 
    '''
    mail.send(msg)
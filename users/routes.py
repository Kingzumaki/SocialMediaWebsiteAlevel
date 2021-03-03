from flask import render_template, url_for, flash, redirect, request, Blueprint,current_app, jsonify
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp import db, bcrypt
from flaskapp.models import User, Post,Message,Notification
from flaskapp.users.forms import (SignUp, Login, UpdateAccount,
                                   RequestReset, ResetPassword, NewMessage) # this imports the classes from the python file 'forms.py' 
from flaskapp.users.util import save_pic, send_email

users = Blueprint('users', __name__) #This a blueprint which provides seperation at the Flask level . This seperates the whole folder called users from the application. This allows the sharing of application config, and can change an application object as necessary with being registered. 



@users.route("/signup", methods = ['GET','POST'] ) # This links the URL of the SignUp Page to this subroutine . The html methods being used are GET & POST
def signup():
    # If the current user is set , the user is automatically redirected to the user home page.
    if current_user.is_authenticated:
        return redirect(url_for('main.HomePage'))
    form = SignUp()#The form is set equal to the SignUp class in forms.py and undergoes the signup prcoess  
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf- 8') # This is Flask-Bcrypt (This is the hashing utility which applies a hash function on the password entered by the user. This turns the plain text password to a hash value)
        user = User(username = form.username.data, email = form.email.data, password = hashed_password) # The variable user is set equal to all the information inputted by the user such as Email,Password etc
        db.session.add(user) # The db.session.add() inserts the information enetred by the user into the database. Firstly it has to create the Python object which has been done above . Then it is added to the session.
        db.session.commit() # Lastly it has to be commited to the session in order to insert to the database
        flash('Your account has been created! You are now able to log in', 'success') # this prints a message telling the user that the account has been created successfully 
        return redirect(url_for('users.login')) # After the message has popped up the user will be redirected to the login page.
    return render_template('signup.html', title = 'Signup', form = form) # in order to render a HTML template the render_template() method has to be used. In order to render the template , the name of the template and the variables you want to pass to the template engine as keyword arguments have to be provided .
    # In this case template name 'signup.html' variables being passed- title = 'Signup', form = form



@users.route("/login", methods=['GET', 'POST']) # This links the URL of the login Page to this subroutine . The html methods being used are GET & POST
def login():
    # If the current user is logged in, the user is automatically redirected to the login page.
    if current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = Login() #The form is set equal to the Login class in forms.py and undergoes the login prcoess  
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first() # The user variable is set equal to the email address entered by the user.
        if user and bcrypt.check_password_hash(user.password, form.password.data): # if the email and password entered by the user is correct the user will be logged in and redirected to the main homepage.
            login_user(user, remember = form.remember.data)
            nextpage = request.args.get('next')
            return redirect(nextpage) if nextpage else redirect(url_for('main.HomePage'))
        else: # However if the email and password entered is not correct , a message will be flashed
            flash('Login Unsuccessful. Please check email and password', 'danger') # message flashed says 'Login Unsuccessful. Please check email and password'
    return render_template('login.html', title='Login', form=form) # This renders the HTML Template , the template name is 'login.html', variables being passed - title='Login', form=form


@users.route("/logout")# This links the URL /logout to this subroutine 
def logout():
    logout_user() # This logs the user out of their account 
    return redirect(url_for('main.HomePage')) # This redirects the logged out user to the homepage 


@users.route("/account",methods=['GET', 'POST']) # This links the URL of the account Page to this subroutine . The html methods being used are GET & POST
@login_required # This page can only be accessed when the user has logged in
def account():
    form = UpdateAccount()#The form is set equal to the UpdateAccount class in forms.py and undergoes the update account prcoess  
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pic(form.picture.data) # The variable picture_file is set equal to the picture 
            current_user.image_file = picture_file # The current profile picture of the user is now set equal to the picture chosen by the user 
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username # The new username entered by the user in the form is set equal to the current username of the user. This changes the username of the user's account
        form.email.data = current_user.email # The new email entered by the user in the form is set equal to the current email address of the user. This changes the email address of the user's account
    image_file = url_for('static', filename= 'webby_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', 
        image_file = image_file, form = form) # This renders the HTML Template , the template name is 'account.html', variables being passed - title='Account', image_file = image_file, form = form

@users.route('/user/<string:username>')  # This links the URL of the user's profile page to this subroutine . 
def user_post(username):
    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()#Gets First User with Username and if user does not exist , a page 404 is returned 
    posts = Post.query.filter_by(author= user).order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5 ) #Allows Posts to Be Posted on users profile page
    return render_template("user_post.html", posts = posts, user = user) # This renders the HTML Template , the template name is 'user_post.html', variables being passed - posts = posts, user = user

@users.route("/reset_password", methods = ['GET', 'POST'])  # This links the URL of the reset password page to this subroutine . The html methods being used are GET & POST
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.HomePage')) #If the current user is already logged in to an account the user will be redirected to the homepage
    form = RequestReset() #The form is set equal to the RequestReset class in forms.py and undergoes the request reset password prcoess  
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first() # The user variable is set equal to the email address entered by the user.
        send_email(user) #An email is sent to the email adress of the user entered in the form 
        flash('An email has been sent to reset your password', 'info') # Message displayed to user saying email has been sent succesfully
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title = "Reset Password", form = form)


#This function is linked to the resetting the password of the account 
@users.route("/reset_password/<token>", methods = ['GET', 'POST'])
def reset_tpassword(token): # the subroutine takes the argument token . The token is the link which is sent to the email address of the account. The token is set to expire in 60 minutes 
    if current_user.is_authenticated:
        return redirect(url_for('main.HomePage'))
    user = User.verify_reset_token(token) #This verifies that the user that clicked on the link sent is the correct account & email addrss   
    if not user:
        flash('That is an invalid or expired token', 'warning') #If token has expired after 1 hour or if the token is not linked to that emaiL, this text will pop up
        return redirect(url_for('users.reset_request'))
    form = ResetPassword() # variable form set equal to the class ResetPassword in forms.py 
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf- 8') # Hash function applied to new password entered by user
        user.password = hashed_password # Old password replaced by new password
        db.session.commit()
        flash('Your password has been changed! You are now able to log in', 'success')
        return redirect(url_for('users.login')) # User redirected to login page 
    return render_template("reset_tpassword.html", title = "Reset Password", form = form) 


@users.route('/follow/<string:username>')
def follow(username): # username is taken as argument in function
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.') # If user doesn't exist or there is an error, this message is popped up
        return redirect(url_for('main.HomePage'))
    if current_user.is_following(user):
        flash('You are already following this user.') # Message is displayed if the user tries to refollow an account that is already followed
        return redirect(url_for('users.user_post', username=username))
    if user == current_user:
        flash('You cannot follow yourself!') # If user tries to follow themselves this message is disolayed 
        return redirect(url_for('users.user_post', username=username))
    current_user.follow(user) # User now follows new user and this is commited to session in database 
    db.session.commit()
    flash('You are following {}!'.format(username)) # Message saying that specified user has been followed 
    return redirect(url_for('users.user_post', username=username))  

# Subroutine which allows a user to unfollow another user
@users.route('/unfollow/<string:username>')
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('main.HomePage'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('users.user_post', username=username))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('users.user_post', username=username))
    current_user.unfollow(user) # User now unfollows user and this is commited to session in database
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('users.user_post', username=username))

#Subroutine which displays a list of all of the followers of the end user.
@users.route('/followers/<string:username>') #This links the URL of the followers list page to this subroutine .
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid User.')
        return redirect(url_for('main.HomePage')) # If user clicked on is invalid , end-user is redirected to homepage
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False) 
    follows = [{'user': item.follower}
               for item in pagination.items] #Pagination created which displays the users folowers on various pages 
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


#This whole subroutine is similar to the def followers(username) subroutine. This subroutine displays a list of users that the ender is followeing 
@users.route('/followed_by/<string:username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('main.HomePage'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


#This is a subroutine which displays all of the private messages being sent to the end-user 
@users.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0) # When a message is read , the unread messages counter reduces in number 
    db.session.commit()
    #Below allows for pagination which allows mutiple messages to be shown on multiple pages
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.date_posted.desc()).paginate(page = page, per_page = 5)
    next_url = url_for('users.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('users.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)

#This is the subroutine for the notifications of a message.
@users.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.date_posted > since).order_by(Notification.date_posted.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'date_posted': n.date_posted
    } for n in notifications])

#This is the subroutine which allows for a private message to be sent from one user to another
@users.route('/send_message/<recipient>', methods=['GET', 'POST']) #This links the URL of the send_message to this subroutine .
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404() # The variable user is set equal tot that of the username of the user that message is being sent to . If the user can not be found, a 404 page is returned as a result.
    form = NewMessage() # The variable form is set equal to the NewMessage class in forms.py 
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      content=form.message.data)
        db.session.add(msg) # Message is added to the database
        user.add_notification('unread_message_count', user.new_messages()) #Unread messages counter increases
        db.session.commit() # The message is committed to the session of the database
        flash('Your message has been sent.')
        return redirect(url_for('users.user_post', username=recipient))
    return render_template('send_message.html', title=('Send Message'),
                           form=form, recipient=recipient)
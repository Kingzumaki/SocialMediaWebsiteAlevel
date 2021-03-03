import os 

#Creates a class called Congigrutation . All attributes need to be integrated into application for functionality
class Configuration:
    SECRET_KEY = os.environ.get('SECRET_KEY') # A secret key that will be used for securely signing the session cookie 
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') # This holds The database URI that will be used for the connection.
    MAIL_SERVER = 'smtp.aol.com' #Server that will be used to email user
    MAIL_PORT = 587 #Port neeeded to email user
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')# This holds the username  of the email account that will send reset password link to user
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS') # This holds the password of the email account that will send reset password link to user
    POSTS_PER_PAGE = 25 # Pagination showing that a maximum of 25 posts can be shown on each page
    COMMENTS_PER_PAGE = 30 #Pagination showing that a maximum of 30 comments can be shown on each page
    FOLLOWERS_PER_PAGE = 50 #Pagination showing that a maximum of 50 followers  can be shown on each page
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') # This a required public key needed to setup reCAPTCHA
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')# This a required private key needed to setup reCAPTCHA
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') #This holds the Elasticsearch URL needed for user to search for post searching and integrates it 
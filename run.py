from flaskapp import create_app
from flaskapp.models import User, Post, Notification, Message

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification}

if __name__== "__main__":
    app.run(debug=True)

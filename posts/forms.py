from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

#This is class is a form which allows a post to be created by a user
class NewPost(FlaskForm):
    title = StringField('Title', validators= [DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

# This class is a form which allows comments to be posted under a post
class NewComment(FlaskForm):
	content = TextAreaField('Comment', validators=[DataRequired()])
	submit = SubmitField('Submit')
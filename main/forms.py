from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

#This form allows the user to type inn what they want to search for 

class Searcher(FlaskForm):
    q = StringField(('Search'), validators=[DataRequired()]) 

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(Searcher, self).__init__(*args, **kwargs)
__author__ = 'abought'
import flask_wtf
import wtforms
from wtforms.validators import DataRequired


class CreatePollForm(flask_wtf.Form):
    """Create a poll"""
    title = wtforms.StringField('Title', validators=[DataRequired()])
    # Poll must have at least two choices. Else it's just silly
    choice1 = wtforms.StringField('Option 1', validators=[DataRequired()])
    choice2 = wtforms.StringField('Option 2', validators=[DataRequired()])
    choice3 = wtforms.StringField('Option 3')
    choice4 = wtforms.StringField('Option 4')
    choice5 = wtforms.StringField('Option 5')

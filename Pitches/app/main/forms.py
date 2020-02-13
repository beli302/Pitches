from wtforms.validators import Required
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from flask_wtf import FlaskForm

class PitchForm(FlaskForm):
    """
    Create a wtf form for creating a pitch
    """
    content = TextAreaField('Input your pitch')
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    """
    Create a wtf form for creating a pitch
    """
    opinion = TextAreaField('Write your comment')
    submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
    """
    Create a wtf form for creating a pitch
    """
    name =  StringField('Category Name', validators=[Required()])
    submit = SubmitField('Create')
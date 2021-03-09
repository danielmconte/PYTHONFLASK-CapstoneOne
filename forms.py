from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, BooleanField, StringField, PasswordField, FieldList
from wtforms.validators import InputRequired

# Class forms below (as needed)
class AddPhotoForm(FlaskForm):

    rover = SelectField("Rover", choices=[('curiosity', 'Curiosity'), ('spirit','Spirit'), ('insight', 'Insight'), ('perseverance', 'Perseverance')], validators=[InputRequired()])
    sol= IntegerField("Sol", validators=[InputRequired()])



class UserForm(FlaskForm):
    username= StringField("Username", validators=[InputRequired()])
    password= PasswordField("Password", validators=[InputRequired()])




    







 
    

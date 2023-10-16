from wtforms import SelectField, StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email")
    first_name = StringField("First_name", validators=[InputRequired()])
    last_name = StringField("Last_name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
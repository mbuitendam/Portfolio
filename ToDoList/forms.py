from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, DateField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

# Register User Form
class RegisterUser(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Your Name", validators=[DataRequired()])
    role = StringField("What is your role", validators=[DataRequired()])
    submit = SubmitField("Register")


# Login User Form
class loginUser(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# Add toDo item form
class addToDo(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subheading = StringField("Subheading", validators=[DataRequired()])
    content = CKEditorField("What are you trying to do", validators=[DataRequired()])
    dueDate = DateField()
    submit = SubmitField("Add Item")
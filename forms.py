from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User



class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=4, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),
                                                      Length(min=4, message="gadhe, password thoda majboot bana")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),
                                                      EqualTo("password", message="password must match")])
    submit = SubmitField("Sign Up")

    # extra check for already username taken
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError(f"Username: {username} is already taken")
        

    # extra check for already email taken
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError(f"email is already taken")
        


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), 
                                                     Length(min=4, message="gadhe, password thoda majboot bana")])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    body = TextAreaField("Body", validators=[DataRequired()])
    # tags for the user to include in his post
    tags = StringField("Tags (comma-separated karke likhna)")
    submit = SubmitField("Create Post")


class CommentForm(FlaskForm):
    body = TextAreaField("Add a comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")



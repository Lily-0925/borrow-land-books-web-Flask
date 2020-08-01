from wtforms import Form,StringField,IntegerField, PasswordField
from wtforms.validators import Length, NumberRange,DataRequired, Email, ValidationError,EqualTo
from app.models.user import User

class RegisterForm(Form):
    nickname = StringField(validators=[DataRequired(), Length(min=1,max=30)])
    email = StringField(validators=[DataRequired(), Email(message = "This email is not valid!")])
    password = PasswordField(validators=[DataRequired(message = "please enter you password"), Length(min=1,max=30)])

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This Email has exited")

    def validate_nickname(self, nickname):
        if User.query.filter_by(nickname=nickname.data).first():
            raise ValidationError("This nickname has exited")

class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Email(message = "This email is not valid!")])
    password = PasswordField(validators=[DataRequired(message = "please enter you password"), Length(min=1,max=30)])

class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Email(message="This email is not valid!")])

class ResetPassWordForm(Form):
    password1 = PasswordField(validators=[DataRequired(message="please enter you password"), Length(min=1, max=30),
                                          EqualTo("password2", message="These two password should be the same")])
    password2 = PasswordField(validators=[DataRequired(message="please enter you password again"),
                                          Length(min=1, max=30)])









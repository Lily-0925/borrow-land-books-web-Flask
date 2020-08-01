from wtforms import Form,StringField,IntegerField
from wtforms.validators import Length, NumberRange,DataRequired,Regexp

class searchform(Form):
    q = StringField(validators = [DataRequired(), Length(min=1,max=30)])
    page = IntegerField(validators = [NumberRange(min=1,max=99)], default = 1)

class DriftForm(Form):
    recipient_name = StringField(
        'receiver name', validators=[DataRequired(), Length(min=2, max=20,
                                                            message='The length of receiver should between 2 to 20')])
    mobile = StringField('phone number', validators=[DataRequired(),
                                                     Regexp('^1[0-9]{10}$', 0, 'Please input valid phone number')])
    message = StringField('message')
    address = StringField(
        'mail address', validators=[DataRequired(),
                                    Length(min=10, max=70, message='Please fill in full mail address')])

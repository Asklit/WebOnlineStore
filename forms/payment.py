from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class Payment(FlaskForm):
    name = StringField('', validators=[DataRequired()])
    surname = StringField('', validators=[DataRequired()])
    number_card = StringField('', validators=[DataRequired()])
    month = StringField('', validators=[DataRequired()])
    year = StringField('', validators=[DataRequired()])
    cvv = StringField('', validators=[DataRequired()])
    submit = SubmitField('Оплатить')

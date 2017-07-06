from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import DateField, BooleanField, SelectField, FloatField, StringField, PasswordField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, ValidationError

from app.util import TimeDeltaField

from wtforms_alchemy.fields import QuerySelectField
from app.models import Place
from app import db


def get_places():
    return Place.query


class NightForm(FlaskForm):
    day = DateField('Date', format='%d/%m/%Y', validators=[DataRequired()])
    to_bed = TimeField('Coucher', format='%H:%M', validators=[DataRequired()])
    to_rise = TimeField('Lever', format='%H:%M', validators=[DataRequired()])
    amount = TimeDeltaField('Durée', validators=[DataRequired()])
    alone = BooleanField('Seul')
    sleepless = BooleanField('Nuit blanche')
    place = QuerySelectField('Lieu', query_factory=get_places, validators=[DataRequired()])

    def to_bed_datetime(self):
        date = self.day.data
        btime = self.to_bed.data
        rtime = self.to_rise.data
        if btime > rtime:
            date = date - timedelta(days=1)
        return datetime.combine(date, btime)

    def to_rise_datetime(self):
        date = self.day.data
        rtime = self.to_rise.data
        return datetime.combine(date, rtime)

    def amount_timedelta(self):
        #return timedelta(hours=self.amount.data.hour,minutes=self.amount.data.minute)
        return self.amount.data

    def validate_amount(form, field):
        if field.data > (form.to_rise_datetime() - form.to_bed_datetime()):
            raise ValidationError('La durée de sommeil doit être inférieure à la durée de la nuit.')


class PlaceForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Identifiant', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])

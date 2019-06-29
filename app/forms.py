import pendulum
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import DateField, BooleanField, FloatField, StringField, PasswordField
from wtforms_components import TimeField
from wtforms.validators import InputRequired, ValidationError

from app.util import TimeDeltaField

from wtforms_alchemy.fields import QuerySelectField
from app.models import Place


def get_places():
    return Place.query


class NightForm(FlaskForm):
    day = DateField('Date', format='%d/%m/%Y', validators=[])
    to_bed = TimeField('Coucher', format='%H:%M', validators=[InputRequired()])
    to_rise = TimeField('Lever', format='%H:%M', validators=[InputRequired()])
    amount = TimeDeltaField('Durée', validators=[InputRequired()])
    alone = BooleanField('Seul')
    sleepless = BooleanField('Nuit blanche')
    place = QuerySelectField('Lieu', query_factory=get_places, validators=[InputRequired()])

    def to_bed_datetime(self):
        date = self.day.data
        btime = self.to_bed.data
        rtime = self.to_rise.data
        if btime > rtime:
            date = date - timedelta(days=1)
        # Keep it timezone unaware, as we store the local time in the nights table
        # and the timezone in the places table
        return datetime.combine(date, btime)

    def to_rise_datetime(self):
        date = self.day.data
        rtime = self.to_rise.data
        # Keep it timezone unaware, as we store the local time in the nights table
        # and the timezone in the places table
        return datetime.combine(date, rtime)

    def amount_timedelta(self):
        return self.amount.data

    def validate_amount(form, field):
        # take timezone into account in case of DST
        timezone = form.place.data.timezone
        to_rise_with_tz = pendulum.instance(form.to_rise_datetime(), tz=timezone)
        to_bed_with_tz = pendulum.instance(form.to_bed_datetime(), tz=timezone)
        if field.data > (to_rise_with_tz - to_bed_with_tz).as_interval():
            raise ValidationError('La durée de sommeil doit être inférieure à la durée de la nuit.')


class PlaceForm(FlaskForm):
    name = StringField('Nom', validators=[InputRequired()])
    latitude = FloatField('Latitude', validators=[InputRequired()])
    longitude = FloatField('Longitude', validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField('Identifiant', validators=[InputRequired()])
    password = PasswordField('Mot de passe', validators=[InputRequired()])

from flask import redirect
from flask import url_for
from datetime import datetime, timedelta
from app import app, db
from app.forms import NightForm
from app.places import Place
from flask import render_template, jsonify, request, abort
from sqlalchemy import func
import isodate
from app.util import dump_datetime


class Night(db.Model):
    __tablename__ = 'nights'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date, unique=True)
    sleepless = db.Column(db.Boolean)
    to_bed = db.Column(db.DateTime, unique=True)
    to_rise = db.Column(db.DateTime, unique=True)
    amount = db.Column(db.Interval)
    alone = db.Column(db.Boolean)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    place = db.relationship("Place")

    def __init__(self):
        pass

    def populate(self, day, sleepless, begin, end, amount, alone, place):
        self.day = isodate.parse_date(day)
        self.alone = alone
        self.place = place
        self.sleepless = sleepless
        if self.sleepless:
            self.to_bed = None
            self.to_rise = None
            self.amount = isodate.parse_duration("PT0H0M")
        else:
            self.to_bed = isodate.parse_datetime(begin)
            self.to_rise = isodate.parse_datetime(end)
            if amount == "":
                self.amount = self.to_rise - self.to_bed
            else:
                self.amount = isodate.parse_duration(amount)

    def __repr__(self):
        return '<Night ending on the %s>' % (self.day)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        dump_to_bed = ""
        dump_to_rise = ""
        if self.to_bed:
            dump_to_bed = dump_datetime(self.to_bed)
        if self.to_rise:
            dump_to_rise = dump_datetime(self.to_rise)

        return {
           'id': self.id,
           'sleepless': self.sleepless,
           'date': dump_datetime(self.day),
           'begin': dump_to_bed,
           'end': dump_to_rise,
           'amount': dump_datetime(self.amount),
           'alone': self.alone,
           'place_id': self.place_id
        }


@app.route('/nights', methods=['GET', 'POST'])
def show_nights():
    form = NightForm()
    places = []
    for p in Place.query.all():
        places.append((p.id, p.name))
    form.place.choices = places
    if form.validate_on_submit():
        new_night = Night()
        form.populate_obj(new_night)

        new_night.to_bed = form.to_bed_datetime()
        new_night.to_rise = form.to_rise_datetime()
        new_night.place = Place.query.get(form.place.data)
        new_night.amount = form.amount_timedelta()

        db.session.add(new_night)
        db.session.commit()
        return redirect(url_for('show_nights'))
    return render_template('nights2.html', form=form)

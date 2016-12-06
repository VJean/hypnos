from app import app, db
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

    def __init__(self, day, sleepless, begin, end, amount, alone, place):
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


@app.route('/nights', methods=['GET'])
def show_nights():
    return render_template('nights.html')


# API routes
# Nights
@app.route('/api/nights', methods=['GET'])
def get_nights():
    nlast = request.args.get('nlast')
    nights = Night.query.order_by(Night.day).all()
    if nlast is not None:
        nlast = int(nlast)
        nights = nights[-nlast:]
    return jsonify({'nights': [i.serialize for i in nights]})


@app.route('/api/nights/stats', methods=['GET'])
def get_stats():
    stats = []
    if request.args.get('q') == "places_repartition":
        stats = db.session.query(Night.place_id, func.count(Night.place_id)).group_by(Night.place_id).order_by(func.count(Night.place_id)).all()
    return jsonify({'stats': stats})


@app.route('/api/nights', methods=['POST'])
def create_night():
    if not request.json or 'begin' not in request.json:
        abort(400)
    place = Place.query.get(request.json.get('place_id'))
    night = Night(request.json.get('date'), request.json.get('sleepless'), request.json.get('begin'), request.json.get('end'), request.json.get('amount'), request.json.get('alone'), place)
    db.session.add(night)
    db.session.commit()
    return jsonify({'night': night.serialize}), 201


@app.route('/api/nights/<int:sid>', methods=['GET'])
def get_night(sid):
    return jsonify({'night': Night.query.filter(Night.id == sid).first().serialize})


@app.route('/api/nights/<int:sid>', methods=['DELETE'])
def delete_night(sid):
    s = Night.query.get(sid)
    if s is None:
        abort(404)

    db.session.delete(s)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/nights/<int:sid>', methods=['PUT'])
def update_night(sid):
    s = Night.query.get(sid)
    if s is None:
        abort(404)
    if not request.json:
        abort(400)

    if 'date' in request.json:
        s.day = isodate.parse_date(request.json.get('date'))
    if 'begin' in request.json:
        s.to_bed = isodate.parse_datetime(request.json.get('begin'))
    if 'end' in request.json:
        s.to_rise = isodate.parse_datetime(request.json.get('end'))
    if 'amount' in request.json and request.json.get('amount'):
        s.amount = isodate.parse_duration(request.json.get('amount'))
    s.alone = request.json.get('alone', s.alone)
    s.sleepless = request.json.get('sleepless', s.sleepless)
    if s.sleepless:
        s.to_bed = None
        s.to_rise = None
    if 'place_id' in request.json:
        s.place = Place.query.get(request.json.get('place_id'))
    db.session.commit()
    return jsonify({'night': s.serialize})

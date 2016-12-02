from app import app, db
from app.places import Place
from flask import render_template, jsonify, request, abort
import isodate
from app.util import dump_datetime


class Night(db.Model):
    __tablename__ = 'nights'
    id = db.Column(db.Integer, primary_key=True)
    to_bed = db.Column(db.DateTime, unique=True)
    to_rise = db.Column(db.DateTime, unique=True)
    amount = db.Column(db.Interval)
    alone = db.Column(db.Boolean)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    place = db.relationship("Place")

    def __init__(self, to_bed, to_rise, amount, alone, place):
        self.to_bed = isodate.parse_datetime(to_bed)
        self.to_rise = isodate.parse_datetime(to_rise)
        if amount == "":
            self.amount = self.to_rise - self.to_bed
        else:
            self.amount = isodate.parse_duration(amount)
        self.alone = alone
        self.place = place

    def __repr__(self):
        return '<Night from %r to %r>' % (self.to_bed, self.to_rise)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'id': self.id,
           'to_bed': dump_datetime(self.to_bed),
           'to_rise': dump_datetime(self.to_rise),
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
    nights = Night.query.order_by(Night.to_rise).all()
    if nlast is not None:
        nlast = int(nlast)
        nights = nights[-nlast:]
    return jsonify({'nights': [i.serialize for i in nights]})


@app.route('/api/nights', methods=['POST'])
def create_night():
    if not request.json or 'to_bed' not in request.json:
        abort(400)
    place = Place.query.get(request.json.get('place_id'))
    night = Night(request.json.get('to_bed'), request.json.get('to_rise'), request.json.get('amount'), request.json.get('alone'), place)
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

    if 'to_bed' in request.json:
        s.to_bed = isodate.parse_datetime(request.json.get('to_bed'))
    if 'to_rise' in request.json:
        s.to_rise = isodate.parse_datetime(request.json.get('to_rise'))
    if 'amount' in request.json and request.json.get('amount'):
        s.amount = isodate.parse_duration(request.json.get('amount'))
    s.alone = request.json.get('alone', s.alone)
    if 'place_id' in request.json:
        s.place = Place.query.get(request.json.get('place_id'))
    db.session.commit()
    return jsonify({'night': s.serialize})

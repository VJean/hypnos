from app import db
from datetime import datetime, timedelta
import isodate

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, timedelta):
        return isodate.duration_isoformat(value)

    raise TypeError("type not serializable")


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, unique=True)
    done = db.Column(db.Boolean)

    def __init__(self, content, done=False):
        self.content = content
        self.done = done
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<Note %r, %r>' % (self.content[:30], self.timestamp)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'id'       : self.id,
           'content'  : self.content,
           'done'     : self.done,
           'timestamp': dump_datetime(self.timestamp)
        }


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


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<Place named %r>' % self.name

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'id': self.id,
           'name': self.name,
           'lat': self.latitude,
           'lon': self.longitude
        }
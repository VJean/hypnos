import isodate
import pendulum
import requests
from sqlalchemy.ext.hybrid import hybrid_property

from app import db, bcrypt, TZ_DB_KEY
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
    place = db.relationship("Place", backref='nights')

    def __init__(self):
        pass

    @staticmethod
    def get_last_night():
        last = Night.query.order_by(Night.day.desc()).first()
        if last is None:
            return None
        return last

    @staticmethod
    def from_date(dref):
        n = Night.query.filter(Night.day == dref).one_or_none()
        return n

    def populate(self, day, sleepless, begin, end, amount, alone, place):
        self.day = pendulum.parse(day, exact=True)
        self.alone = alone
        self.place = place
        self.sleepless = sleepless
        if self.sleepless:
            self.to_bed = None
            self.to_rise = None
            self.amount = pendulum.Duration()
        else:
            self.to_bed = pendulum.parse(begin)
            self.to_rise = pendulum.parse(end)
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


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    archived = db.Column(db.Boolean)
    _latitude = db.Column(db.Float)
    _longitude = db.Column(db.Float)
    _timezone = db.Column(db.String(50))

    @staticmethod
    def find_timezone(lat, lon):
        tzdb_api_key = TZ_DB_KEY
        call = "http://api.timezonedb.com/v2.1/get-time-zone?key={}&format=json&by=position&lat={}&lng={}".format(tzdb_api_key, lat, lon)
        r = requests.get(call)
        rjson = r.json()
        if rjson['status'] != "OK":
            raise RuntimeError("Impossible d'obtenir le fuseau horaire (http://api.timezonedb.com): {}".format(rjson['message']))
        return rjson['zoneName']

    def __init__(self, name, lat, lon):
        self.name = name
        self._latitude = lat
        self._longitude = lon
        self._timezone = Place.find_timezone(self._latitude, self._longitude)

    def update(self, name, lat, lon):
        self.name = name
        update_tz = self._latitude != lat or self._longitude != lon
        self._latitude = lat
        self._longitude = lon
        if update_tz:
            self._timezone = Place.find_timezone(self._latitude, self._longitude)


    @hybrid_property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, lon):
        if lon != self._longitude and self._latitude is not None:
            self._timezone = Place.find_timezone(self._latitude, lon)
        self._longitude = lon

    @hybrid_property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, lat):
        if lat != self._latitude and self._longitude is not None:
            self._timezone = Place.find_timezone(lat, self._longitude)
        self._latitude = lat

    @hybrid_property
    def timezone(self):
        return self._timezone

    def __repr__(self):
        return '{!s}'.format(self.name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'lat': self.latitude,
            'lon': self.longitude,
            'tz': self.timezone,
            'archived': self.archived
        }


class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(255), nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def nb_users():
        return len(User.query.all())

    @staticmethod
    def create(username, password):
        user = User()
        user.username = username
        user.password = bcrypt.generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        print('Created user %s' % user.username)
        return user

import isodate
from sqlalchemy.orm import load_only

from app import db, bcrypt
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

    @staticmethod
    def get_last_date():
        last = Night.query.options(load_only("day")).order_by(Night.day.desc()).first()
        if last is None:
            return None
        return last.day

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


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def populate(self, name, latitude, longitude):
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

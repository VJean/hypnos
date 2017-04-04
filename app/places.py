from app import app, db
from flask import render_template, jsonify, request, abort


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


@app.route('/places', methods=['GET'])
def show_places():
    return render_template('places.html')

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


@app.route('/api/places', methods=['GET'])
def get_places():
    return jsonify({'places': [p.serialize for p in Place.query.all()]})


@app.route('/api/places', methods=['POST'])
def create_place():
    if not request.json or 'name' not in request.json:
        abort(400)
    place = Place(request.json.get('name'), request.json.get('lat'), request.json.get('lon'))
    db.session.add(place)
    db.session.commit()
    return jsonify({'place': place.serialize}), 201


@app.route('/api/places/<int:pid>', methods=['GET'])
def get_place(pid):
    return jsonify({'place': Place.query.filter(Place.id == pid).first().serialize})


@app.route('/api/places/<int:pid>', methods=['DELETE'])
def delete_place(pid):
    p = Place.query.get(pid)
    if p is None:
        abort(404)

    db.session.delete(p)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/places/<int:pid>', methods=['PUT'])
def update_place(pid):
    p = Place.query.get(pid)
    if p is None:
        abort(404)
    if not request.json:
        abort(400)
    p.name = request.json.get('name', p.name)
    p.longitude = request.json.get('lon', p.longitude)
    p.latitude = request.json.get('lat', p.latitude)
    db.session.commit()
    return jsonify({'place': p.serialize})

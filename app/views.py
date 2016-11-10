from app import app, db
from app import models
from flask import render_template, jsonify, request, abort
from fetch_posts import get_random_redditnugget
import isodate


@app.route('/')
def homepage():
    n = get_random_redditnugget()
    return render_template('index.html', nugget=n)


@app.route('/notes', methods=['GET'])
def show_notes():
    notes = models.Note.query.all()
    return render_template('show_notes.html', notes=notes)


@app.route('/nights', methods=['GET'])
def show_nights():
    nights = models.Night.query.all()
    dates = []
    durations = []
    for i in nights:
        dates.append(i.to_rise.date().isoformat())
        durations.append(i.amount.total_seconds() / 3600)
    a = {'x': dates, 'y': durations}
    return render_template('show_nights.html', nights=nights, amountchart=a)


@app.route('/places', methods=['GET'])
def show_places():
    return render_template('show_places.html')


# API routes
# Notes

@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = models.Note.query.order_by(models.Note.timestamp.desc()).all()
    return jsonify({'notes': [n.serialize for n in notes]})


@app.route('/api/notes', methods=['POST'])
def create_note():
    if not request.json or 'content' not in request.json:
        abort(400)
    note = models.Note(request.json.get('content'))
    db.session.add(note)
    db.session.commit()
    return jsonify({'note': note.serialize}), 201


@app.route('/api/notes/<int:nid>', methods=['GET'])
def get_note(nid):
    return jsonify({'note': models.Note.query.filter(models.Note.id == nid).first().serialize})


@app.route('/api/notes/<int:nid>', methods=['DELETE'])
def delete_note(nid):
    n = models.Note.query.get(nid)
    if n is None:
        abort(404)

    db.session.delete(n)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/notes/<int:nid>', methods=['PUT'])
def update_note(nid):
    n = models.Note.query.get(nid)
    if n is None:
        abort(404)
    if not request.json:
        abort(400)
    n.content = request.json.get('content', n.content)
    n.done = request.json.get('done', n.done)
    db.session.commit()
    return jsonify({'note': n.serialize})


# SleepItems

@app.route('/api/nights', methods=['GET'])
def get_nights():
    nlast = request.args.get('nlast')
    nights = models.Night.query.order_by(models.Night.to_rise).all()
    if nlast is not None:
        nlast = int(nlast)
        nights = nights[-nlast:]
    return jsonify({'nights': [i.serialize for i in nights]})


@app.route('/api/nights', methods=['POST'])
def create_night():
    if not request.json or 'to_bed' not in request.json:
        abort(400)
    place = models.Place.query.get(request.json.get('place_id'))
    item = models.Night(request.json.get('to_bed'), request.json.get('to_rise'), request.json.get('amount'), request.json.get('alone'), place)
    db.session.add(item)
    db.session.commit()
    return jsonify({'item': item.serialize}), 201


@app.route('/api/nights/<int:sid>', methods=['GET'])
def get_night(sid):
    return jsonify({'item': models.Night.query.filter(models.Night.id == sid).first().serialize})


@app.route('/api/nights/<int:sid>', methods=['DELETE'])
def delete_night(sid):
    s = models.Night.query.get(sid)
    if s is None:
        abort(404)

    db.session.delete(s)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/nights/<int:sid>', methods=['PUT'])
def update_night(sid):
    s = models.Night.query.get(sid)
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
        s.place = models.Place.query.get(request.json.get('place_id'))
    db.session.commit()
    return jsonify({'item': s.serialize})


# Places

@app.route('/api/places', methods=['GET'])
def get_places():
    return jsonify({'places': [p.serialize for p in models.Place.query.all()]})


@app.route('/api/places', methods=['POST'])
def create_place():
    if not request.json or 'name' not in request.json:
        abort(400)
    place = models.Place(request.json.get('name'))
    db.session.add(place)
    db.session.commit()
    return jsonify({'place': place.serialize}), 201


@app.route('/api/places/<int:pid>', methods=['GET'])
def get_place(pid):
    return jsonify({'place': models.Place.query.filter(models.Place.id == pid).first().serialize})


@app.route('/api/places/<int:pid>', methods=['DELETE'])
def delete_place(pid):
    p = models.Place.query.get(pid)
    if p is None:
        abort(404)

    db.session.delete(p)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/places/<int:pid>', methods=['PUT'])
def update_place(pid):
    p = models.Place.query.get(pid)
    if p is None:
        abort(404)
    if not request.json:
        abort(400)
    p.name = request.json.get('name', p.name)
    db.session.commit()
    return jsonify({'place': p.serialize})

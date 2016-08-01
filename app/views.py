from app import app, db
from app import models
from flask import render_template, jsonify, request, abort
from fetch_posts import get_random_redditnugget


@app.route('/')
def homepage():
    n = get_random_redditnugget()
    return render_template('index.html', nugget=n)


@app.route('/notes', methods=['GET'])
def show_notes():
    notes = models.Note.query.all()
    return render_template('show_notes.html', notes=notes)


@app.route('/sleep', methods=['GET'])
def show_sleepitems():
    sleepitems = models.SleepItem.query.all()
    return render_template('show_sleepitems.html', sleepitems=sleepitems)


@app.route('/places', methods=['GET'])
def show_places():
    places = models.Place.query.all()
    return render_template('show_places.html', places=places)


# API routes
# Notes

@app.route('/api/notes', methods=['GET'])
def get_notes():
    return jsonify({'notes': [n.serialize for n in models.Note.query.all()]})


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
    db.session.commit()
    return jsonify({'note': n.serialize})


# SleepItems

@app.route('/api/sleep', methods=['GET'])
def get_sleepitems():
    return jsonify({'sleepitems': [i.serialize for i in models.SleepItem.query.all()]})


@app.route('/api/sleep', methods=['POST'])
def create_sleepitem():
    if not request.json or 'to_bed' not in request.json:
        abort(400)
    place = models.Place.query.get(request.json.get('place_id'))
    item = models.SleepItem(request.json.get('to_bed'), request.json.get('to_rise'), request.json.get('amount'), request.json.get('alone'), place)
    db.session.add(item)
    db.session.commit()
    return jsonify({'item': item.serialize}), 201


@app.route('/api/sleep/<int:sid>', methods=['GET'])
def get_sleepitem(sid):
    return jsonify({'item': models.SleepItem.query.filter(models.SleepItem.id == sid).first().serialize})


@app.route('/api/sleep/<int:sid>', methods=['DELETE'])
def delete_sleepitem(sid):
    s = models.SleepItem.query.get(sid)
    if s is None:
        abort(404)

    db.session.delete(s)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/sleep/<int:sid>', methods=['PUT'])
def update_sleepitem(sid):
    s = models.SleepItem.query.get(sid)
    if s is None:
        abort(404)
    if not request.json:
        abort(400)
    s.to_bed = request.json.get('to_bed', s.to_bed)
    s.to_rise = request.json.get('to_rise', s.to_rise)
    s.amount = request.json.get('amount', s.amount)
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

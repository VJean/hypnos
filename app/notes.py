from app import app, db
from flask import render_template, jsonify, request, abort
from datetime import datetime
from app.util import dump_datetime


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


@app.route('/notes', methods=['GET'])
def show_notes():
    notes = Note.query.all()
    return render_template('notes.html', notes=notes)


@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = Note.query.order_by(Note.timestamp.desc()).all()
    return jsonify({'notes': [n.serialize for n in notes]})


@app.route('/api/notes', methods=['POST'])
def create_note():
    if not request.json or 'content' not in request.json:
        abort(400)
    note = Note(request.json.get('content'))
    db.session.add(note)
    db.session.commit()
    return jsonify({'note': note.serialize}), 201


@app.route('/api/notes/<int:nid>', methods=['GET'])
def get_note(nid):
    return jsonify({'note': Note.query.filter(Note.id == nid).first().serialize})


@app.route('/api/notes/<int:nid>', methods=['DELETE'])
def delete_note(nid):
    n = Note.query.get(nid)
    if n is None:
        abort(404)

    db.session.delete(n)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/notes/<int:nid>', methods=['PUT'])
def update_note(nid):
    n = Note.query.get(nid)
    if n is None:
        abort(404)
    if not request.json:
        abort(400)
    n.content = request.json.get('content', n.content)
    n.done = request.json.get('done', n.done)
    db.session.commit()
    return jsonify({'note': n.serialize})

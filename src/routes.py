from __main__ import app, db, ma

from flask import request, jsonify

from models import NoteSchema, NoteModel

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

@app.route('/notes')
def note_list():
    all_notes = NoteModel.query.all()
    return jsonify(notes_schema.dump(all_notes))


@app.route('/note', methods=['POST'])
def create_note():
    title = request.json.get('title', '')
    content = request.json.get('content', '')

    note = NoteModel(title=title, content=content)
    
    db.session.add(note)
    db.session.commit()
    
    return note_schema.jsonify(note)


@app.route('/note/<int:note_id>', methods=["GET"])
def note_detail(note_id):
    note = NoteModel.query.get(note_id)
    return note_schema.jsonify(note)


@app.route('/note/<int:note_id>', methods=['PATCH'])
def update_note(note_id):
    title = request.json.get('title', '')
    content = request.json.get('content', '')

    note = NoteModel.query.get(note_id)
    
    note.title = title
    note.content = content

    db.session.add(note)
    db.session.commit()

    return note_schema.jsonify(note)


@app.route('/note/<int:note_id>', methods=["DELETE"])
def delete_note(note_id):
    note = NoteModel.query.get(note_id)
    
    db.session.delete(note)
    db.session.commit()

    return note_schema.jsonify(note)
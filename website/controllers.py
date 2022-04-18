from flask import Blueprint, jsonify, request

from .auth import token_required
from .models import Note
from .shared import db

controllers = Blueprint('controllers', __name__)


@controllers.route('/notes')
@token_required
def get_notes(current_user):
    notes = Note.query.filter_by(user_id=current_user.id).all()
    output = []
    for note in notes:
        output.append({
            'title': note.title,
            'words': note.words,
            'progress': note.progress,
            'excerpt': note.excerpt,
            'content': note.content,
        })
    return jsonify(output)


@controllers.route('/note', methods=['POST'])
@token_required
def get_or_post_note(current_user):
    data = request.get_json()
    new_note = Note(title=data.get('title'), words=data.get('words'), progress=data.get('progress'),
                    excerpt=data.get('excerpt'), user_id=current_user.id)
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'new note created'})

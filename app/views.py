"""
    app.views
    ~~~~~~~~~~~~
"""
from datetime import datetime
from sqlalchemy.sql import func
from flask import abort, request, jsonify, Response
from app import db, app, ma, bcrypt

from app.users_notes import *

@app.route('/register/user', methods=['POST'])
def register():
    """Register new user."""
    username = request.form.get('username')
    if not username:
        abort(400, 'User name is not pointed!')
    if len(username) > 20:
        abort(400, 'User name is too long!')
    email = request.form.get('email')
    if not email:
        abort(400, 'Email is not pointed!')
    if len(email) > 50:
        abort(400, 'Email address is too long!')
    indx = email.find('@')
    if indx <= 0:
        abort(400, 'Bad email address!')
    passwd = request.form.get('passwd')
    if not passwd:
        abort(400, 'Password is not pointed!')
    pw_hash = bcrypt.generate_password_hash(passwd)

    if db.session.query(UserInfo).filter(UserInfo.username==username).first():
        abort(400, 'Such user already exists!')
    try:
        user = UserInfo(username=username, email=email, passwd=pw_hash)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        abort(400, 'Bad data: %s' % (str(e)))
    user_schema = UserInfoSchema()
    return user_schema.dump(user)

@app.route('/user/<username>', methods=['GET'])
def get_user_info_by_username(username):
    """Get user info by user name."""
    if not username:
        abort(400, 'User name is not pointed!')
    if len(username) > 20:
        abort(400, 'User name is too long!')
    user = db.session.query(UserInfo).filter(UserInfo.username==username).first()
    if not user:
        abort(400, 'User name %s does not exist!' % (username))
    user_schema = UserInfoSchema()
    return user_schema.dump(user)

@app.route('/deluser/<username>', methods=['DELETE'])
def del_user_info_by_username(username):
    """Delete user."""
    if not username:
        abort(403, 'User name is not pointed!')
    if len(username) > 20:
        abort(400, 'User name is too long!')
    user = db.session.query(UserInfo).filter(UserInfo.username==username).first()
    if not user:
        abort(403, 'User name %s does not exist!' % (username))
    db.session.delete(user)
    db.session.commit()
    return Response(status=200)

@app.route('/moduser/<username>', methods=['PUT'])
def mod_user_info_by_username(username):
    """Modify user information."""
    if not username:
        abort(403, 'User name is not pointed!')
    email = request.form.get('email')
    passwd = request.form.get('passwd')
    if not email and not passwd:
        abort(403, 'None data is not pointed for modification!')
    user = db.session.query(UserInfo).filter(UserInfo.username==username).first()
    if not user:
        abort(403, 'User name %s does not exist!' % (username))
    if email:
        user.email = email
    if passwd:
        user.passwd = bcrypt.generate_password_hash(passwd)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        abort(403, 'Bad input data: %s!' % (str(e)))
    user_schema = UserInfoSchema()
    return user_schema.dump(user)

@app.route('/add/note/<username>', methods=['POST'])
def add_note(username):
    """ Add new note."""
    if not username:
        abort(400, 'User name is not pointed!')
    user = db.session.query(UserInfo).filter(UserInfo.username==username).first()
    if not user:
        abort(400, 'User name %s does not exist!' % (username))
    text = request.form.get('text')
    if not text:
        abort(400, 'Text is absent!')
    if len(text) < 20 or len(text) > 404:
        abort(400, 'Text must contain more 19 and less 405 symbols!')
    tag_id = request.form.get('tag_id')
    if tag_id:
        try:
            tag_id = int(tag_id)
        except:
            abort(400, 'Tag ID parameter must be number!')
    else:
        tag_id = 0
    try:
        note = Notes(user_id=user.id, text=text, ctime=datetime.now(), tag_id=tag_id)
        db.session.add(note)
        db.session.commit()
    except Exception as e:
        abort(403, 'Bad input data: %s!' % (str(e)))
    try:
        note_id = db.session.query(func.max(Notes.id)).scalar()
        edituser = EditUser(note_id=note_id, user_id1=user.id)
        db.session.add(edituser)
        db.session.commit()
    except Exception as e:
        abort(403, 'Bad input data: %s!' % (str(e)))
    note_schema = NotesSchema()
    return note_schema.dump(note)

@app.route('/notes', methods=['GET'])
def get_note_ids():
    """Get all note ids with the corresponding user names."""
    user_notes = dict() 
    for user, note in db.session.query(UserInfo, Notes).\
                       filter(UserInfo.id==Notes.user_id).all():
        if not user_notes.get(user.id):
            user_notes[user.id] = list()
        user_notes[user.id].append(note.id)
    return jsonify(str(user_notes))

@app.route('/note/<note_id>', methods=['GET'])
def get_note_info_by_id(note_id):
    """Get note info by note Id."""
    if not note_id or not note_id.isnumeric():
        abort(403, 'Note id must be number!')
    note = db.session.query(Notes).filter(Notes.id==note_id).first()
    if not note:
        abort(403, 'Note id %d does not exist!' % (int(note_id)))
    note_schema = NotesSchema()
    return note_schema.dump(note)

@app.route('/edit/note/<note_id>/<username>', methods=['POST'])
def edit_note_info_by_id(note_id, username):
    """Edit note info identified by note Id by user ID (only 5 users may edit note!)."""
    if not note_id or not note_id.isnumeric():
        abort(403, 'Note id must be number!')
    if not username:
        abort(400, 'User name is not pointed!')
    text = request.form.get('text')
    if not text:
        abort(400, 'Text is not pointed!')
    if len(text) > 404:
        abort(400, 'Text is too long!')
    note = db.session.query(Notes).filter(Notes.id==note_id).first()
    if not note:
        abort(403, 'Note id %s does not exist!' % (note_id))
    user = db.session.query(UserInfo).filter(UserInfo.username==username).first()
    if not user:
        abort(400, 'User name %s does not exist!' % (username))
    edit_user = db.session.query(EditUser).filter(EditUser.note_id==note.id).first()
    access_list = (edit_user.user_id1, edit_user.user_id2,
                   edit_user.user_id3, edit_user.user_id4, edit_user.user_id5)
    if not user.id in access_list:
        if 0 in access_list:
            if not edit_user.user_id2:
                edit_user.user_id2 = user.id
            elif not edit_user.user_id3:
                edit_user.user_id3 = user.id
            elif not edit_user.user_id4:
                edit_user.user_id4 = user.id
            db.session.add(edit_user)
            db.session.commit()
        else:
            abort(400, 'User %s can not edit this note!' % (username))
    note.text = text
    db.session.add(note)
    statistic = Statistics(note_id=note.id, user_id=user.id, utime=datetime.now())
    db.session.add(statistic)
    db.session.commit()
    note_schema = NotesSchema()
    return note_schema.dump(note)

@app.route('/text/note', methods=['GET'])
def get_note_info_by_pattern():
    """Get note info by the text pattern from note."""
    pattern = request.form.get('text')
    if not pattern:
        abort(403, 'Text pattern is not pointed!')
    notes = db.session.query(Notes).filter(Notes.text.like('%' + pattern + '%')).all()
    notes_schema = NotesSchema(many=True)
    return jsonify(str(notes_schema.dump(notes)))

@app.route('/note_by_users', methods=['GET'])
def get_note_by_users():
    """Show an array with a list of users that edited note."""
    note_id = request.form.get('note_id')
    if not note_id:
        abort(403, 'Note id is not pointed!')
    if not note_id.isnumeric():
        abort(403, 'Note id must be number!')
    user = request.form.get('user')

    qname = 'db.session.query(Statistics).filter(Statistics.note_id==' + note_id + ')'
    if user:
        u = db.session.query(UserInfo).filter(UserInfo.username==user).first()
        if not u:
            abort(403, 'User name %s does not exist!' % (user))
        qname += '.filter(Statistics.user_id==' + str(u.id) + ')'
    statistics = eval(qname).all()
    statistics_schema = StatisticsSchema(many=True)
    return jsonify(str(statistics_schema.dump(statistics)))

@app.route('/del/note/<note_id>', methods=['DELETE'])
def del_note(note_id):
    """Delete note."""
    if not note_id:
        abort(403, 'Note id is not pointed!')
    note = db.session.query(Notes).filter(Notes.id==note_id).first()
    if not note:
        abort(403, 'Note id does not exist!')
    try:
        db.session.delete(note)
        db.session.commit()
    except Exception as e:
        abort(403, 'Delete error: %s' % (str(e)))
    return Response(status=200)

@app.route('/tag', methods=['POST'])
def add_tag():
    """Create tag."""
    tagname = request.form.get('name')
    if not tagname:
        abort(403, 'Tag name is not pointed!')
    tag = db.session.query(UserInfo).filter(Tags.name==tagname).first()
    if tag:
        abort(403, 'Tag name "%s" already exists!' % (tagname))
    tag = Tags(name=tagname);
    db.session.add(tag)
    db.session.commit()
    return Response(status=200)

@app.route('/tags', methods=['GET'])
def show_tags():
    """Show all tags."""
    tags = db.session.query(Tags).all()
    tags_schema = TagsSchema(many=True)
    return jsonify(str(tags_schema.dump(tags)))

from app import db, app, ma

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(50))
    passwd = db.Column(db.String(64))

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(404))
    ctime = db.Column(db.DateTime, nullable=False)
    tag_id = db.Column(db.Integer, default=0)

class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class EditUser(db.Model):
    __tablename__ = 'edit_user'
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer)
    user_id1 = db.Column(db.Integer, default=0)
    user_id2 = db.Column(db.Integer, default=0)
    user_id3 = db.Column(db.Integer, default=0)
    user_id4 = db.Column(db.Integer, default=0)
    user_id5 = db.Column(db.Integer, default=0)

class Statistics(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    utime = db.Column(db.DateTime, nullable=False)

class UserInfoSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email")

class NotesSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "text", "ctime", "tag_id")

class TagsSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")

class EditUserSchema(ma.Schema):
    class Meta:
        fields = ("note_id", "owner_id", "ctime", "user_id1",
		  "user_id2", "user_id3", "", "user_id4", "user_id1")

class StatisticsSchema(ma.Schema):
    class Meta:
        fields = ("note_id", "user_id", "utime")

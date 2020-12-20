from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql://katya:1@localhost/users_notes")

BaseModel = declarative_base()

class UserInfo(BaseModel):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(20))
    email = Column(String(50))
    passwd = Column(String(20))

    def __init__(self, name, email, passwd):
        self.user_name = name
        self.email = email
        self.passwd = passwd
    def __repr__(self):
        return "<UserInfo('%s','%s', '%s')>" % (self.user_name, self.email, self.passwd)


class Notes(BaseModel):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    text = Column(String(404))
    tag_id = Column(Integer)

    def __init__(self, text, tag_id):
        self.text = text
        self.tag_id = tag_id
    def __repr__(self):
        return "<Note('%d','%s', '%d')>" % (self.id, self.text, self.tag_id)


class Tags(BaseModel):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "<tags('%d','%s')>" % (self.id, self.name)


class EditUser(BaseModel):
    __tablename__ = 'edit_user'
    id = Column(Integer, primary_key=True)
    note_id = Column(Integer)
    owner_id = Column(Integer)
    ctime = Column(Integer, nullable=False)
    user_id1 = Column(Integer, default=0)
    user_id2 = Column(Integer, default=0)
    user_id3 = Column(Integer, default=0)
    user_id4 = Column(Integer, default=0)
    user_id5 = Column(Integer, default=0)

    def __init__(self, note_id, owner_id, ctime):
        self.note_id = note_id
        self.owner_id = owner_id
        self.ctime = ctime

    def __repr__(self):
        return "<EditUser('%s','%d'')>" % (self.note_id, self.owner_id, self.ctime)


class Statistics(BaseModel):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True)
    note_id = Column(Integer)
    user_id = Column(Integer)
    utime = Column(Integer, nullable=False)

    def __init__(self, name, email, passwd):
        self.note_id = note_id
        self.user_id = user_id
        self.stime = stime
        self.etime = etime
    def __repr__(self):
        return "<User('%d','%d', '%d', '%d')>" % (self.note_id, self.user_id, self.stime, self.etime)

BaseModel.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

user = UserInfo("Katya", "katya@ukr.net", "1")

session = Session()
session.add(user)
session.commit()

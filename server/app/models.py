from app import db, ma
from time import time

class User(db.Model):
    __tablename__ = "users"
    myid = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.Integer, nullable=False, default=int(time()))

    def __init__(self, name, password):
        self.name = name
        self.password = password
    
    def post(self):
        db.session.add(self)
        db.session.commit()
    
    def put(self, data):
        self.name = data['username']
        self.password = data['password']
        db.session.commit()

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class LeetCodeNote(db.Model):
    __tablename__ = "leetcodenote"
    myid = db.Column(db.Integer, db.Sequence('leetcodenote_id_seq'), primary_key=True)
    problem = db.Column(db.String(255), nullable=False)
    solution = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.Integer, nullable=False, default=int(time()))

    def __init__(self, problem, solution, message):
        self.problem = problem
        self.solution = solution
        self.message = message

    def post(self):
        db.session.add(self)
        db.session.commit()

class LeetCodeNoteSchema(ma.ModelSchema):
    class Meta:
        model = LeetCodeNote
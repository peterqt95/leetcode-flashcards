from app import db, ma

class User(db.Model):
    __tablename__ = "users"
    myid = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
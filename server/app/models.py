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
        for key in data:
            if getattr(self, key):
                setattr(self, key, data[key])
        db.session.commit()

class UserSchema(ma.ModelSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rename_map = {
            "my_id": "myId",
            "date_created": "dateCreated"
        }

    class Meta:
        model = User
    
    def dump(self, *args, **kwargs):
        rename = kwargs.pop("rename", None)
        results = super(UserSchema, self).dump(*args, **kwargs)
        if rename:
            # Adjust remapping if single vs multiple reutnr
            if isinstance(results, list):
                for result in results:
                    for field in result:
                        if field in rename:
                            result[rename[field]] = result.pop(field)
            else:
                for field in results:
                    if field in rename:
                        results[rename[field]] = results.pop(field)
        return results

class LeetCodeNote(db.Model):
    __tablename__ = "leetcodenote"
    myid = db.Column(db.Integer, db.Sequence('leetcodenote_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.myid"), nullable = False)
    problem = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    solution = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.Integer, nullable=False, default=int(time()))

    def __init__(self, title, problem, solution, message, user_id):
        self.title = title
        self.problem = problem
        self.solution = solution
        self.message = message
        self.user_id = user_id

    def post(self):
        db.session.add(self)
        db.session.commit()
    
    def put(self, data):
        for key in data:
            if getattr(self, key):
                setattr(self, key, data[key])
        db.session.commit()

class LeetCodeNoteSchema(ma.ModelSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rename_map = {
            "user_id": "userId",
            "myid": "myId",
            "date_created": "dateCreated"
        }

    class Meta:
        include_fk = True
        model = LeetCodeNote
    
    def dump(self, *args, **kwargs):
        rename = kwargs.pop("rename", None)
        results = super(LeetCodeNoteSchema, self).dump(*args, **kwargs)
        if rename:
            # Adjust remapping if single vs multiple reutnr
            if isinstance(results, list):
                for result in results:
                    for field in result:
                        if field in rename:
                            result[rename[field]] = result.pop(field)
            else:
                for field in results:
                    if field in rename:
                        results[rename[field]] = results.pop(field)
        return results
    
    def deserialize_args(self, params):
        deserialize_param_map = {v: k for k, v in self.rename_map.items()}
        new_params = {}
        for param in params.keys():
            values = params.getlist(param)
            if param in deserialize_param_map:
                new_params[deserialize_param_map[param]] = values
            else:
                new_params[param] = values
        return new_params
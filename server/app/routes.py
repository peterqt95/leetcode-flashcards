import sys
sys.path.insert(0, '/app/models')

from app import api
from app.models.User import User, UserSchema
from flask_restful import Resource, Api

class DefaultResource(Resource):
    def get(self):
        return {'task': 'Hello world'}
        
class UserResource(Resource):
    def __init__(self):
        self.users_schema = UserSchema(many=True)

    def get(self):
        users = User.query.all()
        return self.users_schema.dump(users)


api.add_resource(DefaultResource, '/')
api.add_resource(UserResource, '/users')
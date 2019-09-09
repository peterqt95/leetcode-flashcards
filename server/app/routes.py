import json
from app import api
from .models import User, UserSchema, LeetCodeNote, LeetCodeNoteSchema
from flask import request, session
from flask_restful import Resource, Api
from http import HTTPStatus

class Error():
    def __init__(self):
        self.status = False
        self.error = None
    
    def to_json(self):
        return {
            "error": self.error,
            "status": self.status
        }

class DefaultResource(Resource):
    def get(self):
        return {'task': 'Hello world'}
        
class UsersResource(Resource):
    def __init__(self):
        self.users_schema = UserSchema(many=True)

    def get(self):
        users = User.query.all()
        return self.users_schema.dump(users)
    
    def post(self):
        return_status = HTTPStatus.CREATED
        data = request.get_json(force = True)
        try:
            user = User(data['name'], data['password'])
            user.post()
        except Exception as e:
            print(e)
            return_status = HTTPStatus.FORBIDDEN

        return data, return_status

class UserResource(Resource):
    def __init__(self):
        self.user_schema = UserSchema()

    def get(self, id):
        return_status = HTTPStatus.OK
        try:
            user = User.query.get(id)
        except Exception as e:
            print(e)
            return_status = HTTPStatus.NOT_FOUND
        
        return self.user_schema.dump(user)
    
    def put(self, id):
        return_status = HTTPStatus.CREATED
        data = request.get_json(force = True)
        try:
            # Get the information
            user = User.query.filter_by(myid=id).first()

            # Update information from request
            user.put(data)
        except Exception as e:
            print(e)
            return_status = HTTPStatus.FORBIDDEN

        return data, return_status

class LeetCodeNotesResource(Resource):
    def __init__(self):
        self.leetcode_notes_schema = LeetCodeNoteResource(many=True)

    def get(self):
        leetcode_notes = LeetCodeNote.query.all()
        return self.leetcode_notes_schema(leetcode_notes)

class LeetCodeNoteResource(Resource):
    def __init__(self):
        self.leetcode_note_schema = LeetCodeNoteResource()

    def get(self, id):
        leetcode_note = LeetCodeNote.query.get(id)
        return self.leetcode_note_schema(leetcode_note)

class LoginRequired(Resource):
    def get(self):
        return_status = HTTPStatus.OK
        status = Error()
        try:
            username = request.args.get('name')
            if username and username in session:
                status.status = True
            else:
                status.error = "Not logged in"
        except Exception as e:
            status.error = str(e)
            return_status = HTTPStatus.BAD_REQUEST

        return status.to_json(), return_status

    def post(self):
        return_status = HTTPStatus.OK
        status = Error()
        data = request.get_json(force = True)
        try:
            # Get the info
            user = User.query.filter_by(name=data['name']).first()
            if user and data['password'] == user.password:
                session[user.name] = True
                status.status = True
            else:
                status.error = "Invalid username or password"
        except Exception as e:
            status.error = str(e)
            return_status = HTTPStatus.BAD_REQUEST
        
        return status.to_json(), return_status

api.add_resource(DefaultResource, '/')
api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(LeetCodeNotesResource, '/leetcode_notes')
api.add_resource(LeetCodeNoteResource, '/leetcode_notes/<int:id>')
api.add_resource(LoginRequired, '/login')

import json
from app import api, jwt, db
from .models import User, UserSchema, LeetCodeNote, LeetCodeNoteSchema
from flask import request, session
from flask_restful import Resource, Api
from http import HTTPStatus
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity, create_refresh_token,
    jwt_refresh_token_required
)

class Error():
    def __init__(self):
        self.status = False
        self.error = None
    
    def to_json(self):
        return {
            "error": self.error,
            "status": self.status
        }

class Token(Error):
    def __init__(self):
        super().__init__()
        self.access_token = ''
        self.refresh_token = ''
        self.name = ''
        self.user_id = -1
    
    def to_json(self):
        return {
            "error": self.error,
            "status": self.status,
            "accessToken": self.access_token,
            "refreshToken": self.refresh_token,
            "name": self.name,
            "userId": self.user_id,
        }

class DefaultResource(Resource):
    def get(self):
        return {'task': 'Hello world'}
        
class UsersResource(Resource):
    def __init__(self):
        self.users_schema = UserSchema(many=True)

    @jwt_required
    def get(self):
        users = User.query.all()
        return self.users_schema.dump(users)
    
    @jwt_required
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

    @jwt_required
    def get(self, id):
        return_status = HTTPStatus.OK
        try:
            user = User.query.get(id)
        except Exception as e:
            print(e)
            return_status = HTTPStatus.NOT_FOUND
        
        return self.user_schema.dump(user)

    @jwt_required
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
        self.leetcode_notes_schema = LeetCodeNoteSchema(many=True)

    @jwt_required
    def get(self):
        params = self.leetcode_notes_schema.deserialize_args(request.args)
        leetcode_notes = db.session.query(LeetCodeNote)
        print(params)
        for param, value in params.items():
            if isinstance(value, list):
                leetcode_notes = leetcode_notes.filter(getattr(LeetCodeNote, param).in_(value))
            else:
                leetcode_notes = leetcode_notes.filter(getattr(LeetCodeNote, param) == value)
        leetcode_notes = leetcode_notes.all()
        return self.leetcode_notes_schema.dump(leetcode_notes, rename=self.leetcode_notes_schema.rename_map)
    
    @jwt_required
    def post(self):
        return_status = HTTPStatus.CREATED
        status = Error()
        data = request.get_json(force = True)
        try:
            leetcode_note = LeetCodeNote(data['title'], data['problem'], data['solution'], data['message'], data['userId'])
            leetcode_note.post()
            status.status = True
        except Exception as e:
            status.error = str(e)
            return_status = HTTPStatus.FORBIDDEN

        return status.to_json(), return_status

class LeetCodeNoteResource(Resource):
    def __init__(self):
        self.leetcode_note_schema = LeetCodeNoteSchema()
    
    @jwt_required
    def get(self, id):
        leetcode_note = LeetCodeNote.query.get(id)
        return self.leetcode_note_schema.dump(leetcode_note, rename=self.leetcode_note_schema.rename_map)
    
    @jwt_required
    def put(self, id):
        return_status = HTTPStatus.CREATED
        data = request.get_json(force = True)
        try:
            # Get the information
            leetcode_note = LeetCodeNote.query.filter_by(myid=id).first()

            # Update information from request
            leetcode_note.put(data)
        except Exception as e:
            print(e)
            return_status = HTTPStatus.FORBIDDEN

        return data, return_status


class LoginRequired(Resource):
    @jwt_required
    def get(self):
        return_status = HTTPStatus.OK
        status = Error()
        try:
            current_user = get_jwt_identity()
            if current_user:
                status.status = True
            else:
                status.error = "Not logged in"
        except Exception as e:
            status.error = str(e)
            return_status = HTTPStatus.BAD_REQUEST

        return status.to_json(), return_status

    def post(self):
        return_status = HTTPStatus.OK
        status = Token()
        data = request.get_json(force = True)
        try:
            # Get the info
            user = User.query.filter_by(name=data['name']).first()
            if user and data['password'] == user.password:
                session[user.name] = True
                status.status = True
                status.access_token = create_access_token(identity=user.name)
                status.refresh_token = create_refresh_token(identity=user.name)
                status.name = user.name
                status.user_id = user.myid
            else:
                status.error = "Invalid username or password"
        except Exception as e:
            status.error = str(e)
            return_status = HTTPStatus.BAD_REQUEST
        
        return status.to_json(), return_status

class RefreshTokenResource(Resource):
    @jwt_refresh_token_required
    def get(self):
        return_status = HTTPStatus.OK
        status = Token()
        current_user = get_jwt_identity()
        if current_user:
            status.status = True
            status.access_token = create_access_token(identity=current_user)
        else:
            status.error = "Invalid refresh token"

        return status.to_json(), return_status

api.add_resource(DefaultResource, '/')
api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(LeetCodeNotesResource, '/leetcode_notes')
api.add_resource(LeetCodeNoteResource, '/leetcode_notes/<int:id>')
api.add_resource(LoginRequired, '/login')
api.add_resource(RefreshTokenResource, '/refresh')

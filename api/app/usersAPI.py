# https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flasgger.utils import swag_from

from app import app
api = Api(app)

USERS = {
    1: {'firstname': 'Coco', 'lastname': 'Bella'},
    2: {'firstname': 'Peachy', 'lastname': 'Peach'},
}

def abort_if_user_doesnt_exist(id):
    if id not in USERS:
        abort(404, message="User {} doesn't exist".format(id))

parser = reqparse.RequestParser()
parser.add_argument('firstname')
parser.add_argument('lastname')

class Users(Resource):
    @swag_from('user_get.yml')
    def get(self, id):
        id = int(id)
        abort_if_user_doesnt_exist(id)
        return USERS[id]

    @swag_from('user_update.yml')
    def put(self, id):
        id = int(id)
        args = parser.parse_args()
        name = {'firstname': args['firstname'], 'lastname': args['lastname']}
        USERS[id] = name
        return name, 201

    @swag_from('user_delete.yml')
    def delete(self, id):
        id = int(id)
        abort_if_user_doesnt_exist(id)
        del USERS[id]
        return '', 204

class UsersList(Resource):
    @swag_from('user_list.yml')
    def get(self):
        return USERS

    @swag_from('user_create.yml')
    def post(self):
        args = parser.parse_args()
        id = int(max(USERS.keys())) + 1
        USERS[id] = {'firstname': args['firstname'], 'lastname': args['lastname']}
        return USERS[id], 201


api.add_resource(Users, '/v1/users/<id>')
api.add_resource(UsersList, '/v1/userslist')
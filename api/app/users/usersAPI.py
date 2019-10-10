# https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
import json
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_jwt import jwt_required
from flasgger.utils import swag_from

from app import app
from app.db import mysql
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
        # return USERS[id]
        conn = mysql.connect()
        cursor = mysql.get_db().cursor()
        try:
            cursor.execute("SELECT first_name, last_name, email FROM user_info where id = %s", (int(id)))
            row_headers=[x[0] for x in cursor.description] 
            rows = cursor.fetchall()
            json_data=[]
            for result in rows:
                json_data.append(dict(zip(row_headers,result)))
            # return json.dumps(json_data)
            return jsonify(json_data[0])        
        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()


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
    @jwt_required()
    def get(self):
        #return USERS
        conn = mysql.connect()
        cursor = mysql.get_db().cursor()
        try:
            cursor.execute("SELECT first_name, last_name, email FROM user_info")
            row_headers=[x[0] for x in cursor.description]
            rows = cursor.fetchall()
            # resp = jsonify(rows)
            # resp.status_code = 200
            # return jsonify(resp)
            json_data = []
            for result in rows:
                json_data.append(dict(zip(row_headers,result)))
            return json_data[0]
        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()

    @swag_from('user_create.yml')
    def post(self):
        args = parser.parse_args()
        id = int(max(USERS.keys())) + 1
        USERS[id] = {'firstname': args['firstname'], 'lastname': args['lastname']}
        return USERS[id], 201


api.add_resource(Users, '/v1/users/<id>')
api.add_resource(UsersList, '/v1/userslist')
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flasgger.utils import swag_from

from app import app
api = Api(app)

class HelloWorld(Resource):
    @swag_from('hello.yml')
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/restful')
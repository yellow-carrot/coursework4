from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        request_json = request.json
        username = request_json.get('username')
        password = request_json.get('password')

        if None in [username, password]:
            return '', 401

        tokens = auth_service.generate_tokens(username, password)

        return tokens, 201

    def put(self):
        request_json = request.json
        token = request_json.get('refresh_token')
        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201
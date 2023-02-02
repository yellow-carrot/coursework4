from flask_restx import Resource, Namespace
from flask import request

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class GenresView(Resource):
    def get(self):
        page = request.args.get("page")
        filters = {
            "page": page,
        }

        all_users = user_service.get_all(filters)
        result = UserSchema(many=True).dump(all_users)
        return result, 200

    def post(self):
        request_json = request.json
        user = user_service.create(request_json)
        return '', 201, {'location': f'users/{user.id}'}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        result = UserSchema().dump(user)
        return result, 200

    def patch(self, uid):
        request_json = request.json
        if id not in request_json:
            request_json['id'] = uid

        user_service.update(request_json)
        return '', 204

    def delete(self, uid):
        user_service.delete(uid)

        return '', 204


@user_ns.route('/passwords')
class UpdateUserPasswordViews(Resource):
    def put(self):
        data = request.json
        email = data.get('email')
        old_password = data.geg('old_password')
        new_password = data.geg('new_password')

        user = user_service.get_user_by_email(email)

        if user_service.compare_pwds(user.password, old_password):
            user.password = user_service.create_pwd_hash(new_password)
            result = UserSchema().dump(user)
            user_service.update(result)
            print('Password updated')
        else:
            print('Password did not updated')
        return '', 201

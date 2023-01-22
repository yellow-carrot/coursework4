from flask_restx import Resource, Namespace
from flask import request
from dao.model.director import DirectorSchema
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        request_json = request.json
        director_service.create(request_json)
        return '', 201


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    def put(self, rid):
        request_json = request.json
        if rid not in request_json:
            request_json['rid'] = rid

        director_service.update(request_json)
        return '', 204

    def delete(self, rid):
        director_service.delete(rid)
        return '', 204


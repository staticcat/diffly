from flask_restful import Resource


class UserLogin(Resource):
    @staticmethod
    def get():
        return {'message': 'not yet implemented'}, 404


class UserLogout(Resource):
    @staticmethod
    def get():
        return {'message': 'not yet implemented'}, 404
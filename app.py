import json
from flask import Flask, Response, request
from flask_restful import Api, Resource
from werkzeug.exceptions import HTTPException

class HelloAPI(Resource):
    def get(self):
        data = {'Hello': 'Welcome to the Echo Room.'}
        return Response(response=json.dumps(data),
                        status=200,
                        mimetype='application/json')

class EchoAPI(Resource):

    STR_KEY = 'str'

    def post(self):
        try:
            data = request.get_json()
            s = data[STR_KEY]
        except (TypeError, KeyError):
            raise NoStringProvidedError
        except Exception as e:
            raise InternalServerError
        return Response(response=json.dumps({STR_KEY: s}),
                        status=200,
                        mimetype='application/json')

class InternalServerError(HTTPException):
    pass

class NoStringProvidedError(HTTPException):
    pass

errors = {
    'InternalServerError': {
        'message': 'Something went wrong',
        'status': 500},
    'NoStringProvidedError': {
        'message': 'Request must contain string to be echoed in variable \'str\'',
        'status': 400},
    }

app = Flask(__name__)
api = Api(app, errors=errors)
api.add_resource(HelloAPI, '/', '/hello')
api.add_resource(EchoAPI, '/echo')

if __name__ == '__main__':
    app.run(debug=True)

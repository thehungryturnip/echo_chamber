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
        data = request.get_json()
        try:
            s = data[self.STR_KEY]
        except (TypeError, KeyError):
            raise NoStringProvidedError

        return Response(response=json.dumps({self.STR_KEY: s}),
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
        'message': ('Request must contain string to be echoed in variable ' 
                    '\'str\''),
        'status': 400},
    }

app = Flask(__name__)
api = Api(app, errors=errors)
api.add_resource(HelloAPI, '/', '/hello')
api.add_resource(EchoAPI, '/echo')

if __name__ == '__main__':
    app.run(host='127.0.0.1',
            port='5000',
            ssl_context=('cert.pem', 'key.pem'),
            debug=True,
            )

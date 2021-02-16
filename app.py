import json
from flask import Flask, Response, request
from flask_restful import Api, Resource
from werkzeug.exceptions import HTTPException

# Hard coded auth tokens for the sake of simplicity
AUTH_TOKENS = ['W8cwfEUN2BsBNt5G4rMGQu9A',
               'n9hnzJY3MKjU5JXSSrH5hXfR',
               'suqku8Qm4FqUynH98cL98ZJG',
               'M7SnndsM7tVs7hfBhhJbADgv',
               'rzFsMgKEYsNRvdZnhBHSw8JC']

HTTP_ERRORS = {
    'InternalServerError': {
        'message': 'Something went wrong',
        'status': 500},
    'NoStringProvidedError': {
        'message': ('Request must contain string to be echoed in variable ' 
                    '\'str\''),
        'status': 400},
    'NotAuthorizedError': {
        'message': ('Request must contain valid authorization token in '
                    'valiable \'auth\''),
        'status': 401},
    }

class HelloAPI(Resource):
    """The purpose of this API is to be provide a simple response (as a test to
    make sure the server is up)."""

    def get(self):
        data = {'Hello': 'Welcome to the Echo Room.'}
        return Response(response=json.dumps(data),
                        status=200,
                        mimetype='application/json')

class EchoAPI(Resource):
    """This is the main ECHO API, providing 1 simple POST method that accepts a
    JSON payload with 2 key-value pairs: 'auth', with an auth token to be
    validated; and 'str', the string to be reflected back to the caller."""

    AUTH_KEY = 'auth'
    STR_KEY = 'str'

    def post(self):
        data = request.get_json()
        try:
            a = data[self.AUTH_KEY]
        except (TypeError, KeyError):
            raise NotAuthorizedError

        # Making sure the auth token provided is valid
        if not a in AUTH_TOKENS:
            raise NotAuthorizedError

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

class NotAuthorizedError(HTTPException):
    pass

app = Flask(__name__)
api = Api(app, errors=HTTP_ERRORS)
api.add_resource(HelloAPI, '/', '/hello')
api.add_resource(EchoAPI, '/echo')

if __name__ == '__main__':
    app.run(host='127.0.0.1',
            port='5000',
            ssl_context=('cert.pem', 'key.pem'),
            debug=True,
            )

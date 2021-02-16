import json
import random
import unittest
from app import app, errors, AUTH_TOKENS

class ServerLiveTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_server_is_active(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

class EchoApiTest(unittest.TestCase):
    
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.auth_token = random.choice(AUTH_TOKENS)

    def test_echo_different_strings(self):
        payload = {'auth': self.auth_token}
        strs = ['foobar', '123456', 'amy_bob$']
        for s in strs:
            payload['str'] = s
            response = self.app.post('/echo', 
                                     data=json.dumps(payload),
                                     content_type='application/json')
            response = response.get_json()
            self.assertEqual(response, {'str': s})

    def test_echo_no_string(self):
        payload = {'auth': self.auth_token}
        response = self.app.post('/echo',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        response = response.get_json()
        self.assertEqual(response, errors['NoStringProvidedError'])

    def test_echo_incorrect_key(self):
        keys = ['s', 'abc', '!@#', 'something else']
        for k in keys:
            payload = {'auth': self.auth_token, k: 'foobar'}
            response = self.app.post('/echo',
                                     data=json.dumps(payload),
                                     content_type='application/json')
            response = response.get_json()
            self.assertEqual(response,
                             errors['NoStringProvidedError'])

    def test_echo_mixed_keys(self):
        payload = {'a': 'one',
                   'b': 'two',
                   'c': 'three',
                   'str': 'foobar',
                   'd': 'four',
                   'auth': self.auth_token,
                   }
        response = self.app.post('/echo',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        response = response.get_json()
        self.assertFalse('a' in response)
        self.assertTrue('str' in response)
        self.assertEqual(response['str'], 'foobar')

    def test_echo_no_auth_token(self):
        payload = {'str': 'foobar'}
        response = self.app.post('/echo',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        response = response.get_json()
        self.assertEqual(response, errors['NotAuthorizedError'])

    def test_echo_invalid_auth_token(self):
        payload = {'auth': 'baz', 'str': 'foobar'}
        response = self.app.post('/echo',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        response = response.get_json()
        self.assertEqual(response, errors['NotAuthorizedError'])

if __name__ == '__main__':
    unittest.main()

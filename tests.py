import json
import random
import string
import unittest
from app import app, HTTP_ERRORS, AUTH_TOKENS

class ServerLiveTest(unittest.TestCase):
    def setUp(self):
        print('# SERVER LIVE TEST')
        app.testing = True
        self.app = app.test_client()

    def test_server_is_active(self):
        print('## Making sure server can be started...')
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

class EchoApiTest(unittest.TestCase):
    
    def setUp(self):
        print('# ECHO API TEST')
        app.testing = True
        self.app = app.test_client()
        self.auth_token = random.choice(AUTH_TOKENS)

    def test_echo_different_strings(self):
        print('## Testing different strings...')
        payload = {'auth': self.auth_token}
        strs = ['foobar', '123456', string.printable]
        for s in strs:
            payload['str'] = s
            print(f'\tPayload: {payload}')
            response = self.app.post('/echo', 
                                     data=json.dumps(payload),
                                     content_type='application/json')
            response = response.get_json()
            self.assertEqual(response, {'str': s})

    def test_echo_no_string(self):
        print('## Testing when no string is provided...')
        payload = {'auth': self.auth_token}
        print(f'\tPayload: {payload}')
        response = self.app.post('/echo',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        response = response.get_json()
        self.assertEqual(response, HTTP_ERRORS['NoStringProvidedError'])

    def test_echo_incorrect_key(self):
        print('## Testing when incorrect string key is provided...')
        keys = ['s', 'abc', '!@#', 'something else']
        for k in keys:
            payload = {'auth': self.auth_token, k: 'foobar'}
            print(f'\tPayload: {payload}')
            response = self.app.post('/echo',
                                     data=json.dumps(payload),
                                     content_type='application/json')
            response = response.get_json()
            self.assertEqual(response,
                             HTTP_ERRORS['NoStringProvidedError'])

    def test_echo_mixed_keys(self):
        print('## Testing when irrelevant keys are provided...')
        payload = {'a': 'one',
                   'b': 'two',
                   'c': 'three',
                   'str': 'foobar',
                   'd': 'four',
                   'auth': self.auth_token,
                   }
        print(f'\tPayload: {payload}')
        response = self.app.post('/echo',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        response = response.get_json()
        self.assertFalse('a' in response)
        self.assertTrue('str' in response)
        self.assertEqual(response['str'], 'foobar')

    def test_echo_no_auth_token(self):
        print('## Testing when no auth tokens are provided...')
        payload = {'str': 'foobar'}
        print(f'\tPayload: {payload}')
        response = self.app.post('/echo',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        response = response.get_json()
        self.assertEqual(response, HTTP_ERRORS['NotAuthorizedError'])

    def test_echo_invalid_auth_token(self):
        print('## Testing when invallid auth tokens are provided...')
        payload = {'auth': 'baz', 'str': 'foobar'}
        print(f'\tPayload: {payload}')
        response = self.app.post('/echo',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        response = response.get_json()
        self.assertEqual(response, HTTP_ERRORS['NotAuthorizedError'])

if __name__ == '__main__':
    unittest.main()

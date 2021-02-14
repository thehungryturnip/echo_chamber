import json
import unittest
from app import app, errors

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

    def test_echo_different_strings(self):
        strs = ['foobar', '123456', 'amy_bob$']
        for s in strs:
            response = self.app.post('/echo', 
                                     data=json.dumps({'str': s}),
                                     content_type='application/json')
            self.assertEqual(response.get_json(), {'str': s})

    def test_echo_no_string(self):
        response = self.app.post('/echo').get_json()
        self.assertEqual(response, errors['NoStringProvidedError'])

    def test_echo_incorrect_key(self):
        keys = ['s', 'abc', '!@#', 'something else']
        for k in keys:
            response = self.app.post('/echo',
                                     data=json.dumps({k: 'foobar'}),
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
                   }
        response = self.app.post('/echo',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        response = response.get_json()
        self.assertFalse('a' in response)
        self.assertTrue('str' in response)
        self.assertEqual(response['str'], 'foobar')

if __name__ == '__main__':
    unittest.main()

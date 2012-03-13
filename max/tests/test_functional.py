import unittest
import os
from paste.deploy import loadapp
import base64
import json

from mock import patch


class mock_post(object):

    def __init__(*args, **kwargs):
        pass

    text = ""
    status_code = 200


@patch('requests.post', new=mock_post)
class FunctionalTests(unittest.TestCase):

    def setUp(self):
        conf_dir = os.path.dirname(__file__)
        self.app = loadapp('config:tests.ini', relative_to=conf_dir)
        self.app.registry.max_store.drop_collection('users')
        self.app.registry.max_store.drop_collection('activity')
        from webtest import TestApp
        self.testapp = TestApp(self.app)

    def create_user(self, username):
        self.testapp.post('/people/%s' % username, "", basicAuthHeader('operations', 'operations'), status=201)

    def create_activity(self, username):
        from .mockers import user_status
        self.testapp.post('/people/%s/activities' % username, json.dumps(user_status), oauth2Header(username), status=201)

    def subscribe_user_to_context(self, username, context=None):
        from .mockers import subscribe_context
        self.testapp.post('/people/%s/subscriptions' % username, json.dumps(subscribe_context), basicAuthHeader('operations', 'operations'), status=201)

    def test_add_user(self):
        username = 'messi'
        res = self.testapp.post('/people/%s' % username, "", basicAuthHeader('operations', 'operations'), status=201)
        result = json.loads(res.text)
        self.assertEqual(result.get('username', None), 'messi')
        # u'{"username": "messi", "subscribedTo": {"items": []}, "last_login": "2012-03-07T22:32:19Z", "published": "2012-03-07T22:32:19Z", "following": {"items": []}, "id": "4f57e1f3530a693147000000"}'

    def test_user_exist(self):
        username = 'messi'
        self.create_user(username)
        res = self.testapp.post('/people/%s' % username, "", basicAuthHeader('operations', 'operations'), status=200)
        result = json.loads(res.text)
        self.assertEqual(result.get('username', None), 'messi')

    def test_get_user(self):
        username = 'messi'
        self.create_user(username)
        res = self.testapp.get('/people/%s' % username, "", oauth2Header(username))
        result = json.loads(res.text)
        self.assertEqual(result.get('username', None), 'messi')

    def test_get_user_not_me(self):
        username = 'messi'
        username_not_me = 'xavi'
        self.create_user(username)
        self.create_user(username_not_me)
        res = self.testapp.get('/people/%s' % username_not_me, "", oauth2Header(username), status=401)
        result = json.loads(res.text)
        self.assertEqual(result.get('error', None), 'Unauthorized')

    def test_get_non_existent_user(self):
        username = 'messi'
        res = self.testapp.get('/people/%s' % username, "", oauth2Header(username), status=400)
        result = json.loads(res.text)
        self.assertEqual(result.get('error', None), 'UnknownUserError')

    def test_modify_user(self):
        username = 'messi'
        self.create_user(username)
        res = self.testapp.put('/people/%s' % username, json.dumps({"displayName": "Lionel Messi"}), oauth2Header(username))
        result = json.loads(res.text)
        self.assertEqual(result.get('displayName', None), 'Lionel Messi')

    def test_modify_non_existent_user(self):
        username = 'messi'
        res = self.testapp.put('/people/%s' % username, json.dumps({"displayName": "Lionel Messi"}), oauth2Header(username), status=400)
        result = json.loads(res.text)
        self.assertEqual(result.get('error', None), 'UnknownUserError')

    def test_get_all_users(self):
        username = 'messi'
        self.create_user(username)
        res = self.testapp.get('/people', "", oauth2Header(username))
        result = json.loads(res.text)
        self.assertEqual(result.get('totalItems', None), 1)
        self.assertEqual(result.get('items', None)[0].get('username'), 'messi')

    def test_post_activity(self):
        from .mockers import user_status
        username = 'messi'
        self.create_user(username)
        res = self.testapp.post('/people/%s/activities' % username, json.dumps(user_status), oauth2Header(username), status=201)
        result = json.loads(res.text)
        self.assertEqual(result.get('actor', None).get('username', None), 'messi')
        self.assertEqual(result.get('object', None).get('objectType', None), 'note')
        self.assertEqual(result.get('contexts', None)[0].get('url', None), 'http://atenea.upc.edu/4127368123')

    def test_post_activity_not_me(self):
        from .mockers import user_status
        username = 'messi'
        username_not_me = 'xavi'
        self.create_user(username)
        self.create_user(username_not_me)
        res = self.testapp.post('/people/%s/activities' % username_not_me, json.dumps(user_status), oauth2Header(username), status=401)
        result = json.loads(res.text)
        self.assertEqual(result.get('error', None), 'Unauthorized')

    def test_post_activity_non_existent_user(self):
        from .mockers import user_status
        username = 'messi'
        res = self.testapp.post('/people/%s/activities' % username, json.dumps(user_status), oauth2Header(username), status=400)
        result = json.loads(res.text)
        self.assertEqual(result.get('error', None), 'UnknownUserError')

    def test_post_activity_no_auth_headers(self):
        from .mockers import user_status
        username = 'messi'
        self.create_user(username)
        res = self.testapp.post('/people/%s/activities' % username, json.dumps(user_status), status=401)
        result = json.loads(res.text)
        self.assertEqual(result.get('error', None), 'Unauthorized')

    def test_get_activity(self):
        username = 'messi'
        self.create_user(username)
        self.create_activity(username)
        res = self.testapp.get('/people/%s/activities' % username, "", oauth2Header(username), status=200)
        result = json.loads(res.text)
        self.assertEqual(result.get('totalItems', None), 1)
        self.assertEqual(result.get('items', None)[0].get('actor', None).get('username'), 'messi')
        self.assertEqual(result.get('items', None)[0].get('object', None).get('objectType', None), 'note')
        self.assertEqual(result.get('items', None)[0].get('contexts', None)[0].get('url', None), 'http://atenea.upc.edu/4127368123')

    def test_get_activity_not_me(self):
        username = 'messi'
        username_not_me = 'xavi'
        self.create_user(username)
        self.create_user(username_not_me)
        self.create_activity(username_not_me)
        res = self.testapp.get('/people/%s/activities' % username_not_me, "", oauth2Header(username), status=401)
        result = json.loads(res.text)
        self.assertEqual(result.get('error', None), 'Unauthorized')

    def test_get_activities(self):
        from .mockers import context_query
        username = 'messi'
        username_not_me = 'xavi'
        self.create_user(username)
        self.create_user(username_not_me)
        self.create_activity(username)
        self.create_activity(username_not_me)
        self.subscribe_user_to_context(username)
        res = self.testapp.get('/activities', context_query, oauth2Header(username), status=200)
        result = json.loads(res.text)
        self.assertEqual(result.get('totalItems', None), 2)
        self.assertEqual(result.get('items', None)[0].get('actor', None).get('username'), 'xavi')
        self.assertEqual(result.get('items', None)[0].get('object', None).get('objectType', None), 'note')
        self.assertEqual(result.get('items', None)[0].get('contexts', None)[0].get('url', None), 'http://atenea.upc.edu/4127368123')
        self.assertEqual(result.get('items', None)[1].get('actor', None).get('username'), 'messi')
        self.assertEqual(result.get('items', None)[1].get('object', None).get('objectType', None), 'note')
        self.assertEqual(result.get('items', None)[1].get('contexts', None)[0].get('url', None), 'http://atenea.upc.edu/4127368123')


    def test_subscribe_to_context(self):
        from .mockers import subscribe_context
        username = 'messi'
        self.create_user(username)
        self.create_activity(username)
        res = self.testapp.post('/people/%s/subscriptions' % username, json.dumps(subscribe_context), basicAuthHeader('operations', 'operations'), status=201)
        result = json.loads(res.text)
        self.assertEqual(result.get('actor', None).get('username', None), 'messi')
        self.assertEqual(result.get('object', None).get('objectType', None), 'context')
        self.assertEqual(result.get('object', None).get('url', None), 'http://atenea.upc.edu/4127368123')


def basicAuthHeader(username, password):
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    return dict(Authorization="Basic %s" % base64string)


def oauth2Header(username):
    return {"X-Oauth-Token": "jfa1sDF2SDF234", "X-Oauth-Username": username, "X-Oauth-Scope": "widgetcli"}

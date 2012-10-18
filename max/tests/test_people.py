# -*- coding: utf-8 -*-
import unittest
import os
from paste.deploy import loadapp
import base64
import json

from mock import patch


def basicAuthHeader(username, password):
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    return dict(Authorization="Basic %s" % base64string)


def oauth2Header(username):
    return {"X-Oauth-Token": "jfa1sDF2SDF234", "X-Oauth-Username": username, "X-Oauth-Scope": "widgetcli"}


class mock_post(object):

    def __init__(self, *args, **kwargs):
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
        self.app.registry.max_store.drop_collection('contexts')
        from webtest import TestApp
        self.testapp = TestApp(self.app)

    def create_user(self, username):
        res = self.testapp.post('/people/%s' % username, "", basicAuthHeader('operations', 'operations'), status=201)
        return res

    def modify_user(self, username, properties):
        res = self.testapp.put('/people/%s' % username, json.dumps(properties), oauth2Header(username))
        return res

    def create_activity(self, username, activity, oauth_username=None, expect=201):
        oauth_username = oauth_username is not None and oauth_username or username
        res = self.testapp.post('/people/%s/activities' % username, json.dumps(activity), oauth2Header(oauth_username), status=expect)
        return res

    def create_context(self, context, permissions=None, expect=201):
        default_permissions = dict(read='public', write='public', join='public', invite='subscribed')
        new_context = dict(context)
        if 'permissions' not in new_context:
            new_context['permissions'] = default_permissions
        if permissions:
            new_context['permissions'].update(permissions)
        res = self.testapp.post('/contexts', json.dumps(new_context), basicAuthHeader('operations', 'operations'), status=expect)
        return res

    def modify_context(self, context, properties):
        from hashlib import sha1
        url_hash = sha1(context).hexdigest()
        res = self.testapp.put('/contexts/%s' % url_hash, json.dumps(properties), basicAuthHeader('operations', 'operations'), status=200)
        return res

    def subscribe_user_to_context(self, username, context, expect=201):
        res = self.testapp.post('/people/%s/subscriptions' % username, json.dumps(context), basicAuthHeader('operations', 'operations'), status=expect)
        return res

    # BEGIN TESTS

    def test_add_user(self):
        username = 'messi'
        res = self.testapp.post('/people/%s' % username, "", basicAuthHeader('operations', 'operations'), status=201)
        result = json.loads(res.text)
        self.assertEqual(result.get('username', None), 'messi')
        u'{"username": "messi", "subscribedTo": {"items": []}, "last_login": "2012-03-07T22:32:19Z", "published": "2012-03-07T22:32:19Z", "following": {"items": []}, "id": "4f57e1f3530a693147000000"}'

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

    def test_modify_user_one_parameter(self):
        username = 'messi'
        self.create_user(username)
        res = self.testapp.put('/people/%s' % username, json.dumps({"displayName": "Lionel Messi"}), oauth2Header(username))
        result = json.loads(res.text)
        self.assertEqual(result.get('displayName', None), 'Lionel Messi')

    def test_modify_user_several_parameters(self):
        username = 'messi'
        self.create_user(username)
        res = self.testapp.put('/people/%s' % username, json.dumps({"displayName": "Lionel Messi", "twitterUsername": "leomessi"}), oauth2Header(username))
        result = json.loads(res.text)
        self.assertEqual(result.get('displayName', None), 'Lionel Messi')
        self.assertEqual(result.get('twitterUsername', None), 'leomessi')

    def test_modify_user_several_parameters_twice(self):
        username = 'messi'
        self.create_user(username)
        self.modify_user(username, {"displayName": "Lionel Messi"})
        res = self.testapp.put('/people/%s' % username, json.dumps({"twitterUsername": "leomessi"}), oauth2Header(username))
        result = json.loads(res.text)
        self.assertEqual(result.get('displayName', None), 'Lionel Messi')
        self.assertEqual(result.get('twitterUsername', None), 'leomessi')

    def test_modify_non_existent_user(self):
        username = 'messi'
        res = self.testapp.put('/people/%s' % username, json.dumps({"displayName": "Lionel Messi"}), oauth2Header(username), status=400)
        result = json.loads(res.text)
        self.assertEqual(result.get('error', None), 'UnknownUserError')

    def test_get_all_users(self):
        username = 'messi'
        self.create_user(username)
        res = self.testapp.get('/people', json.dumps({"username": username}), oauth2Header(username), status=200)
        result = json.loads(res.text)

        self.assertEqual(result.get('totalItems', ''), 1)
        self.assertEqual(result.get('items', '')[0].get('username', ''), username)
        self.assertEqual(len(result.get('items', '')[0].keys()), 2)

    def test_get_all_users_with_regex(self):
        username = 'usuarimoltllarg'
        self.create_user(username)
        query = {'username': 'usuarimoltll'}
        res = self.testapp.get('/people', json.dumps(query), oauth2Header(username), status=200)
        result = json.loads(res.text)
        self.assertEqual(result.get('items', '')[0].get('username', ''), username)

        query = {'username': 'usuarimo'}
        res = self.testapp.get('/people', json.dumps(query), oauth2Header(username), status=200)
        result = json.loads(res.text)
        self.assertEqual(result.get('items', '')[0].get('username', ''), username)

    def test_get_all_users_with_regex_weird(self):
        username1 = 'victor.fernandez'
        self.create_user(username1)
        username2 = 'victor.fernandez.altable'
        self.create_user(username2)

        query = {'username': username1}
        res = self.testapp.get('/people', query, oauth2Header(username1), status=200)
        result = json.loads(res.text)
        self.assertEqual(len(result.get('items', '')), 2)

        query = {'username': username2}
        res = self.testapp.get('/people', query, oauth2Header(username2), status=200)
        result = json.loads(res.text)
        self.assertEqual(len(result.get('items', '')), 1)
# -*- coding: utf-8 -*-
import os
import json
import unittest
from functools import partial

from mock import patch
from paste.deploy import loadapp

from max.tests.base import MaxTestBase, MaxTestApp, oauth2Header, mock_post
from max.tests import test_manager, test_default_security


class FunctionalTests(unittest.TestCase, MaxTestBase):

    def setUp(self):
        conf_dir = os.path.dirname(__file__)
        self.app = loadapp('config:tests.ini', relative_to=conf_dir)
        self.app.registry.max_store.drop_collection('users')
        self.app.registry.max_store.drop_collection('activity')
        self.app.registry.max_store.drop_collection('contexts')
        self.app.registry.max_store.drop_collection('security')
        self.app.registry.max_store.drop_collection('conversations')
        self.app.registry.max_store.drop_collection('messages')
        self.app.registry.max_store.security.insert(test_default_security)
        self.app.registry.max_security = test_default_security
        self.patched_post = patch('requests.post', new=partial(mock_post, self))
        self.patched_post.start()
        self.testapp = MaxTestApp(self)

    # BEGIN TESTS
    def test_get_all_users_admin(self):
        username = 'messi'
        self.create_user(username)
        res = self.testapp.get('/people', "", oauth2Header(test_manager))
        result = json.loads(res.text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get('username'), 'messi')

    def test_admin_post_activity_without_context(self):
        from .mockers import user_status
        username = 'messi'
        self.create_user(username)
        res = self.testapp.post('/people/%s/activities' % username, json.dumps(user_status), oauth2Header(test_manager))
        result = json.loads(res.text)
        self.assertEqual(result.get('actor', None).get('username', None), 'messi')
        self.assertEqual(result.get('object', None).get('objectType', None), 'note')
        self.assertEqual(result.get('contexts', None), None)

    def test_admin_post_activity_with_context(self):
        """ doctest .. http:post:: /people/{username}/activities """
        from .mockers import subscribe_context
        from .mockers import user_status_context
        from .mockers import create_context

        username = 'messi'
        self.create_user(username)
        self.create_context(create_context)
        self.admin_subscribe_user_to_context(username, subscribe_context)
        res = self.testapp.post('/people/%s/activities' % username, json.dumps(user_status_context), oauth2Header(test_manager))
        result = json.loads(res.text)
        self.assertEqual(result.get('actor', None).get('username', None), 'messi')
        self.assertEqual(result.get('object', None).get('objectType', None), 'note')
        self.assertEqual(result.get('contexts', None)[0]['url'], subscribe_context['object']['url'])

    def test_admin_post_activity_with_context_as_actor(self):
        """ doctest .. http:post:: /contexts/{hash}/activities """
        from .mockers import subscribe_context
        from .mockers import user_status_context
        from .mockers import create_context
        from hashlib import sha1
        self.create_context(create_context)
        url_hash = sha1(create_context['url']).hexdigest()
        res = self.testapp.post('/contexts/%s/activities' % url_hash, json.dumps(user_status_context), oauth2Header(test_manager), status=201)
        result = json.loads(res.text)
        self.assertEqual(result.get('actor', None).get('hash', None), url_hash)
        self.assertEqual(result.get('object', None).get('objectType', None), 'note')
        self.assertEqual(result.get('contexts', None)[0]['url'], subscribe_context['object']['url'])

    def test_get_security(self):
        res = self.testapp.get('/admin/security', "", oauth2Header(test_manager), status=200)
        result = json.loads(res.text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get('roles', None).get('Manager')[0], 'test_manager')

    def test_security_add_user_to_role(self):
        username = 'messi'
        self.create_user(username)
        res = self.testapp.post('/admin/security/roles/%s/users/%s' % ('Manager', username), "", oauth2Header(test_manager), status=201)
        self.assertListEqual(['messi', 'test_manager'], res.json)

    def test_security_add_user_to_non_allowed_role(self):
        username = 'messi'
        self.create_user(username)
        self.testapp.post('/admin/security/roles/%s/users/%s' % ('WrongRole', username), "", oauth2Header(test_manager), status=400)

    def test_security_remove_user_from_non_allowed_role(self):
        username = 'messi'
        self.create_user(username)
        self.testapp.delete('/admin/security/roles/%s/users/%s' % ('WrongRole', username), "", oauth2Header(test_manager), status=400)

    def test_security_add_user_to_role_already_has_role(self):
        res = self.testapp.post('/admin/security/roles/%s/users/%s' % ('Manager', 'test_manager'), "", oauth2Header(test_manager), status=200)
        self.assertListEqual(['test_manager'], res.json)

    def test_security_remove_user_from_role(self):
        username = 'messi'
        self.create_user(username)
        self.testapp.post('/admin/security/roles/%s/users/%s' % ('Manager', username), "", oauth2Header(test_manager), status=201)
        res = self.testapp.delete('/admin/security/roles/%s/users/%s' % ('Manager', username), "", oauth2Header(test_manager), status=200)
        self.assertListEqual(['test_manager'], res.json)

    def test_security_remove_user_from_role_user_not_in_role(self):
        username = 'messi'
        self.create_user(username)
        self.testapp.delete('/admin/security/roles/%s/users/%s' % ('Manager', username), "", oauth2Header(test_manager), status=404)

    def test_security_add_user_to_role_check_security_reloaded(self):
        test_manager2 = 'messi'
        self.create_user(test_manager2)
        self.testapp.get('/activities', "", oauth2Header(test_manager2), status=404)
        self.testapp.post('/admin/security/roles/%s/users/%s' % ('Manager', test_manager2), "", oauth2Header(test_manager), status=201)
        self.testapp.get('/activities', "", oauth2Header(test_manager2), status=200)

    def test_security_remove_user_from_role_check_security_reloaded(self):
        test_manager2 = 'messi'
        self.create_user(test_manager2)
        self.testapp.post('/admin/security/roles/%s/users/%s' % ('Manager', test_manager2), "", oauth2Header(test_manager), status=201)
        self.testapp.get('/activities', "", oauth2Header(test_manager2), status=200)
        self.testapp.delete('/admin/security/roles/%s/users/%s' % ('Manager', test_manager2), "", oauth2Header(test_manager), status=200)
        self.testapp.get('/activities', "", oauth2Header(test_manager2), status=404)

    def test_get_other_activities(self):
        from .mockers import user_status_context
        from .mockers import subscribe_context, create_context
        username = 'messi'
        self.create_user(username)
        self.create_user(test_manager)
        self.create_context(create_context)
        self.admin_subscribe_user_to_context(username, subscribe_context)
        self.create_activity(username, user_status_context)
        self.testapp.get('/people/%s/activities' % (username), '', oauth2Header(test_manager), status=200)

    def test_delete_user(self):
        username = 'messi'
        self.create_user(username)
        self.testapp.delete('/people/%s' % username, '', oauth2Header(test_manager), status=204)

    def test_delete_inexistent_user(self):
        username = 'messi'
        username2 = 'xavi'
        self.create_user(username)
        self.testapp.delete('/people/%s' % username2, '', oauth2Header(test_manager), status=404)

    def test_admin_delete_inexistent_activity(self):
        fake_id = '519200000000000000000000'
        self.testapp.delete('/activities/%s' % (fake_id), '', oauth2Header(test_manager), status=404)

    def test_admin_activities_search_by_context(self):
        """
        """
        from .mockers import user_status
        from .mockers import context_query
        from .mockers import create_context
        from .mockers import subscribe_context, user_status_context

        username = 'messi'
        self.create_user(username)
        self.create_context(create_context, permissions=dict(read='subscribed', write='subscribed', subscribe='restricted', invite='restricted'))
        self.admin_subscribe_user_to_context(username, subscribe_context)
        self.create_activity(username, user_status_context)
        self.create_activity(username, user_status)

        res = self.testapp.get('/people/%s/activities' % username, context_query, oauth2Header(test_manager), status=200)
        result = json.loads(res.text)
        self.assertEqual(len(result), 1)

    # def test_admin_post_activity_with_unauthorized_context_type_as_actor(self):
    #     from .mockers import create_unauthorized_context
    #     from hashlib import sha1

    #     result = self.create_context(create_invalid_context, expect=201)
    #     import ipdb;ipdb.set_trace()
        # url_hash = sha1(create_invalid_context['object']['url']).hexdigest()
        # res = self.testapp.post('/contexts/%s/activities' % url_hash, json.dumps(user_status_context), oauth2Header(test_manager))
        # result = json.loads(res.text)
        # self.assertEqual(result.get('actor', None).get('hash', None), url_hash)
        # self.assertEqual(result.get('object', None).get('objectType', None), 'note')
        # self.assertEqual(result.get('contexts', None)[0], subscribe_context['object'])

    def test_get_users_twitter_enabled(self):
        """ Doctest .. http:get:: /people """
        username = 'messi'
        username2 = 'xavi'
        self.create_user(username)
        self.create_user(username2)
        self.modify_user(username, {"twitterUsername": "messipowah"})
        res = self.testapp.get('/people', {"twitter_enabled": True}, oauth2Header(test_manager), status=200)

        self.assertEqual(len(res.json), 1)

    def test_get_context_twitter_enabled(self):
        from .mockers import create_context, create_contextA
        self.create_user(test_manager)
        self.create_context(create_context)
        self.create_context(create_contextA)
        self.modify_context(create_context['url'], {"twitterHashtag": "assignatura1", "twitterUsername": "maxupcnet"})

        res = self.testapp.get('/contexts', {"twitter_enabled": True}, oauth2Header(test_manager), status=200)

        self.assertEqual(len(res.json), 1)

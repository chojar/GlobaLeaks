# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks

import json

from globaleaks.rest import requests
from globaleaks.tests import helpers
from globaleaks.handlers import overview

class TestUsersOverview(helpers.TestHandlerWithPopulatedDB):
    _handler = overview.Users

    @inlineCallbacks
    def setUp(self):
        yield helpers.TestHandlerWithPopulatedDB.setUp(self)
        yield self.perform_submission()

    @inlineCallbacks
    def test_get(self):
        handler = self.request({}, role='admin')
        yield handler.get()

        self.assertTrue(isinstance(self.responses, list))
        self.assertEqual(len(self.responses), 1)
        self.assertEqual(len(self.responses[0]), 2)
        self._handler.validate_message(json.dumps(self.responses[0]), requests.UsersOverview)


class TestTipsOverview(helpers.TestHandlerWithPopulatedDB):
    _handler = overview.Tips

    @inlineCallbacks
    def setUp(self):
        yield helpers.TestHandlerWithPopulatedDB.setUp(self)
        yield self.perform_submission()

    @inlineCallbacks
    def test_get(self):
        handler = self.request({}, role='admin')
        yield handler.get()

        self.assertTrue(isinstance(self.responses, list))
        self.assertEqual(len(self.responses), 1)
        self.assertEqual(len(self.responses[0]), 1)
        self._handler.validate_message(json.dumps(self.responses[0]), requests.TipsOverview)


class TestFilesOverview(helpers.TestHandlerWithPopulatedDB):
    _handler = overview.Files

    @inlineCallbacks
    def setUp(self):
        yield helpers.TestHandlerWithPopulatedDB.setUp(self)
        yield self.perform_submission()

    @inlineCallbacks
    def test_get(self):
        handler = self.request({}, role='admin')
        yield handler.get()

        self.assertTrue(isinstance(self.responses, list))
        self.assertEqual(len(self.responses), 1)
        self._handler.validate_message(json.dumps(self.responses[0]), requests.FilesOverview)

# -*- coding: utf-8 -*-
from twisted.internet.defer import inlineCallbacks

import json

from globaleaks.rest import requests
from globaleaks.tests import helpers
from globaleaks.handlers import receiver, admin, submission
from globaleaks.settings import GLSetting
from globaleaks.jobs import delivery_sched
from globaleaks.jobs.notification_sched import NotificationSchedule

class TestReceiverInstance(helpers.TestHandlerWithPopulatedDB):
    _handler = receiver.ReceiverInstance

    @inlineCallbacks
    def test_get(self):
        handler = self.request(role='receiver')

        rcvrs = yield admin.get_receiver_list('en')
        for rcvr in rcvrs:
            handler = self.request(role='receiver')
            handler.current_user.user_id = rcvr['id']

            yield handler.get()

    @inlineCallbacks
    def test_put_data_obtained_with_get(self):
        handler = self.request(role='receiver')

        rcvrs = yield admin.get_receiver_list('en')
        for rcvr in rcvrs:
            handler = self.request(role='receiver')
            handler.current_user.user_id = rcvr['id']

            yield handler.get()

            handler = self.request(self.responses[0], role='receiver')
            handler.current_user.user_id = rcvr['id']
            yield handler.put()

    @inlineCallbacks
    def test_put_with_remove_pgp_flag_true(self):
        handler = self.request(role='receiver')

        rcvrs = yield admin.get_receiver_list('en')
        for rcvr in rcvrs:
            handler = self.request(role='receiver')
            handler.current_user.user_id = rcvr['id']

            yield handler.get()

            self.responses[0]['gpg_key_remove'] = True

            handler = self.request(self.responses[0], role='receiver')
            handler.current_user.user_id = rcvr['id']
            yield handler.put()

    @inlineCallbacks
    def test_ping_mail_change(self):
        handler = self.request(role='receiver')

        rcvrs = yield admin.get_receiver_list('en')
        for rcvr in rcvrs:
            handler = self.request(role='receiver')
            handler.current_user.user_id = rcvr['id']

            yield handler.get()

            self.responses[0]['ping_mail_address'] = 'ortomio@x.com'

            handler = self.request(self.responses[0], role='receiver')
            handler.current_user.user_id = rcvr['id']
            yield handler.put()

class TestTipsCollection(helpers.TestHandlerWithPopulatedDB):
    _handler = receiver.TipsCollection

    @inlineCallbacks
    def setUp(self):
        yield helpers.TestHandlerWithPopulatedDB.setUp(self)
        yield self.perform_submission()

    @inlineCallbacks
    def test_get(self):
        handler = self.request(role='receiver')
        handler.current_user.user_id = self.dummyReceiver_1['id']
        yield handler.get()

class TestNotificationCollection(helpers.TestHandlerWithPopulatedDB):
    _handler = receiver.NotificationCollection

    @inlineCallbacks
    def setUp(self):
        yield helpers.TestHandlerWithPopulatedDB.setUp(self)
        yield self.perform_submission()
 
    @inlineCallbacks
    def test_get(self):
        handler = self.request(role='receiver')
        handler.current_user.user_id = self.dummyReceiver_1['id']
        yield handler.get()

        self.assertEqual(len(self.responses), 1)
        self.assertEqual(len(self.responses[0]['tips']), 1)
        self.assertEqual(len(self.responses[0]['activities']), 5)

    @inlineCallbacks
    def test_delete(self):
        handler = self.request(role='receiver')
        handler.current_user.user_id = self.dummyReceiver_1['id']
        yield handler.delete()

        self.assertEqual(len(self.responses), 0)

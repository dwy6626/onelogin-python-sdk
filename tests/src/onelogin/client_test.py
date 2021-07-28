# -*- coding: utf-8 -*-

# Copyright (c) 2017, OneLogin, Inc.
# All rights reserved.

import unittest

from onelogin.api.client import OneLoginClient


class OneLogin_API_Client_Test(unittest.TestCase):

    def testClientWithData(self):
        """
        Tests the constructor method of the OneLoginClient class
        Build a OneLoginClient object with a client_id and client_secret
        """
        client = OneLoginClient(
            client_id='test_client_id',
            client_secret='test_client_secret'
        )
        self.assertIsNot(client, None)
        self.assertEqual('test_client_id', client.client_id)
        self.assertEqual('test_client_secret', client.client_secret)
        self.assertEqual('us', client.url_builder.region)

    def testClientWithDataAndRegion(self):
        """
        Tests the constructor method of the OneLoginClient class
        Build a OneLoginClient object with a client_id, client_secret and region
        """
        client = OneLoginClient(
            client_id='test_client_id',
            client_secret='test_client_secret',
            region='eu'
        )
        self.assertIsNot(client, None)
        self.assertEqual('test_client_id', client.client_id)
        self.assertEqual('test_client_secret', client.client_secret)
        self.assertEqual('eu', client.url_builder.region)

    def testClientWithNoData(self):
        """
        Tests the constructor method of the OneLoginClient class
        Build a OneLoginClient object with no data
        """
        with self.assertRaises(Exception):
            client = OneLoginClient()
            self.assertIsNot(client, None)

    def testClientDefaultErrorValues(self):
        """
        Tests the constructor method of the OneLoginClient class
        Build a OneLoginClient object and check if the error attributes exist and are None
        """
        client = OneLoginClient(
            client_id='test_client_id',
            client_secret='test_client_secret',
            region='eu'
        )
        self.assertIsNone(client.error)
        self.assertIsNone(client.error_description)

    def testGetVersionID(self):
        """
        Tests the method to get endpoint version
        """
        client = OneLoginClient(
            client_id='test_client_id',
            client_secret='test_client_secret',
        )
        version = client.get_version_id('GET_APPS_URL')
        self.assertEqual(version, 1)

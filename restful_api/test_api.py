#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

import application


class DataTests(unittest.TestCase):
    def setUp(self):
        application.app.config['TESTING'] = False
        application.app.config['WTF_CSRF_ENABLED'] = False
        application.app.config['DEBUG'] = False

        self.app = application.app.test_client()

    def tearDown(self):
        pass

    def test_endpoint_1(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_2(self):
        response = self.app.get('/sorry', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_3(self):
        response = self.app.get('/submit', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_4(self):
        response = self.app.get('/submit', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_endpoint_5(self):
        response = self.app.get('/thanks', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_6(self):
        response = self.app.get('/thanks', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_endpoint_7(self):
        response = self.app.get('/close', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_8(self):
        response = self.app.get('/current_round', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_9(self):
        response = self.app.get('/get_all_rounds', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_10(self):
        response = self.app.get('/list_all_rounds', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_11(self):
        response = self.app.get('/round', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_12(self):
        response = self.app.get('/round2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_13(self):
        response = self.app.get('/statistics', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_14(self):
        response = self.app.get('/statistics2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_auto_close(self):
        expected = True
        response = application.close_automatically(remaining=0)

        self.assertEqual(response, expected)


if __name__ == '__main__':
    unittest.main()

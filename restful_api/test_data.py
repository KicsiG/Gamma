#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

import application


class DataTests(unittest.TestCase):
    def setUp(self):
        self.data = application.Data()

        self.active_game_mock_data = {
            'players': [
                'a',
                'b'
            ],
            'round_id': 1589898360,
            'votes': [
                5,
                6
            ]
        }

        self.previous_games_mock_data = {
            1589898360: {
                'players': ['a', 'b'],
                'votes': [5, 6],
                'start': 1589898360,
                'end': 1589902017,
                'winner': 'a',
                'winner_number': 5
            }
        }

        self.data.active_game = self.active_game_mock_data
        self.data.previous_games = self.previous_games_mock_data

    def tearDown(self):
        pass

    def test_get_active_game_data(self):
        expected = self.active_game_mock_data
        response = self.data.get_active_game

        self.assertEqual(response, expected)

    def test_is_active_game_1(self):
        expected = True
        response = self.data.is_active_game

        self.assertEqual(response, expected)

    @unittest.expectedFailure
    def test_is_active_game_2(self):
        expected = False
        response = self.data.is_active_game

        self.assertEqual(response, expected)

    @unittest.expectedFailure
    def test_is_active_game_3(self):
        self.data.active_game.clear()
        expected = True
        response = self.data.is_active_game

        self.assertEqual(response, expected)

    def test_get_active_game_start_1(self):
        expected = 1589898360
        response = self.data.get_active_game_start

        self.assertEqual(response, expected)

    @unittest.expectedFailure
    def test_get_active_game_start_2(self):
        expected = 1589889360
        response = self.data.get_active_game_start

        self.assertEqual(response, expected)

    def test_add_round(self):
        self.data.active_game.clear()
        self.data.add_round(1234567689)

        expected = {
            'round_id': 1234567689,
            'players': [],
            'votes': []
        }
        response = self.data.get_active_game

        self.assertEqual(response, expected)

    def test_get_round_id_1(self):
        expected = 1589898360
        response = self.data.get_round_id

        self.assertEqual(response, expected)

    @unittest.expectedFailure
    def test_get_round_id_2(self):
        expected = 123456789
        response = self.data.get_round_id

        self.assertEqual(response, expected)

    def test_check_name_1(self):
        expected = (
            'Your chosen name is not unique. '
            'Please select an other one.'
        )
        response = self.data.check_name('a')

        self.assertEqual(response, expected)

    def test_check_name_2(self):
        expected = (
            'Your chosen name is not unique. '
            'Please select an other one.'
        )
        response = self.data.check_name('')

        self.assertEqual(response, expected)

    @unittest.expectedFailure
    def test_check_name_3(self):
        expected = ''
        response = self.data.check_name('b')

        self.assertEqual(response, expected)

    def test_check_name_4(self):
        expected = ''
        response = self.data.check_name('d')

        self.assertEqual(response, expected)

    def test_check_number_1(self):
        expected = ''
        response = self.data.check_number(1)

        self.assertEqual(response, expected)

    def test_check_number_2(self):
        expected = 'Please give a positive integer.'
        response = self.data.check_number(0)

        self.assertEqual(response, expected)

    def test_check_number_3(self):
        expected = 'Please give a positive integer.'
        response = self.data.check_number(-1)

        self.assertEqual(response, expected)

    def test_check_number_4(self):
        expected = ''
        response = self.data.check_number('1')

        self.assertEqual(response, expected)

    def test_check_number_5(self):
        expected = 'Please give a positive integer.'
        response = self.data.check_number('0')

        self.assertEqual(response, expected)

    def test_check_number_6(self):
        expected = 'Please give a positive integer.'
        response = self.data.check_number('-1')

        self.assertEqual(response, expected)

    def test_check_number_7(self):
        expected = 'Please give a positive integer.'
        response = self.data.check_number('a')

        self.assertEqual(response, expected)

    def test_add_vote_1(self):
        self.data.add_vote('d', 11)

        expected = {
            'players': [
                'a',
                'b',
                'd'
            ],
            'round_id': 1589898360,
            'votes': [
                5,
                6,
                11
            ]
        }
        response = self.data.get_active_game

        self.assertEqual(response, expected)

    def test_add_vote_2(self):
        self.data.add_vote('d', '11')

        expected = {
            'players': [
                'a',
                'b',
                'd'
            ],
            'round_id': 1589898360,
            'votes': [
                5,
                6,
                11
            ]
        }
        response = self.data.get_active_game

        self.assertEqual(response, expected)

    def test_get_winner_data_1(self):
        expected = ('a', 5)
        response = self.data.get_winner_data

        self.assertEqual(response, expected)

    def test_get_winner_data_2(self):
        self.data.add_vote('c', 2)
        self.data.add_vote('d', 2)

        expected = ('a', 5)
        response = self.data.get_winner_data

        self.assertEqual(response, expected)

    def test_get_winner_data_3(self):
        self.data.add_vote('c', 5)

        expected = ('b', 6)
        response = self.data.get_winner_data

        self.assertEqual(response, expected)

    def test_get_winner_data_4(self):
        self.data.add_vote('c', 5)
        self.data.add_vote('d', 6)

        expected = (None, None)
        response = self.data.get_winner_data

        self.assertEqual(response, expected)

    def test_close_round_1(self):
        expected = 1589898360
        response = self.data.close_round()

        self.assertEqual(response, expected)

    def test_close_round_2(self):
        self.data.close_round()

        expected = {}
        response = self.data.get_active_game

        self.assertEqual(response, expected)

    def test_close_round_3(self):
        self.data.close_round()

        expected = self.previous_games_mock_data.copy()
        del expected[1589898360]['end']

        response = self.data.get_previous_games

        self.assertEqual(response, expected)

    def test_get_previous_games(self):
        expected = self.previous_games_mock_data
        response = self.data.get_previous_games

        self.assertEqual(response, expected)


if __name__ == '__main__':
    unittest.main()

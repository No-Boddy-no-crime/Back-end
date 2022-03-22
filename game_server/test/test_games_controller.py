# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from game_server.models.error import Error  # noqa: E501
from game_server.models.game import Game  # noqa: E501
from game_server.test import BaseTestCase


class TestGamesController(BaseTestCase):
    """GamesController integration test stubs"""

    def test_create_game(self):
        """Test case for create_game

        Create a game
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/games',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_games(self):
        """Test case for list_games

        List all games
        """
        query_string = [('limit', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/games',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_show_game_by_id(self):
        """Test case for show_game_by_id

        Info for a specific game
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/games/{game_id}'.format(game_id='game_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

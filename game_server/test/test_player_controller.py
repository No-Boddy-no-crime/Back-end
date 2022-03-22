# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from game_server.models.error import Error  # noqa: E501
from game_server.models.player import Player  # noqa: E501
from game_server.models.rebuttal_card import RebuttalCard  # noqa: E501
from game_server.test import BaseTestCase


class TestPlayerController(BaseTestCase):
    """PlayerController integration test stubs"""

    def test_create_player(self):
        """Test case for create_player

        Join a game as a player
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/games/{game_id}/player'.format(game_id='game_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_make_accusation(self):
        """Test case for make_accusation

        Create a new player accusation
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/games/{game_id}/player/{player_id}/accusation'.format(game_id='game_id_example', player_id='player_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_make_suggestion(self):
        """Test case for make_suggestion

        Create a new player suggestion
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/games/{game_id}/player/{player_id}/suggestion'.format(game_id='game_id_example', player_id='player_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_move_player(self):
        """Test case for move_player

        Create a new player move
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/games/{game_id}/player/{player_id}/move'.format(game_id='game_id_example', player_id='player_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_show_player_by_id(self):
        """Test case for show_player_by_id

        Info for a specific player
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/games/{game_id}/player/{player_id}'.format(game_id='game_id_example', player_id='player_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from game_server.models.card_set import CardSet  # noqa: E501
from game_server.models.game import Game  # noqa: E501
from game_server.models.player import Player  # noqa: E501
from game_server.models.rebuttal_card import RebuttalCard  # noqa: E501
from game_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_create_game(self):
        """Test case for create_game

        Create a new game
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/game',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_player(self):
        """Test case for create_player

        Create a new player
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/game/{game_id}/player'.format(game_id='game_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_player(self):
        """Test case for find_player

        Find a player
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/game/{game_id}/player/{player_id}'.format(game_id='game_id_example', player_id='player_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_game_by_id(self):
        """Test case for get_game_by_id

        Find game by ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/game/{game_id}'.format(game_id='game_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_make_accusation(self):
        """Test case for make_accusation

        Make an accusation
        """
        query_string = [('accusation', game_server.CardSet())]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/game/{game_id}/player/{player_id}/accusation'.format(game_id='game_id_example', player_id='player_id_example'),
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_make_suggestion(self):
        """Test case for make_suggestion

        Make a suggestion
        """
        query_string = [('suggestion', game_server.CardSet())]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/game/{game_id}/player/{player_id}/suggestion'.format(game_id='game_id_example', player_id='player_id_example'),
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_move_player(self):
        """Test case for move_player

        Create a new player move
        """
        query_string = [('move', 3.4)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/game/{game_id}/player/{player_id}/move'.format(game_id='game_id_example', player_id='player_id_example'),
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

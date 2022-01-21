import unittest
import requests
from assertpy import *
from unittest.mock import *
from src.client import Client
import json


# id, firstname, surname, email, born
class TestMainClient(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @patch('src.client.requests.post')
    def test_add_client_mock_post_called(self, post_mock):
        post_mock.return_value.status_code = 201
        assert self.client.add_client(1, "Michal", "Bidz", "mbidz@example.com",
                                      "2001") == post_mock.return_value.json


    def test_add_new_client_success(self):
        with patch.object(requests, 'post') as post_mock:
            post_mock.return_value.status_code = 201
            post_mock.return_value.json = "success"
            assert self.client.add_client(1, "Michal", "Bidz", "mbidz@example.com",
                                          "2001") == post_mock.return_value.json

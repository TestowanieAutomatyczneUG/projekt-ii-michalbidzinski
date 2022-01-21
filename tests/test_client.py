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

    @patch.object(requests, 'post')
    def test_add_client_mock_post_called(self, post_mock):
        post_mock.return_value.status_code = 201
        assert self.client.add_client("1", "Michal", "Bidz", "mbidz@example.com",
                                      "2001") == post_mock.return_value.json

    def test_add_new_client_success(self):
        with patch.object(requests, 'post') as post_mock:
            post_mock.return_value.status_code = 201
            post_mock.return_value.json = "success"
            assert self.client.add_client("2", "Michal", "Bidz", "mbidz@example.com",
                                          "2001") == post_mock.return_value.json



    @patch.object(requests, 'post')
    def test_add_client_existing_eror(self, post_mock):
        post_mock.return_value.status_code = 400
        assert_that(self.client.add_client("1", "Michal", "Bidz", "mbidz@example.com",
                                      "2001")).is_equal_to("Client of this id already exists")

    def test_add_new_client_int(self):
        assert_that(self.client.add_client).raises(ValueError).when_called_with(1, 2, 3, 4, 5)

    def test_add_new_client_floats(self):
        assert_that(self.client.add_client).raises(ValueError).when_called_with(3.14, 1.23, 2.15, 0.7, 0.333)

    def test_add_new_client_array(self):
        assert_that(self.client.add_client).raises(ValueError).when_called_with([], [], [], [], [])

    def test_add_new_client_object(self):
        assert_that(self.client.add_client).raises(ValueError).when_called_with({}, {}, {}, {}, {})

    def test_add_new_client_int_as_id(self):
        assert_that(self.client.add_client).raises(ValueError).when_called_with(1, "Michal", "Bidz",
                                                                                "mbidz@example.com",
                                                                                "2001")

    def test_add_new_client_None(self):
        assert_that(self.client.add_client).raises(ValueError).when_called_with(None, None, None, None, None)

    @patch.object(requests, 'delete')
    def test_delete_client_success(self, mock_delete):
        id = "1"
        mock_delete.return_value.status_code = 201
        mock_delete.return_value.json = {"deleted": id}
        assert self.client.delete_client(id) == mock_delete.return_value.json

    def test_delete_client_success2(self):
        with patch.object(requests, 'delete') as mock_delete:
            id = "1"
            mock_delete.return_value.status_code = 201
            mock_delete.return_value.json = {"deleted": id}
            assert self.client.delete_client(id) == mock_delete.return_value.json

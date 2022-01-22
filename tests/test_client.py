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

    def test_add_client_existing_eror2(self):
        with patch.object(requests, 'post') as post_mock:
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

    def test_delete_client_wrong_int_id_type(self):
        assert_that(self.client.delete_client).raises(ValueError).when_called_with(1)

    def test_delete_client_wrong_flot_id_type(self):
        assert_that(self.client.delete_client).raises(ValueError).when_called_with(1.23)

    def test_delete_client_wrong_array_id_type(self):
        assert_that(self.client.delete_client).raises(ValueError).when_called_with([])

    def test_delete_client_not_existing(self):
        self.client.delete_client = MagicMock(
            return_value=400)
        response = self.client.delete_client("777")
        assert_that(response).is_equal_to(400)

    def test_delete_client_not_existing_2(self):
        self.client.delete_client = MagicMock(
            return_value=400)
        self.client.delete_client("777")
        self.client.delete_client.assert_called_with("777")

    def test_delete_client_connection_error(self):
        self.client.delete_client = MagicMock(side_effect=ConnectionError(
        ))
        assert_that(self.client.delete_client).raises(
            ConnectionError).when_called_with("1")

    def test_get_client_info_with_specified_id(self):
        id = "1"
        self.client.get_client_info = Mock()
        self.client.get_client_info.return_value = {'id': id, 'firstname': 'Michal', 'surname': 'Bidz',
                                                    'email': 'michalbidz@example.com', 'born': '2001'}
        response = self.client.get_client_info(id)
        self.assertEqual(response['firstname'], 'Michal')

    @patch.object(requests, 'get')
    def test_get_client_info_which_does_not_exisit_in_database(self, get_mock):
        get_mock.return_value.status_code = 404
        response = self.client.get_client_info('2')
        self.assertEqual(response, 'Such a client does not exists')
    @patch.object(requests, 'get')
    def test_get_client_info_server_error(self, get_mock):
        get_mock.return_value.status_code = 400
        response = self.client.get_client_info('2')
        self.assertEqual(response, 'Server error')

    def test_get_client_info_invalid_id_float(self):
        assert_that(self.client.get_client_info).raises(
            TypeError).when_called_with(5.3)

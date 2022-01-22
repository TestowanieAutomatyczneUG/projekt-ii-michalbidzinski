import unittest
import requests
from assertpy import *
from unittest.mock import *
from src.user import User
import json


# id, firstname, surname, email, born
class TestMainClient(unittest.TestCase):
    def setUp(self):
        self.temp = User()

    @patch.object(requests, 'post')
    def test_add_user_mock_post_called(self, post_mock):
        post_mock.return_value.status_code = 201
        assert self.temp.add_user("1", "Michal", "Bidz", "mbidz@example.com",
                                  "2001") == post_mock.return_value.json

    def test_add_new_user_success(self):
        with patch.object(requests, 'post') as post_mock:
            post_mock.return_value.status_code = 201
            post_mock.return_value.json = "success"
            assert self.temp.add_user("2", "Michal", "Bidz", "mbidz@example.com",
                                      "2001") == post_mock.return_value.json

    @patch.object(requests, 'post')
    def test_add_user_existing_eror(self, post_mock):
        post_mock.return_value.status_code = 400
        assert_that(self.temp.add_user("1", "Michal", "Bidz", "mbidz@example.com",
                                       "2001")).is_equal_to("Client of this id already exists")

    def test_add_user_existing_eror2(self):
        with patch.object(requests, 'post') as post_mock:
            post_mock.return_value.status_code = 400
            assert_that(self.temp.add_user("1", "Michal", "Bidz", "mbidz@example.com",
                                           "2001")).is_equal_to("Client of this id already exists")

    def test_add_new_usert_int(self):
        assert_that(self.temp.add_user).raises(ValueError).when_called_with(1, 2, 3, 4, 5)

    def test_add_new_user_floats(self):
        assert_that(self.temp.add_user).raises(ValueError).when_called_with(3.14, 1.23, 2.15, 0.7, 0.333)

    def test_add_new_user_array(self):
        assert_that(self.temp.add_user).raises(ValueError).when_called_with([], [], [], [], [])

    def test_add_new_user_object(self):
        assert_that(self.temp.add_user).raises(ValueError).when_called_with({}, {}, {}, {}, {})

    def test_add_new_user_int_as_id(self):
        assert_that(self.temp.add_user).raises(ValueError).when_called_with(1, "Michal", "Bidz",
                                                                            "mbidz@example.com",
                                                                            "2001")

    def test_add_new_user_None(self):
        assert_that(self.temp.add_user).raises(ValueError).when_called_with(None, None, None, None, None)

    @patch.object(requests, 'delete')
    def test_delete_user_success(self, mock_delete):
        id = "1"
        mock_delete.return_value.status_code = 201
        mock_delete.return_value.json = {"deleted": id}
        assert self.temp.delete_user(id) == mock_delete.return_value.json

    def test_delete_user_success2(self):
        with patch.object(requests, 'delete') as mock_delete:
            id = "1"
            mock_delete.return_value.status_code = 201
            mock_delete.return_value.json = {"deleted": id}
            assert self.temp.delete_user(id) == mock_delete.return_value.json

    def test_delete_user_wrong_int_id_type(self):
        assert_that(self.temp.delete_user).raises(ValueError).when_called_with(1)

    def test_delete_user_wrong_flot_id_type(self):
        assert_that(self.temp.delete_user).raises(ValueError).when_called_with(1.23)

    def test_delete_user_wrong_array_id_type(self):
        assert_that(self.temp.delete_user).raises(ValueError).when_called_with([])

    def test_delete_user_not_existing(self):
        self.temp.delete_client = MagicMock(
            return_value=400)
        response = self.temp.delete_client("777")
        assert_that(response).is_equal_to(400)

    def test_delete_user_not_existing_2(self):
        self.temp.delete_client = MagicMock(
            return_value=400)
        self.temp.delete_client("777")
        self.temp.delete_client.assert_called_with("777")

    def test_delete_user_connection_error(self):
        self.temp.delete_client = MagicMock(side_effect=ConnectionError(
        ))
        assert_that(self.temp.delete_client).raises(
            ConnectionError).when_called_with("1")

    def test_get_user_info_with_specified_id(self):
        id = "1"
        self.temp.get_user_info = Mock()
        self.temp.get_user_info.return_value = {'id': id, 'firstname': 'Michal', 'surname': 'Bidz',
                                                'email': 'michalbidz@example.com', 'born': '2001'}
        response = self.temp.get_user_info(id)
        self.assertEqual(response['firstname'], 'Michal')

    @patch.object(requests, 'get')
    def test_get_user_info_which_does_not_exisit_in_database(self, get_mock):
        get_mock.return_value.status_code = 404
        response = self.temp.get_user_info('2')
        self.assertEqual(response, 'Such a client does not exists')

    @patch.object(requests, 'get')
    def test_get_user_info_server_error(self, get_mock):
        get_mock.return_value.status_code = 400
        response = self.temp.get_user_info('2')
        self.assertEqual(response, 'Server error')

    def test_get_user_info_invalid_id_int(self):
        assert_that(self.temp.get_user_info).raises(
            TypeError).when_called_with(5)

    def test_get_user_info_invalid_id_float(self):
        assert_that(self.temp.get_user_info).raises(
            TypeError).when_called_with(5.3)

    def test_get_user_info_invalid_id_arr(self):
        assert_that(self.temp.get_user_info).raises(
            TypeError).when_called_with([])

    def test_get_user_info_invalid_id_obj(self):
        assert_that(self.temp.get_user_info).raises(
            TypeError).when_called_with({})

    def test_get_user_info_connection_error(self):
        self.temp.get_client = Mock(side_effect=ConnectionError)
        assert_that(self.temp.get_client).raises(
            ConnectionError).when_called_with('3')

    def test_get_all_users(self):
        self.temp.get_all_users = Mock()
        self.temp.get_all_users.return_value = (
            [{'id': '1',
              'firstname':
                  'Michal',
              'surname':
                  'Bidzinski',
              'email':
                  'michalbidzinski@gmail.com',
              'born': '2001'
              },
             {'id': '2',
              'name':
                  'Jarek',
              'surname':
                  'Pasha',
              'email':
                  'mich@gmail.com',
              'born': '2001'
              }])
        response = self.temp.get_all_users()
        self.assertEqual(response[1], {'email': 'mich@gmail.com', 'id': '2', 'name': 'Jarek', 'surname': 'Pasha', 'born': '2001'})

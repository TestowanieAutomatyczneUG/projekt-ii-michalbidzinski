import unittest
import requests
from assertpy import *
from unittest.mock import *
from src.user import User
import json

def request_mock(mockk, response):
    mockk.return_value = Mock(ok=True)
    mockk.return_value = response

class TestMainUser(unittest.TestCase):
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
                                       "2001")).contains("Client of this id already exists")

    @patch.object(requests, 'post', autospec=True)
    def test_add_user_existing_eror_autospec(self, post_mock):
        post_mock.return_value.status_code = 400
        assert_that(self.temp.add_user("1", "Michal", "Bidz", "mbidz@example.com",
                                       "2001")).is_equal_to_ignoring_case("CLIENT OF THIS ID ALREADY EXISTS")

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
        self.temp.delete_user = MagicMock(
            return_value=400)
        response = self.temp.delete_user("777")
        assert_that(response).is_equal_to(400)

    def test_delete_user_not_existing_2(self):
        self.temp.delete_user = MagicMock(
            return_value=400)
        self.temp.delete_user("777")
        self.temp.delete_user.assert_called_with("777")

    def test_delete_user_connection_error(self):
        self.temp.delete_user = MagicMock(side_effect=ConnectionError(
        ))
        assert_that(self.temp.delete_user).raises(
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
        self.temp.get_user_info = Mock(side_effect=ConnectionError)
        assert_that(self.temp.get_user_info).raises(
            ConnectionError).when_called_with('3')

    def test_get_user_no_such_id(self):
        self.temp.get_user_info = MagicMock(
            return_value=404)
        self.temp.get_user_info("777")
        self.temp.get_user_info.assert_called_with("777")

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
        self.assertEqual(response[1],
                         {'email': 'mich@gmail.com', 'id': '2', 'name': 'Jarek', 'surname': 'Pasha', 'born': '2001'})

    def test_update_user_eror_with_wrong_id(self):
        assert_that(self.temp.update_users).raises(ValueError).when_called_with(11.23, 'pepsi',
                                                                                'cola', '23@example.com', '2001')

    def test_update_user_eror_with_wrong_name(self):
        assert_that(self.temp.update_users).raises(ValueError).when_called_with('11', [],
                                                                                'cola', '23@example.com', '2001')

    def test_update_user_eror_with_wrong_surname(self):
        assert_that(self.temp.update_users).raises(ValueError).when_called_with('11', 'pepsi',
                                                                                12, '23@example.com', '2001')

    def test_update_user_eror_with_wrong_email(self):
        assert_that(self.temp.update_users).raises(ValueError).when_called_with('11', 'pepsi',
                                                                                'cola', 3.3, '2001')

    def test_update_user_eror_with_wrong_born_year(self):
        assert_that(self.temp.update_users).raises(ValueError).when_called_with('11', 'pepsi',
                                                                                'cola', "23213@example.com", 2001)

    def test_update_user(self):
        self.temp.update_users = Mock()
        self.temp.update_users.return_value = 'Some error'
        response = self.temp.update_users('2', 'mk', 'lqq', 'example@com.pl', '2001')
        assert_that(response).is_equal_to('Some error')

    def test_updatE_user_connection_error(self):
        self.temp.update_users = Mock(side_effect=ConnectionError)
        assert_that(self.temp.update_users).raises(
            ConnectionError).when_called_with(
            '2', 'mk', 'lqq', 'example@com.pl', '2001')

    @patch('src.user.requests.put')
    def test_update_user_mock(self, put_mock):
        request_mock(put_mock, FakeMock(200, {'id': 1}))
        self.temp.update_users( '2', 'mk', 'lqq', 'example@com.pl', '2001')
        put_mock.assert_called_once()

    @patch('src.user.requests.put')
    def test_update_user_21(self, put_mock):
        request_mock(put_mock, FakeMock(200, {'id': '1'}))
        response = self.temp.update_users( '1', 'mk', 'lqq', 'example@com.pl', '2001')
        assert_that(response['id']).is_equal_to('1')

    @patch('src.user.requests.put')
    def test_update_user_fake_mock(self, put_mock):
        request_mock(put_mock, FakeMock(404))
        response = self.temp.update_users('1', 'mk', 'lqq', 'example@com.pl', '2001')
        assert_that(response).is_equal_to("Some error")

    @patch('src.user.requests.put')
    def test_update_user_fake_mock_2(self, put_mock):
        request_mock(put_mock, FakeMock(404))
        self.temp.update_users('1', 'mk', 'lqq', 'example@com.pl', '2001')
        put_mock.assert_called_once()
    @patch('src.user.requests.put')
    def test_update_user_error_3(self, put_mock):
        request_mock(put_mock, FakeMock(521))
        response = self.temp.update_users('1', 'mk', 'lqq', 'example@com.pl', '2001')
        assert_that(response).contains('error')

    @patch('src.user.requests.post')
    def test_add_user_fake(self, post_mock):
        request_mock(post_mock, FakeMock(201, {'id': 1}))
        self.temp.add_user('1', 'mk', 'lqq', 'example@com.pl', '2001')
        post_mock.assert_called_once()

    @patch('src.user.requests.get')
    def test_get_non_existing_user_(self, get_mock):
        request_mock(get_mock, FakeMock(404))
        response = self.temp.get_user_info('3')
        self.assertEqual(response, 'Such a client does not exists')














class FakeMock(object):
    def __init__(self, status_code, json=None):
        self.status_code = status_code
        self.json = json

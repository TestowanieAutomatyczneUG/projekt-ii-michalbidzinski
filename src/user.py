import requests
class User:
    def __init__(self):
        self.url = "https://fakestoreapi.com/"
        self.create = "https://fakestoreapi.com/add"
        self.read = "https://fakestoreapi.com/get"
        self.update = "https://fakestoreapi.com/update"
        self.delete = "https://fakestoreapi.com/delete"
    def add_user(self,id, firstname, surname, email,born):
        if type(id) is not str:
            raise ValueError("id is not an str")
        if type(firstname) is not str:
            raise ValueError("firstname is not a string")
        if type(surname) is not str:
            raise ValueError("surname is not a string")
        if type(email) is not str:
            raise ValueError("email is not a string")
        if type(born) is not str:
            raise ValueError("born year is not a string")
        response = requests.post(self.create,
                                 data={'id': id ,'firstname': firstname, 'surname': surname, 'email': email,
                                       'born': born})
        if 200 <= response.status_code <= 299:
            return response.json
        if response.status_code == 400:
            return 'Client of this id already exists'
        else:
            return 'Server error'

    def delete_user(self, id):
        if not isinstance(id, str):
            raise ValueError("id must be type of str")
        response = requests.delete(self.delete, data={'id': id})
        if 200 <= response.status_code <= 299:
            return response.json
        if response.status_code == 404:
            return 'Such a client does not exists'
        else:
            return 'Server error'
    def get_user_info(self, id):
        if type(id) is not str:
            raise TypeError('id is not a str')
        response = requests.get(self.read + '/' + id)
        if 200 <= response.status_code <= 299:
            return response.json
        if response.status_code == 404:
            return 'Such a client does not exists'
        else:
            return 'Server error'

    def get_all_users(self):
        response = requests.get(self.url)
        return response

    def update_users(self, id, firstname, surname, email,born):
        if type(id) is not str:
            raise ValueError("id is not an str")
        if type(firstname) is not str:
            raise ValueError("firstname is not a string")
        if type(surname) is not str:
            raise ValueError("surname is not a string")
        if type(email) is not str:
            raise ValueError("email is not a string")
        if type(born) is not str:
            raise ValueError("born year is not a string")
        response = requests.put(self.update + '/' + id,
                                data={ 'firstname': firstname, 'surname': surname, 'email': email,
                                      'born': born})
        if 200 <= response.status_code <= 299:
            return response.json
        if response.status_code == 404:
            return 'Some error'

        else:
            return 'Server error'
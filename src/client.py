import requests
class Client:
    def __init__(self):
        self.create = "https://client.pl/add"
        self.read = "https:/client.pl/get"
        self.update = "https:/client.pl/update"
        self.delete = "https:/client.pl/update"
    def add_client(self,id, firstname, surname, email,born):
        if type(id) is not int:
            raise ValueError("id is not an int")
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
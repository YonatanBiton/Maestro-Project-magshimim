from pathlib import Path

class User():
    def __init__(self, json):
        self.from_json(json)


    def __init__(self, name, active, password, email):
        self.name = name
        self.active = active
        self.password = password
        self.email = email
    

    def to_json(self):
        return self.__dict__


    def from_json(self, json):
        self.name = json['name']
        self.active = json['active']
        self.password = json['password']
        self.email = json['email']


    def create_folder_if_no_exists(self, path):
        Path(path).mkdir(parents=True, exist_ok=True)
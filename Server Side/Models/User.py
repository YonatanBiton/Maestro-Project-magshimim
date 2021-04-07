from pathlib import Path

class User():
    def __init__(self, name, active=-1, password="", email=""):
        if active == -1 and password == "" and email == "":
            self.from_json(name)
        else:
            self.name = name
            self.active = active
            self.password = password
            self.email = email
    

    def to_json(self):
        return self.__dict__


    def from_json(self, json):
        self.name = str(json['name'])
        self.active = int(json['active'])
        self.password = str(json['password'])
        self.email = str(json['email'])


    def create_folder_if_no_exists(self, path):
        Path(f'Server Side/{path}/{self.name}').mkdir(parents=True, exist_ok=True)
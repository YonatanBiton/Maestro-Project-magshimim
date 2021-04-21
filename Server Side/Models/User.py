from pathlib import Path
from Core.Check import check_logged_user
import Config

class User():
    def __init__(self, name, active=-1, password="", email=""):
        if active == -1 and password == "" and email == "":
            check_logged_user(name)
            self.from_json(name['logged_user'])
        else:
            self.name = name
            self.active = active
            self.password = password
            self.email = email
        create_folder_if_no_exists(Config.UPLOAD_FOLDER)


    def to_json(self):
        return self.__dict__


    def from_json(self, json):
        self.name = str(json['name'])
        self.active = int(json['active'])
        self.password = str(json['password'])
        self.email = str(json['email'])


    def create_folder_if_no_exists(self, path):
        Path(f'Server Side/{path}/{self.name}').mkdir(parents=True, exist_ok=True)
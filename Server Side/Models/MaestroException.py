import random

class MaestroException(Exception):
    def __init__(self, error_message="", no_warning_message=False):
        self.error_message = get_random_warning_message() if error_message == "" and not no_warning_message else error_message

  
    def get_random_warning_message(self):
        warning_messages = [
            "Don't try to mess with us!",
            "You think you're so smart? Ha?"
        ]
        return random.choice(warning_messages) 
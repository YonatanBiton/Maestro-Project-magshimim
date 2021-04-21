from Models.MaestroException import MaestroException
from Models.Linker import Linker

ALLOWED_KEYBOARD_NUMBERS = "123456789"
ALLOWED_KEYBOARD_ENGLISH = "abcdefghijklmnopqrstuvwxyz"
ALLOWED_KEYBOARD_UPPER_ENGLISH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALLOWED_KEYBOARD_SPECIAL = "!@#$%^&*(){}[]\"'/.,;:+-"

def check_args_in_object(object, args):
    for arg in args:
        if arg not in object:
            raise MaestroException()


def check_signup_request(form):
    required_args = [
        'username',
        'password',
        'email',
        'confirmPassword'
    ]
    check_args_in_object(form, required_args)
    check_valid_email(form)
    check_password_confirmed(form)


def check_password_confirmed(form):
    check_args_in_object(form, ['password', 'confirmPassword'])
    if not form['password'] == form['confirmPassword']:
        raise MaestroException()


def check_valid_user_name(form):
    check_args_in_object(form, ['username']):
    check_allowed_characters(form['username'], allow_special=False)
    if len(form['username']) < 2 or len(form['username']) > 20:
        raise MaestroException()
    if(not Linker.is_user_name_unique(form['username'])):
        raise MaestroException('This user name already exists! Please try a different one.')


def check_valid_email(form):
    check_args_in_object(form, ['email']):
    if len(form['email']) < 1 or len(form['email']) > 254 or '@' not in form['email']:
        raise MaestroException()
    if(not Linker.is_email_unique(form['email'])):
        raise MaestroException('This email is already registered! Please try a different one or try logging in with the given email.')


def check_valid_password(form):
    check_args_in_object(form, ['password']):
    if len(form['password']) < 8 or len(form['password']) > 30:
        raise MaestroException()


def check_allowed_characters(string, allow_numbers=True, allow_english=True, allow_upper_english=True, allow_special=True):
    allowed_chars = ""
    if allow_numbers:
        allowed_chars.append(ALLOWED_KEYBOARD_NUMBERS)
    if allow_english:
        allowed_chars.append(ALLOWED_KEYBOARD_ENGLISH)
    if allow_upper_english:
        allowed_chars.append(ALLOWED_KEYBOARD_UPPER_ENGLISH)
    if allow_special:
        allowed_chars.append(ALLOWED_KEYBOARD_SPECIAL)
    for char in string:
        if char not in allowed_chars:
            raise MaestroException()
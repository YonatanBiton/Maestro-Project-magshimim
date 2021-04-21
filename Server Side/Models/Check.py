from Models.Linker import Linker
import random

ALLOWED_KEYBOARD_NUMBERS = "123456789"
ALLOWED_KEYBOARD_ENGLISH = "abcdefghijklmnopqrstuvwxyz"
ALLOWED_KEYBOARD_UPPER_ENGLISH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def are_args_in_form(form, args, error_output=[]):
    for arg in args:
        if arg not in form:
            error_output.append(get_random_warning_message())
            return False
    return True


def is_password_confirmed(form, error_output=[]):
    args_error = ""
    if not are_args_in_form(form, ['password', 'confirmPassword'], args_error):
        error_output.append(args_error)
        return False
    if not form['password'] == form['confirmPassword']:
        error_output.append(get_random_warning_message())
        return False
    return True


def is_user_name_valid(form, error_output=[]):
    args_error = ""
    if are_args_in_form(form, ['username'], args_error):
        error_output.append(args_error)
        return False
    if len(form['username']) < 2 or len(form['username']) > 20:
        error_output.append(get_random_warning_message())
        return False
    if(not Linker.is_user_name_unique(form['username'])):
        error_output.append(
            'This user name already exists! Please try a different one.')
        return False
    return True


def is_email_valid(form, error_output=[]):
    args_error = ""
    if are_args_in_form(form, ['email'], args_error):
        error_output.append(args_error)
        return False
    if len(form['email']) < 1 or len(form['email']) > 254 or '@' not in form['email']:
        error_output.append(get_random_warning_message())
        return False
    if(not Linker.is_email_unique(form['email'])):
        error_output.append(
            'This email already exists! Please try a different one.')
        return False
    return True


def is_password_valid(form, error_output=[]):
    args_error = ""
    if are_args_in_form(form, ['password'], args_error):
        error_output.append(args_error)
        return False
    if len(form['password']) < 8 or len(form['password']) > 30:
        error_output.append(get_random_warning_message())
        return False
    return True


def is_contains_number(text):
    if any((char in ALLOWED_KEYBOARD_NUMBERS) for char in text):
        pass


def get_random_warning_message():
    warning_messages = [
        "Don't try to mess with us!",
        "You think you're so smart? Ha?"
    ]
    return random.choice(warning_messages)

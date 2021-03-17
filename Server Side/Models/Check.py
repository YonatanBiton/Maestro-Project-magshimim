def are_args_in_form(form, args):
    for arg in args:
        if arg not in form:
            return False
    return True
import re


def UsernameValidator(val):
    return True
    # if re.match("^(?=.{3,20}$)(?![-_.0-9])(?!.*[_.-]{2})[a-zA-Z0-9._-]+(?<![_.-])$", val):
    # return True
    # else:
    # return False


def NameValidator(val):
    if re.match("^[a-zA-Z]+(\s[a-zA-Z]+)?$", val):
        return True
    else:
        return False


def EmailValidator(val):
    if re.match("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", val):
        return True
    else:
        return False

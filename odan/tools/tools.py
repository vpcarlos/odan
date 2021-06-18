import string
import secrets
import re
import os
import datetime


def gen_pass(lenght):
    password_characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(password_characters) for i in range(lenght))


def yesterday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime('%Y%m%d')

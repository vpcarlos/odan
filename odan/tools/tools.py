import string
import secrets
import subprocess
import re
import os
import datetime


def gen_pass(lenght):
    password_characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(password_characters) for i in range(lenght))


def run_command(command, stream_output=False, raise_error=True):
    """
    Run a Linux command.
    Here, check_output is used to retrieve the command output when
    an exception is raised.
    """
    try:
        if stream_output:
            subprocess.check_call(
                command, stderr=subprocess.STDOUT)
        else:
            subprocess.check_output(
                command, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        error_msg = "The '%s' command has failed" % e.cmd[0]
        if not stream_output:
            error_msg += " with the following output:\n %s" % e.output.decode(
                "utf-8"
            ).rstrip("\n")
        if raise_error:
            raise Warning(error_msg)
    except FileNotFoundError as error_msg:
        if raise_error:
            raise Warning(error_msg)
        return False
    

def yesterday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime('%Y%m%d')





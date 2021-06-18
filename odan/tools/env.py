import os
import json
import secrets
import string
import subprocess
from contextlib import contextmanager


def apt(command, packages=[], stream_output=False):
    run_command(
        ["sudo", "apt-get", "-y", command] + packages,
        stream_output=stream_output
    )


def apt_update(stream_output=False):
    apt("update", stream_output=stream_output)


def apt_install(packages, stream_output=False):
    apt("install", packages, stream_output=stream_output)


def apt_remove(packages, stream_output=False):
    apt("remove", packages, stream_output=stream_output)


def check(package, stream_output=False):
    return run_command([package, "--version"], raise_error=False)


def rm(file):
    run_command(["rm", "-rf", file])


def check_dir(directory):
    return os.path.isdir(directory)


@contextmanager
def cwd(new_cwd=None):
    """
    run commands in an especific workdir
    """
    new_cwd = new_cwd or os.environ.get('EXC_CWD')
    cwd = os.getcwd()
    try:
        yield os.chdir(new_cwd)
    finally:
        os.chdir(cwd)


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

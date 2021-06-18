import os
import json
import secrets
import string
from contextlib import contextmanager
from odan.tools.tools import run_command


def apt(command, packages=[]):
    run_command(["sudo", "apt-get", "-y", command] + packages)


def apt_update():
    apt("update")


def apt_install(packages):
    apt("install", packages)


def apt_remove(packages):
    apt("remove", packages)


def check(package):
    return run_command([package, "--version"], raise_error=False)


def rm(file):
    run_command(["rm", "-rf", file])


def check_dir(directory):
    return os.path.isdir(directory)


def create_dir(directory):
    return os.mkdir(directory)


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

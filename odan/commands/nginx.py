import click
import os
import getpass
from odan.templates.template import copy
from odan.tools.env import cwd, run_command, check

NGINX_DIR = '/opt/nginx'


@click.group(help='Manage Nginx')
def nginx():
    pass


@nginx.command()
@click.pass_context
def deploy(ctx):
    if check('docker') and check('docker-compose') and os.path.isdir(NGINX_DIR):
        ctx.invoke(network)
        with cwd(NGINX_DIR):
            run_command([
                'docker-compose',
                'up',
                '--build',
                '-d'
            ], stream_output=True)
            click.secho('Nginx deployed', fg='green')


@nginx.command()
def build():
    run_command(['sudo', 'mkdir', NGINX_DIR])
    run_command(['sudo', 'chown', getpass.getuser(), NGINX_DIR])
    with cwd(NGINX_DIR):
        copy('nginx', {}, render=False)


@nginx.command()
def network():
    if not check('docker'):
        click.secho('Docker not installed', fg='red')
        return False
    run_command(['docker', 'network', 'create', 'nginx-net'])
    click.secho('Network nginx-net deployed', fg='green')
    return True

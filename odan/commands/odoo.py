import click
import uuid
import requests
from odan.templates.template import copy
from odan.tools.tools import *
from odan.tools.env import *
from datetime import date
from odan.commands import nginx


@click.group(help='Manage odoo')
def odoo():
    pass


@odoo.command(help='Deploy a new odoo instance')
@click.option(
    '--name',
    prompt='Project name',
    required=True,
    default='odoo-'+str(uuid.uuid4())[:4]
)
@click.option(
    '--branch',
    prompt='Your name please',
    type=click.Choice(['14.0', '13.0', '12.0', '11.0']),
    required=True,
    default='14.0'
)
@click.option(
    '--domain',
    prompt='Enter a domain',
    required=False,
    default='demo.com'
)
@click.option(
    '--email',
    prompt='Enter a email',
    required=False,
    default='demo@demo.com'
)
@click.option(
    '--admin-pass',
    prompt='Create an admin password',
    required=True,
    default=gen_pass(10)
)
@click.option(
    '--pg-pass',
    prompt='Create a postgress password',
    required=True,
    default=gen_pass(10)
)
@click.option(
    '--release',
    prompt='Write a release in format YYYYMMDD',
    required=True,
    default=yesterday()
)
@click.pass_context
def deploy(ctx, name, branch, domain, email, admin_pass, pg_pass, release):
    ctx.invoke(nginx.deploy)
    ctx.forward(
        build,
        name=name,
        branch=branch,
        domain=domain,
        email=email,
        admin_pass=admin_pass,
        pg_pass=pg_pass,
        release=release
    )

    with cwd(name):
        run_command(['docker-compose', 'up', '--build', '-d'])


@odoo.command(
    help='Build new odoo project'
)
@click.option(
    '--name',
    prompt='Project name',
    required=True,
    default='odoo-'+str(uuid.uuid4())[:4]
)
@click.option(
    '--branch',
    prompt='Your name please',
    type=click.Choice(['14.0', '13.0', '12.0', '11.0']),
    required=True,
    default='14.0'
)
@click.option(
    '--domain',
    prompt='Enter a domain',
    required=False,
    default='demo.com'
)
@click.option(
    '--email',
    prompt='Enter a email',
    required=False,
    default='demo@demo.com'
)
@click.option(
    '--admin-pass',
    prompt='Create an admin password',
    required=True,
    default=gen_pass(10)
)
@click.option(
    '--pg-pass',
    prompt='Create a postgress password',
    required=True,
    default=gen_pass(10)
)
@click.option(
    '--release',
    prompt='Write a release in format YYYYMMDD',
    required=True,
    default=yesterday()
)
@click.pass_context
def build(ctx, name, branch, domain, email, admin_pass, pg_pass, release):
    data = {
        'branch': branch,
        'name': name,
        'domain': domain,
        'pg_pass': pg_pass,
        'admin_pass': admin_pass,
        'release': release,
        'sha1': ctx.invoke(sha, branch=branch, release=release)
    }
    os.mkdir(name)
    with cwd(name):
        copy(f'odoo/{branch}', data)


@odoo.command(help='Get sha1 from a odoo branch release')
@click.option(
    '--branch',
    prompt='Chose a branch',
    type=click.Choice(['14.0', '13.0', '12.0', '11.0']),
    required=True,
    default='14.0'
)
@click.option(
    '--release',
    prompt='Write a release in format YYYYMMDD',
    required=True,
    default=yesterday()
)
def sha(branch, release):
    url = f'https://nightly.odoo.com/14.0/nightly/deb/odoo_{branch}.{release}_amd64.changes'
    f = requests.get(url)

    sha_list = f.text.split('\n')
    for index, info in enumerate(sha_list):
        if f'odoo_{branch}.{release}_all.deb' in info:
            sha = sha_list[index].lstrip().split(' ')[0]
            click.secho(
                f'Sha1 for {branch}/{release} found: {sha}', fg='green')
            return sha

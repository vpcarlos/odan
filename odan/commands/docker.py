import click
from odan.tools.env import *
from odan.tools.tools import *


@click.group(help='Manage docker')
def docker():
    pass


@click.option('--force', is_flag=True, help='Force instalation')
@docker.command(help='Install docker')
@click.pass_context
def install(ctx, force):
    # Install curl in order to get docker
    if not check("curl"):
        click.secho('Installing curl...', fg='green')
        apt_update()
        apt_install(["curl"], stream_output=True)

    if force:
        ctx.invoke(uninstall)
    # Check if docker is already installed
    if check("docker"):
        click.secho('Docker already installed!', fg='yellow')
        return

    # Install docker
    click.secho('Installing docker...')

    # Get sh script for instalation and storing it in a temp file
    run_command([
        "curl",
        "-sL",
        "get.docker.com",
        "-o",
        "docker.sh"
    ])

    # Executing sh script
    run_command([
        "sh",
        "docker.sh",
    ], stream_output=True)

    # Removing temp file
    rm("docker.sh")

    # Crear docker group and user
    create_docker_group()
    add_user_to_group()


@docker.command(help='Reinstall docker')
@click.pass_context
def reinstall(ctx):
    if ctx.invoke(uninstall):
        ctx.invoke(install)


@docker.command(help='Uninstall docker')
def uninstall():
    if not check('docker'):
        click.secho("Docker is not installed", fg='red')
        return False
    if click.confirm('Are you sure you want to uninstall Docker?'):
        click.secho('Removing docker...', fg='yellow')
        apt_purge([
            'docker',
            'docker-ce',
            'docker-ce-cli',
            'containerd.io'
        ], stream_output=True)
        click.secho('Docker uninstaled', fg='green')
        return True
    return False


def create_docker_group():
    run_command(["groupadd", "docker"])


def add_user_to_group():
    run_command(["usermod", "-aG", "docker", "${SUDO_USER:-$USER}"])

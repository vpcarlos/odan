import click
import os

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')


class Odan(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py') and filename != '__init__.py':
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"odan.commands.{name}", None, None, [name])
        except ImportError:
            return

        return getattr(mod, name)


odan = Odan(help='Odoo deployment and network')

if __name__ == '__main__':
    odan()

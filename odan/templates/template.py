import os
import shutil
from jinja2 import Template, PackageLoader, Environment
from odan.tools.env import cwd


loader = PackageLoader('odan', 'templates')
env = Environment(loader=loader)


def copy(src, data, render=True):

    current_dir = os.path.dirname(os.path.realpath(__file__))

    template_dir = os.path.join(current_dir, src)
    for root, dirs, files in os.walk(template_dir):

        # checking if it is a file
        for name in files:
            rel_tmpl_dir = os.path.join(root.replace(template_dir, ''))
            rel_current_dir = os.path.join(root.replace(current_dir, ''), name)
            if rel_tmpl_dir:
                try:
                    os.makedirs(os.path.join('.' + rel_tmpl_dir))
                except FileExistsError:
                    pass
            if render:
                with open(os.path.join('.' + rel_tmpl_dir, name), 'w') as f:

                    _template = env.get_template(rel_current_dir)
                    f.write(_template.render(data))
            else:
                shutil.copy(os.path.join(root, name),
                            os.path.join('.' + rel_tmpl_dir, name))

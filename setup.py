from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='odan',
    version='0.0.1',
    description='Odoo deployment and network',
    author='Carlos Valdivia',
    author_email='vpcarlos97@gmail.com',
    url='https://github.com/vpcarlos/odan',
    license='unlicensed',
    py_modules=['odan'],
    package_dir={'': 'src'},
    classifiers=[
        'Programing Language :: Python :: 3',
        'Programing Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3.0'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'click>=7.0'
    ],
    extras_require={
        'dev': [
            'pytest >=3.7'
        ]
    }
)

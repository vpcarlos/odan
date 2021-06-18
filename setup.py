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
    include_package_data=True,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'click>=7.0',
        'docker-compose>=1.29.2'
    ],
    extras_require={
        'dev': [
            'pytest >=3.7'
        ]
    },
    entry_points='''
        [console_scripts]
        odan=odan.main:odan
    '''
)

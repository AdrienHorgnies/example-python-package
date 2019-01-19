from setuptools import setup

setup(
    name='sql_check',
    version='1.0',
    description='A module to run billing check, write reports and inspect results',
    author='Adrien Horgnies',
    author_email='aHorgnies@altissia.org',
    packages=['sql_check'],
    install_requires=['mock'],
)

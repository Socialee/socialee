"""This file is mainly here for Heroku to detect it as a Python project."""
from setuptools import setup, find_packages

setup(name='Socialee',
      version='0.1',
      description='Socialee',
      url='http://github.com/Socialee/socialee',
      author='Daniel Hahler',
      author_email='socialee@thequod.de',
      license='Proprietary License',
      packages=find_packages(),
      zip_safe=False)

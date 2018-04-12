#!/usr/bin/env python
import os
from setuptools import setup
from django_dropbox_storage import version


def get_packages():
    # setuptools can't do the job :(
    packages = []
    for root, dirnames, filenames in os.walk('django_dropbox_storage'):
        if '__init__.py' in filenames:
            packages.append(".".join(os.path.split(root)).strip("."))

    return packages

requires = [
    'django>=1.11',
    'dropbox>=8.0.0',
]

setup(name='django-dropbox-storage',
      version=version,
      description='A Dropbox Storage for your Django apps',
      author=u'Emanuele Bertoldi',
      author_email='emanuele.bertoldi@gmail.com',
      url='https://github.com/zuck/django-dropbox-storage',
      packages=get_packages(),
      install_requires=requires,
)

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

project_url = 'https://github.com/zuck/django-dropbox-storage'

setup(
    name='django-dropbox-storage',
    version=version,
    description='A Dropbox Storage for your Django apps',
    author=u'Emanuele Bertoldi',
    author_email='emanuele.bertoldi@gmail.com',
    url=project_url,
    download_url=project_url + '/archive/' + version + '.tar.gz',
    packages=get_packages(),
    install_requires=requires,
    keywords = ['django', 'storage', 'dropbox'],
)

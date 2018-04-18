from __future__ import absolute_import, unicode_literals

import json
from base64 import b64encode

from celery import task

import requests


def __get_credentials():
    with open('.loader_credentials.json', 'r') as f:
        read_data = f.read()

    read_data = json.loads(read_data)
    username = read_data['username']
    password = read_data['password']

    utf_8_authorization = "{username}:{password}".format(
        username=username, password=password
    ).encode()

    return "Basic " + b64encode(utf_8_authorization).decode("ascii")


@task()
def get_parliamentarians():
    url = "http://loader:3500/"
    data = "{\n\"task\": \"get_parliamentarians\"\n}"

    requests.post(
        url=url,
        data=data,
        headers={
            "content-type": "application/json",
            "Authorization": __get_credentials()
        }
    )


@task()
def get_propositions():
    url = "http://loader:3500/"
    data = "{\n\"task\": \"get_propositions\"\n}"

    requests.post(
        url=url,
        data=data,
        headers={
            "content-type": "application/json",
            "Authorization": __get_credentials()
        }
    )

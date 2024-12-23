from unittest import TestCase
from brainbox.framework import Fork, ApiUtils
import requests
import time
from flask import Flask

class Server:
    def __call__(self):
        app = Flask("TestApp")
        app.add_url_rule('/', view_func=self.index, methods=['GET'])
        app.run('127.0.0.1', 8099)

    def index(self):
        return 'OK'

class ForkTestCase(TestCase):
    def test_fork(self):
        Fork(Server()).start()
        ApiUtils.wait_for_reply('http://127.0.0.1:8099', 1)

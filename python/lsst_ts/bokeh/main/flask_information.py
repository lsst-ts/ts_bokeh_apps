from typing import Dict, List

from flask import Flask


class FlaskInformation:

    def __init__(self, server: str, port: int, flask_app: Flask):
        self._app = flask_app
        self._server = server
        self._port = port
        self._applications = {}
        self._data_sources = {}

    @property
    def flask_app(self):
        return self._app

    @property
    def server(self):
        return self._server

    @property
    def port(self):
        return self._port

    @property
    def applications(self) -> Dict:
        return self._applications

    def add_application(self, name: str, application):
        self._applications[name] = application

    def add_data_source(self, name: str):
        self._data_sources[name] = ""
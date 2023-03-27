from typing import Dict, List, Any

from flask import Flask


class ServerInformation:

    def __init__(self, bokeh_server: str, bokeh_port: int, flask_app: Flask):
        """
        :param server: Bokeh server host
        :param port: Bokeh server port
        :param flask_app: Flask Application to add REST API datapoints
        """
        self._app = flask_app
        self._bokeh_server = bokeh_server
        self._bokeh_port = bokeh_port
        self._applications = {}
        self._server_information = {}
        self._bokeh_allowed_connections = []

    @property
    def flask_app(self):
        return self._app

    @property
    def bokeh_server(self):
        return self._bokeh_server

    @property
    def bokeh_port(self):
        return self._bokeh_port

    def add_bokeh_allow_websocket_origin(self, server_port: str):
        self._bokeh_allowed_connections.append(server_port)

    @property
    def bokeh_allowed_websocket_origin(self) -> List[str]:
        return self._bokeh_allowed_connections[:]
    @property
    def applications(self) -> Dict:
        return self._applications

    def add_application(self, name: str, application):
        self._applications[name] = application

    def add_applications_information(self, identifier, value):
        self._server_information[identifier] = value

    def get_application_information(self, identifier: str) -> Any:
        return self._server_information[identifier]
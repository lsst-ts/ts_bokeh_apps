from typing import Dict, List, Any, Callable

from bokeh.document import Document
from flask import Flask


class ServerInformation:

    def __init__(self, flask_app: Flask):
        """
        :param flask_app: Flask Application to add REST API datapoints
        """
        self._app = flask_app
        self._applications = {}
        self._server_information = {}
        self._allowed_websocket_connections = []

    @property
    def flask_app(self):
        return self._app

    def add_allowed_websocket_origin(self, server_port: str):
        self._allowed_websocket_connections.append(server_port)

    @property
    def allowed_websocket_origin(self) -> List[str]:
        return self._allowed_websocket_connections[:]
    @property
    def applications(self) -> Dict:
        return self._applications

    def add_application(self, name: str, application: Callable[[Document], None]):
        self._applications[name] = application

    def add_application_information(self, identifier: str, value: Any):
        self._server_information[identifier] = value

    def get_application_information(self, identifier: str) -> Any:
        return self._server_information[identifier]
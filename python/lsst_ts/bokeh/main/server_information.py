from typing import Callable, Dict, List, Union

from bokeh.document import Document
from flask import Flask


class ServerInformation:
    def __init__(self, flask_app: Flask) -> None:
        """
        :param flask_app: Flask Application to add REST API datapoints
        """
        self._app = flask_app
        self._applications = {}  # type: Dict[str, Callable[[Document], None]]
        self._server_information = {}  # type:  Dict[str, Union[float, str]]
        self._allowed_websocket_connections = []  # type: List[str]

    @property
    def flask_app(self) -> Flask:
        return self._app

    def add_allowed_websocket_origin(self, server_port: str) -> None:
        self._allowed_websocket_connections.append(server_port)

    @property
    def allowed_websocket_origin(self) -> List[str]:
        return self._allowed_websocket_connections[:]

    @property
    def applications(self) -> Dict[str, Callable[[Document], None]]:
        return self._applications

    def add_application(
        self, name: str, application: Callable[[Document], None]
    ) -> None:
        self._applications[name] = application

    def add_application_information(
        self, identifier: str, value: Union[float, str]
    ) -> None:
        self._server_information[identifier] = value

    def get_application_information(self, identifier: str) -> Union[float, str]:
        return self._server_information[identifier]

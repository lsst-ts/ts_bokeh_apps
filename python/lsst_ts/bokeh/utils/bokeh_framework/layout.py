import os
from abc import ABC, abstractmethod
import urllib

from bokeh.io import show

from lsst_ts.bokeh.utils.bokeh_framework.data_aggregator import DataAggregator, VoidDataAggregator
from lsst_ts.bokeh.utils.bokeh_framework.interaction import Interaction, VoidInteraction

from typing import TYPE_CHECKING, Optional

from lsst_ts.library.utils.logger import get_logger

if TYPE_CHECKING:
    from bokeh.models import UIElement  # type: ignore
    from bokeh.document import Document

# T = TypeVar('T', bound='DataAggregator')
# I = TypeVar('I', bound=Interaction)

_log = get_logger("bokeh_framework.layout")

class Layout(ABC):

    def __init__(self, interaction: Interaction = VoidInteraction(),
                 data_aggregator: DataAggregator = VoidDataAggregator()) -> None:
        super().__init__()
        assert (isinstance(interaction, Interaction))
        assert (isinstance(data_aggregator, DataAggregator))
        self._interaction = interaction
        self._data_aggregator = data_aggregator

    @abstractmethod
    def define(self) -> 'UIElement':
        """
        Abstract method. Framework user should inherit from Layout
        and overwrite this method, where basically will
        define all the Element and their relation and return it.
        :return: Bokeh UIElement to be served or integrated into a Notebook
        """
        raise NotImplementedError()

    def create(self) -> 'UIElement':
        """
        Create the full layout (using the define method overwritten)
         and also create data_aggregation and interaction
        to be used inside the Bokeh application
        :return:
        """
        ui_element = self.define()
        _log.info("Setting up Application Interaction")
        self._interaction.setup(self)
        _log.info("Setting up Data")
        self._data_aggregator.setup(self)
        return ui_element

    def notebook_show(self, notebook_url: Optional[str] = None):
        _log.info("Showing application")
        if notebook_url is not None:
            assert(notebook_url != "")
            show(self.deploy, notebook_url=notebook_url)
        else:
            show(self.deploy, notebook_url=Layout._jupyter_hub_url)

    def deploy(self, doc: 'Document') -> None:
        """
        Deploy the application into a bokeh document
        :param doc: Bokeh document where the bokeh application will be deployed
        :return: None
        """
        _log.info("Deploying application")
        element = self.create()
        doc.add_root(element)

    def show(self, notebook_url: str = "") -> None:
        """
        :param notebook_url: String with the URL path to
        the notebook where application will be shown (No interaction available)
        :return: None
        """
        _log.info("Showing application")
        element = self.create()
        show(element, notebook_url=notebook_url)

    @staticmethod
    def _jupyter_hub_url(port: int):
        """
            Callable to configure Bokeh's show method when a proxy must be
            configured.
            If port is None we're asking about the URL
            for the origin header.
        """
        base_url = os.environ['EXTERNAL_INSTANCE_URL']
        host = urllib.parse.urlparse(base_url).netloc
        # If port is None we're asking for the URL origin
        # so return the public hostname.
        if port is None:
            return host
        service_url_path = os.environ['JUPYTERHUB_SERVICE_PREFIX']
        proxy_url_path = 'proxy/%d' % port
        user_url = urllib.parse.urljoin(base_url, service_url_path)
        full_url = urllib.parse.urljoin(user_url, proxy_url_path)
        return full_url

    def _set_interaction(self, interaction: Interaction) -> None:
        """
        Setter for the interaction
        :param interaction: Interaction instance
        :return: None
        """
        assert (isinstance(interaction, Interaction))
        self._interaction = interaction

    @property
    def data_aggregator(self) -> DataAggregator:
        """
        :return:
        """
        return self._data_aggregator

    @data_aggregator.setter
    def data_aggregator(self, data_aggregator: DataAggregator) -> None:
        """
        Setter for the data aggregation
        :param data_aggregator: DataAggregation instance
        :return: None
        """
        assert (isinstance(data_aggregator, DataAggregator))
        self._data_aggregator = data_aggregator

    # Unlike data_aggregator Interaction should
    # not be accessed from outside the class
    interaction = property(None, _set_interaction)

#Skeleton to build an application

from bokeh.document import Document

from lsst_ts.bokeh.main.server_information import ServerInformation


def initialize_main_app(server_information: ServerInformation):
    """
    :param server_information:
    :return:
    """
    def create_application(doc: Document):
        """
        :param doc:
        :return:
        """
        pass
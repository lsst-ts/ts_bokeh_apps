from typing import List, Protocol

import lsst.daf.butler as dafButler

class QueryReturn(Protocol):

    def toDict(self):
        pass

class ButlerDataController:

    def __init__(self, configuration: str = "LATISS", instrument: str = "LATISS", collections: str = "LATISS/raw/all"):
        self._butler = dafButler.Butler(configuration, instrument=instrument, collections=collections)

    def query_record(self, location: str, where_clausule: str) -> List[Protocol[QueryReturn]]:
        return [register for register in self._butler.registry.queryDimensionRecords(location, where=where_clausule)]


if __name__ == '__main__':
    pass
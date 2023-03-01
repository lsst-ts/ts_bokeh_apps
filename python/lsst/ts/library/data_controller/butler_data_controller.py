
import lsst.daf.butler as dafButler

class ButlerDataController:

    def __init__(self):
        self._butler = dafButler.Butler("LATISS", instrument="LATISS", collections="LATISS/raw/all")

    def query_record(self):
        pass
        # t = [
        #     r
        #     for r in self.butler.registry.queryDimensionRecords(
        #         "exposure",
        #         where=f"exposure.day_obs = {self.day_obs} and exposure.seq_num = {self.seq_num}",
        #     )
        # ]
        # if len(t) > 1:
        #     raise RuntimeError(
        #         f"Something went wrong. We only expected one record for {self.day_obs}-{self.seq_num}"
        #     )

if __name__ == '__main__':
    pass
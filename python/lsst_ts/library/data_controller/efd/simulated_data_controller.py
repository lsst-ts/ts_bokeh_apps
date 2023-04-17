from datetime import datetime, timedelta
from typing import List

import pandas as pd
from pandas.core.interchange import dataframe

from lsst_ts.library.data_controller.efd.data_controller import DataController
from lsst_ts.library.utils.date_interval import DateInterval


def get_dumped_log_information(i):
    return [
            (0, datetime.strptime("{} 00:41:18.101000+00:00".format((datetime.today() + timedelta(-1 * ((2 * i) + 1))).strftime("%Y-%m-%d")),'%Y-%m-%d %H:%M:%S.%f%z'), 42658887, "Read historical data in 0.03 sec"),
            (0, datetime.strptime("{} 08:55:39.390000+00:00".format((datetime.today() + timedelta(-1 * ((2 * i) + 1))).strftime("%Y-%m-%d")),'%Y-%m-%d %H:%M:%S.%f%z'), 871602426, " [atdometrajectory]::[<State.ENABLED: 2>, <State.DISABLED: 1>, <State.STANDBY: 5>]"),
            (0, datetime.strptime("{} 08:55:39.392000+00:00".format((datetime.today() + timedelta(-1 * ((2 * i) + 1))).strftime("%Y-%m-%d")),'%Y-%m-%d %H:%M:%S.%f%z'), 871602426, " All components in <State.STANDBY: 5>."),
            (0, datetime.strptime("{} 08:58:16.715000+00:00".format((datetime.today() + timedelta(-1 * ((2 * i) + 1))).strftime("%Y-%m-%d")),'%Y-%m-%d %H:%M:%S.%f%z'), 871602426, """ Unable to transition atcamera to <State.STANDBY: 5> NoneType: None
                            .
                            Traceback (most recent call last):
                            File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/csc_utils.py', line 161, in set_summary_state
                                await cmd.start(timeout=timeout)
                              File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/topics/remote_command.py', line 483, in start
                                return await cmd_info.next_ackcmd(timeout=timeout)
                              File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/topics/remote_command.py', line 201, in next_ackcmd
                                raise base.AckError(msg='Command failed', ackcmd=ackcmd)
                            lsst.ts.salobj.base.AckError: msg='Command failed', ackcmd=(ackcmd private_seqNum=1668433851, ack=<SalRetCode.CMD_FAILED: -302>, error=0, result='Error : java.util.concurrent.TimeoutException: Timed out after 1000 milliseconds.\n\tTimed out after 1000 milliseconds.\n\tCould not get reply within the specified timeout of 1000 milliseconds for command Command(TokenizedCommand) getDistributionInfo to ats')
                        
                            The above exception was the direct cause of the following exception:
                        
                            Traceback (most recent call last):
                              File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/csc_utils.py', line 163, in set_summary_state
                                raise RuntimeError(
                            RuntimeError: Error on cmd=cmd_standby, initial_state=2: msg='Command failed', ackcmd=(ackcmd private_seqNum=1668433851, ack=<SalRetCode.CMD_FAILED: -302>, error=0, result='Error : java.util.concurrent.TimeoutException: Timed out after 1000 milliseconds.\n\tTimed out after 1000 milliseconds.\n\tCould not get reply within the specified timeout of 1000 milliseconds for command Command(TokenizedCommand) getDistributionInfo to ats')
                            """),
            (0, datetime.strptime("{} 15:10:46.820000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 100006, "Configure started"),
            (0, datetime.strptime("{} 15:09:09.056000+00:00".format((datetime.today() + timedelta(-1 * ((2 * i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 7, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 15:18:21.314000+00:00".format((datetime.today() + timedelta(-1 * ((2 * i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 42658887, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 15:25:42.776000+00:00".format((datetime.today() + timedelta(-1 * ((2 * i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 42658887, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 18:10:58.469000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 100000, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 19:58:25.817000+00:00".format((datetime.today() + timedelta(-1 * ((2 * i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 7, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 20:40:31.318000+00:00".format((datetime.today() + timedelta(-1 * ((2 * i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 42658886, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 20:40:57.294000+00:00".format((datetime.today() + timedelta(-1 * ((2 * i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 42658886, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 20:52:48.404000+00:00".format((datetime.today() + timedelta(-1 * ((2 * i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 100001, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 20:52:48.412000+00:00".format((datetime.today() + timedelta(-1 * ((2 * i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 100001, "Configure started"),
            (0, datetime.strptime("{} 21:00:38.757000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 42658887, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 21:11:15.010000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 -- Move to Zero- Starting time: {} 21:10:38.010131 UTC"),
            (0, datetime.strptime("{} 21:11:24.499000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 Compensation mode test Step 17- Starting time: {} 21:10:47.498767 UTC"),
            (0, datetime.strptime("{} 21:12:03.801000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 Compensation mode test Step 17- Starting time: {} 21:11:26.801265 UTC"),
            (0, datetime.strptime("{} 21:32:15.953000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 42658887, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 21:33:10.677000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 42658887, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 21:33:53.638000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'),  42658887, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 21:35:47.396000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'),  42658887, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 21:59:31.119000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'),  42658887, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 22:08:06.152000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'),  42658887, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 22:11:02.459000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'),  42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 -- Move to Zero- Starting time: {} 22:10:25.456788 UTC"),
            (0, datetime.strptime("{} 22:11:07.295000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'),  42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 Compensation mode test Step 17- Starting time: {} 22:10:30.295440 UTC"),
            (0, datetime.strptime("{} 22:11:27.149000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'),  42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 Compensation mode test Step 17- Starting time: {} 22:10:50.148659 UTC"),
            (0, datetime.strptime("{} 22:11:41.007000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'),  42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 Compensation mode test Step 17- Starting time: {} 22:11:04.006157 UTC"),
            (0, datetime.strptime("{} 22:36:45.345000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'),  42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 -- Move to Zero- Starting time: {} 22:36:08.344298 UTC"),
            (0, datetime.strptime("{} 22:58:04.434000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 100002, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 23:00:47.682000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'),  7, "Read historical data in 0.00 sec"),
            (0, datetime.strptime("{} 23:10:06.039000+00:00".format((datetime.today() + timedelta(-1*((2*i) + 1))).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'),  42658887, "Read historical data in 0.00 sec"),

            (0, datetime.strptime("{} 01:34:08.936000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 770156871, "Exception from latiss_take_sequence()"),
            (0, datetime.strptime("{} 01:34:08.937000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 770156871, "Latiss_acquire_and_take_sequence script completed"),
            (0, datetime.strptime("{} 08:55:39.392000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 871602426, " All components in <State.STANDBY: 5>."),
            (0, datetime.strptime("{} 08:58:16.724000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 871602426, "[atheaderservice]::[<State.ENABLED: 2>, <State.DISABLED: 1>, <State.STANDBY: 5>]"),
            (0, datetime.strptime("{} 08:58:16.715000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 871602426, """Unable to transition atcamera to <State.STANDBY: 5> NoneType: None
                            .
                            Traceback (most recent call last):
                              File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/csc_utils.py', line 161, in set_summary_state
                                await cmd.start(timeout=timeout)
                              File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/topics/remote_command.py', line 483, in start
                                return await cmd_info.next_ackcmd(timeout=timeout)
                              File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/topics/remote_command.py', line 201, in next_ackcmd
                                raise base.AckError(msg='Command failed', ackcmd=ackcmd)
                            lsst.ts.salobj.base.AckError: msg='Command failed', ackcmd=(ackcmd private_seqNum=1668433851, ack=<SalRetCode.CMD_FAILED: -302>, error=0, result='Error : java.util.concurrent.TimeoutException: Timed out after 1000 milliseconds.\n\tTimed out after 1000 milliseconds.\n\tCould not get reply within the specified timeout of 1000 milliseconds for command Command(TokenizedCommand) getDistributionInfo to ats')

                            The above exception was the direct cause of the following exception:

                            Traceback (most recent call last):
                              File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/csc_utils.py', line 163, in set_summary_state
                                raise RuntimeError(
                            RuntimeError: Error on cmd=cmd_standby, initial_state=2: msg='Command failed', ackcmd=(ackcmd private_seqNum=1668433851, ack=<SalRetCode.CMD_FAILED: -302>, error=0, result='Error : java.util.concurrent.TimeoutException: Timed out after 1000 milliseconds.\n\tTimed out after 1000 milliseconds.\n\tCould not get reply within the specified timeout of 1000 milliseconds for command Command(TokenizedCommand) getDistributionInfo to ats')
                            """""),
            (0, datetime.strptime("{} 08:58:16.720000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 871602426, "[atspectrograph]::[<State.ENABLED: 2>, <State.DISABLED: 1>, <State.STANDBY: 5>]"),
            (0, datetime.strptime("{} 08:58:16.720000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 871602426, "[atspectrograph]::[<State.ENABLED: 2>, <State.DISABLED: 1>, <State.STANDBY: 5>]"),
            (0, datetime.strptime("{} 08:58:16.724000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 871602426, "[atheaderservice]::[<State.ENABLED: 2>, <State.DISABLED: 1>, <State.STANDBY: 5>]"),
            (0, datetime.strptime("{} 08:58:16.726000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 871602426, "[atarchiver]::[<State.ENABLED: 2>, <State.DISABLED: 1>, <State.STANDBY: 5>]"),
            (0, datetime.strptime("{} 16:01:55.648000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 4008497, "cccamera: Adding all resources."),
            (0, datetime.strptime("{} 16:02:07.735000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 4008497, "ccheaderservice: Adding all resources."),
            (0, datetime.strptime("{} 16:02:08.926000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 4008497, "ccarchiver: Adding all resources."),
            (0, datetime.strptime("{} 16:02:10.244000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 4008497, "ocps_2: Adding all resources."),
            (0, datetime.strptime("{} 16:02:11.998000+00:00".format((datetime.today() + timedelta(-2*i)).strftime("%Y-%m-%d")), '%Y-%m-%d %H:%M:%S.%f%z'), 4008497, "Read historical data in 0.00 sec")]


class SimulatedDataController(DataController):

    def __init__(self):
        self._dumped_log_information = []
        for i in range(60):
            self._dumped_log_information.extend(get_dumped_log_information(i))
        self._topics_available = {"lsst.sal.Script.logevent_logMessage": ['ScriptID',
                                                                          'filePath',
                                                                          'functionName',
                                                                          'level',
                                                                          'lineNumber',
                                                                          'message',
                                                                          'name',
                                                                          'priority',
                                                                          'private_efdStamp',
                                                                          'private_host',
                                                                          'private_identity',
                                                                          'private_kafkaStamp',
                                                                          'private_origin',
                                                                          'private_rcvStamp',
                                                                          'private_revCode',
                                                                          'private_seqNum',
                                                                          'private_sndStamp',
                                                                          'process',
                                                                          'salIndex',
                                                                          'timestamp',
                                                                          'traceback']}

    async def get_topic_available(self) -> List[str]:
        """
        :return:
        """
        return list(self._topics_available.keys())

    async def get_fields_available(self, topic: str) -> List[str]:
        """
        :param topic:
        :return:
        """
        return self._topics_available[topic]

    async def select_top_n(self, topic: str, fields: List[str], last_n: int) -> dataframe:
        """
        :param topic:
        :param fields:
        :param last_n:
        :return:
        """
        information = self._dumped_log_information[-1*last_n:]
        information = sorted(information, key=lambda x: x[1], reverse=True)
        df = pd.DataFrame(information, columns=["ScriptID", 'timestamp', 'salIndex', "message"])
        df.set_index('timestamp', inplace=True)
        return df

    async def select_interval(self, topic: str, fields: List[str], date_interval: DateInterval) -> dataframe:
        """
        :param topic:
        :param fields:
        :param date_interval:
        :return:
        """
        information = []
        for log_values in self._dumped_log_information:
            if date_interval.is_date_in_interval(log_values[1]):
                values = list(log_values)
                #values[1] = values[1].strftime('%Y-%m-%d %H:%M:%S.%f%z')
                information.append(tuple(values))
        information = sorted(information, key=lambda x: x[1], reverse=True)
        df = pd.DataFrame(information, columns=["ScriptID", 'timestamp', 'salIndex', "message"])
        df.set_index('timestamp', inplace=True)
        return df

    async def select_packed_interval(self, topic: str, fields: List[str], date_interval: DateInterval) -> dataframe:
        pass


if __name__ == '__main__':
    data_controller = SimulatedDataController()
    date_interval = DateInterval.from_date(datetime.now(), timedelta(hours = -24))
    log_data = data_controller.select_interval("lsst.sal.Script.logevent_logMessage",  ["ScriptID", 'salIndex', "message"], date_interval)
    display(log_data)
# from datetime import datetime, timedelta
# from typing import Tuple, List
#
# from lsst_ts.library.utils.date_interval import DateInterval
#
# dumped_log_information = [("{} 21:10:46.820000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")), 100006, "Configure started"),
# ("{} 18:10:58.469000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")), 100000, "Read historical data in 0.00 sec"),
# ("{} 21:00:38.757000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")), 42658887, "Read historical data in 0.00 sec"),
# ("{} 21:11:15.010000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")), 42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 -- Move to Zero- Starting time: {} 21:10:38.010131 UTC"),
# ("{} 21:11:24.499000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")), 42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 Compensation mode test Step 17- Starting time: {} 21:10:47.498767 UTC"),
# ("{} 21:12:03.801000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")), 42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 Compensation mode test Step 17- Starting time: {} 21:11:26.801265 UTC"),
# ("{} 21:32:15.953000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")), 42658887, "Read historical data in 0.00 sec"),
# ("{} 21:33:10.677000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")), 42658887, "Read historical data in 0.00 sec"),
# ("{} 21:33:53.638000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "Read historical data in 0.00 sec"),
# ("{} 21:35:47.396000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "Read historical data in 0.00 sec"),
# ("{} 21:59:31.119000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "Read historical data in 0.00 sec"),
# ("{} 22:08:06.152000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "Read historical data in 0.00 sec"),
# ("{} 22:11:02.459000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 -- Move to Zero- Starting time: {} 22:10:25.456788 UTC"),
# ("{} 22:11:07.295000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 Compensation mode test Step 17- Starting time: {} 22:10:30.295440 UTC"),
# ("{} 22:11:27.149000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 Compensation mode test Step 17- Starting time: {} 22:10:50.148659 UTC"),
# ("{} 22:11:41.007000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 Compensation mode test Step 17- Starting time: {} 22:11:04.006157 UTC"),
# ("{} 22:36:45.345000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "START- Camera Hexapod Integration Test -- LVV-T1600 -- Move to Zero- Starting time: {} 22:36:08.344298 UTC"),
# ("{} 23:00:47.682000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  7, "Read historical data in 0.00 sec"),
# ("{} 23:10:06.039000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "Read historical data in 0.00 sec"),
# ("{} 00:41:18.101000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "Read historical data in 0.03 sec"),
# ("{} 15:09:09.056000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  7, "Read historical data in 0.00 sec"),
# ("{} 15:18:21.314000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "Read historical data in 0.00 sec"),
# ("{} 15:25:42.776000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658887, "Read historical data in 0.00 sec"),
# ("{} 19:58:25.817000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  7, "Read historical data in 0.00 sec"),
# ("{} 20:40:31.318000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658886, "Read historical data in 0.00 sec"),
# ("{} 20:40:57.294000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  42658886, "Read historical data in 0.00 sec"),
# ("{} 20:52:48.404000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  100001, "Read historical data in 0.00 sec"),
# ("{} 20:52:48.412000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  100001, "Configure started"),
# ("{} 22:58:04.434000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  100002, "Read historical data in 0.00 sec"),
# ("{} 08:55:39.390000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  871602426, " [atdometrajectory]::[<State.ENABLED: 2>, <State.DISABLED: 1>, <State.STANDBY: 5>]"),
# ("{} 08:55:39.392000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  871602426, " All components in <State.STANDBY: 5>."),
# ("{} 08:58:16.715000+00:00".format((datetime.today() - timedelta(1)).strftime("%Y-%m-%d")),  871602426, """ Unable to transition atcamera to <State.STANDBY: 5> NoneType: None
# .
# Traceback (most recent call last):
# File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/csc_utils.py', line 161, in set_summary_state
#     await cmd.start(timeout=timeout)
#   File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/topics/remote_command.py', line 483, in start
#     return await cmd_info.next_ackcmd(timeout=timeout)
#   File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/topics/remote_command.py', line 201, in next_ackcmd
#     raise base.AckError(msg='Command failed', ackcmd=ackcmd)
# lsst.ts.salobj.base.AckError: msg='Command failed', ackcmd=(ackcmd private_seqNum=1668433851, ack=<SalRetCode.CMD_FAILED: -302>, error=0, result='Error : java.util.concurrent.TimeoutException: Timed out after 1000 milliseconds.\n\tTimed out after 1000 milliseconds.\n\tCould not get reply within the specified timeout of 1000 milliseconds for command Command(TokenizedCommand) getDistributionInfo to ats')
#
# The above exception was the direct cause of the following exception:
#
# Traceback (most recent call last):
#   File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/csc_utils.py', line 163, in set_summary_state
#     raise RuntimeError(
# RuntimeError: Error on cmd=cmd_standby, initial_state=2: msg='Command failed', ackcmd=(ackcmd private_seqNum=1668433851, ack=<SalRetCode.CMD_FAILED: -302>, error=0, result='Error : java.util.concurrent.TimeoutException: Timed out after 1000 milliseconds.\n\tTimed out after 1000 milliseconds.\n\tCould not get reply within the specified timeout of 1000 milliseconds for command Command(TokenizedCommand) getDistributionInfo to ats')
# """),
# ("{} 08:58:16.720000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  871602426, "[atspectrograph]::[<State.ENABLED: 2>, <State.DISABLED: 1>, <State.STANDBY: 5>]"),
# ("{} 08:58:16.724000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  871602426, "[atheaderservice]::[<State.ENABLED: 2>, <State.DISABLED: 1>, <State.STANDBY: 5>]"),
# ("{} 08:58:16.726000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  871602426, "[atarchiver]::[<State.ENABLED: 2>, <State.DISABLED: 1>, <State.STANDBY: 5>]"),
# ("{} 16:01:55.648000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  4008497, "cccamera: Adding all resources."),
# ("{} 16:02:07.735000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  4008497, "ccheaderservice: Adding all resources."),
# ("{} 16:02:08.926000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  4008497, "ccarchiver: Adding all resources."),
# ("{} 16:02:10.244000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  4008497, "ocps_2: Adding all resources."),
# ("{} 16:02:11.998000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  4008497, "Read historical data in 0.00 sec"),
# ("{} 01:34:08.936000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  770156871, "Exception from latiss_take_sequence()"),
# ("{} 01:34:08.937000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  770156871, "Latiss_acquire_and_take_sequence script completed"),
# ("{} 08:55:39.392000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  871602426, " All components in <State.STANDBY: 5>."),
# ("{} 08:58:16.715000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  871602426, """Unable to transition atcamera to <State.STANDBY: 5> NoneType: None
# .
# Traceback (most recent call last):
#   File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/csc_utils.py', line 161, in set_summary_state
#     await cmd.start(timeout=timeout)
#   File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/topics/remote_command.py', line 483, in start
#     return await cmd_info.next_ackcmd(timeout=timeout)
#   File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/topics/remote_command.py', line 201, in next_ackcmd
#     raise base.AckError(msg='Command failed', ackcmd=ackcmd)
# lsst.ts.salobj.base.AckError: msg='Command failed', ackcmd=(ackcmd private_seqNum=1668433851, ack=<SalRetCode.CMD_FAILED: -302>, error=0, result='Error : java.util.concurrent.TimeoutException: Timed out after 1000 milliseconds.\n\tTimed out after 1000 milliseconds.\n\tCould not get reply within the specified timeout of 1000 milliseconds for command Command(TokenizedCommand) getDistributionInfo to ats')
#
# The above exception was the direct cause of the following exception:
#
# Traceback (most recent call last):
#   File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/csc_utils.py', line 163, in set_summary_state
#     raise RuntimeError(
# RuntimeError: Error on cmd=cmd_standby, initial_state=2: msg='Command failed', ackcmd=(ackcmd private_seqNum=1668433851, ack=<SalRetCode.CMD_FAILED: -302>, error=0, result='Error : java.util.concurrent.TimeoutException: Timed out after 1000 milliseconds.\n\tTimed out after 1000 milliseconds.\n\tCould not get reply within the specified timeout of 1000 milliseconds for command Command(TokenizedCommand) getDistributionInfo to ats')
# """""),
# ("{} 08:58:16.720000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  871602426, "[atspectrograph]::[<State.ENABLED: 2>, <State.DISABLED: 1>, <State.STANDBY: 5>]"),
# ("{} 08:58:16.724000+00:00".format((datetime.today()).strftime("%Y-%m-%d")),  871602426, "[atheaderservice]::[<State.ENABLED: 2>, <State.DISABLED: 1>, <State.STANDBY: 5>]")]
#
# class SimulatedLogController:
#     """
#     Handler over a edf db dump to make local tests
#     """
#     _SAL_INDEX_TP_N_RETURN = 10
#     _DATETIME_INDEX = 0
#     _SALINDEX_INDEX = 1
#     _TEXT_INDEX = 2
#
#     def __init__(self):
#         pass
#
#     def get_last_n_sal_index(self, n: int = _SAL_INDEX_TP_N_RETURN) -> List[Tuple[datetime, int]]:
#         """
#         Returns datetime and sal_index for last n elements
#         :param n: last n values to be returned
#         :return: List with tuples values containing datetime and sal_index
#         """
#         values = [(value[SimulatedLogController._DATETIME_INDEX], value[SimulatedLogController._SALINDEX_INDEX]) for value in dumped_log_information[-1:-1*n]]
#         return values
#
#     def get_sal_index_by_interval(self, date_interval: DateInterval) -> List[Tuple[datetime, int]]:
#         """
#         Returns datetime and sal_index for all messages which date is inside the interval selected in dumped DB
#         :param date_interval: date interval that messages should belong to
#         :return: List with tuples values containing datetime and sal_index
#         """
#         date_sal_index = []
#         for log_information in dumped_log_information:
#             date = datetime.strptime(log_information[SimulatedLogController._DATETIME_INDEX], '%Y-%m-%d %H:%M:%S.%f%z')
#             if date_interval.is_date_in_interval(date):
#                 date_sal_index.append((date, log_information[SimulatedLogController._SALINDEX_INDEX]))
#         return date_sal_index
#
#     def get_log_information(self, sal_index: int, search_dt: datetime) -> str:
#         """
#         Search the message associated with the sal_index and the time in dumped DB
#         :param sal_index: int with the sal index information
#         :param search_dt: datetime of the message
#         :return: string with the messages or raise exception if not found
#         """
#         for log_information in dumped_log_information:
#             dt = datetime.strptime(log_information[SimulatedLogController._DATETIME_INDEX], '%Y-%m-%d %H:%M:%S.%f%z')
#             if sal_index == log_information[SimulatedLogController._SALINDEX_INDEX] and dt == search_dt:
#                 return log_information[SimulatedLogController._TEXT_INDEX]
#         raise Exception("Log relation: SalIndex: {}  datetime: {} not found", sal_index, dt.strftime('%Y-%m-%d %H:%M:%S.%f%z'))
#

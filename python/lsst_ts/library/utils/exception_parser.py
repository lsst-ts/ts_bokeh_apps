from dataclasses import dataclass, field
from typing import Iterable, Iterator, List, Optional, Union

exception_text2 = """Unable to transition atcamera to <State.ENABLED: 2> NoneType: None
.
Traceback (most recent call last):
  File "/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-1.0.0/
  lib/python3.8/site-packages/lsst/ts/salobj/csc_utils.py", line 139, in set_summary_state
    state_data = await remote.evt_summaryState.aget(timeout=timeout)  # type: ignore
  File "/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-1.0.0/
  lib/python3.8/site-packages/lsst/ts/salobj/topics/read_topic.py", line 533, in aget
    await asyncio.wait_for(self._next_task, timeout=timeout)
  File "/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-1.0.0/
  lib/python3.8/asyncio/tasks.py", line 501, in wait_for
    raise exceptions.TimeoutError()
asyncio.exceptions.TimeoutError

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-1.0.0/
  lib/python3.8/site-packages/lsst/ts/salobj/csc_utils.py", line 141, in set_summary_state
    raise RuntimeError(f"Cannot get summaryState from {remote.salinfo.name}")
RuntimeError: Cannot get summaryState from ATCamera
"""

exception_text = """ Unable to transition atcamera to <State.STANDBY: 5> NoneType: None
.
Traceback (most recent call last):
File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/
python3.8/site-packages/lsst/ts/salobj/csc_utils.py', line 161, in set_summary_state
    await cmd.start(timeout=timeout)
  File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/lib/
  python3.8/site-packages/lsst/ts/salobj/topics/remote_command.py', line 483, in start
    return await cmd_info.next_ackcmd(timeout=timeout)
  File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/lsst-scipipe-0.7.0/
  lib/python3.8/site-packages/lsst/ts/salobj/topics/remote_command.py', line 201, in next_ackcmd
    raise base.AckError(msg='Command failed', ackcmd=ackcmd)
lsst.ts.salobj.base.AckError: msg='Command failed',
ackcmd=(ackcmd private_seqNum=1668433851, ack=<SalRetCode.CMD_FAILED: -302>, error=0, result='Error :
java.util.concurrent.TimeoutException: Timed out after 1000 milliseconds.\n\t
Timed out after 1000 milliseconds.\n\tCould not get reply within the specified
timeout of 1000 milliseconds for command Command(TokenizedCommand) getDistributionInfo to ats')

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File '/opt/lsst/software/stack/conda/miniconda3-py38_4.9.2/envs/
  lsst-scipipe-0.7.0/lib/python3.8/site-packages/lsst/ts/salobj/csc_utils.py', line 163, in set_summary_state
    raise RuntimeError(
RuntimeError: Error on cmd=cmd_standby, initial_state=2: msg='Command failed',
ackcmd=(ackcmd private_seqNum=1668433851, ack=<SalRetCode.CMD_FAILED: -302>, error=0, result='Error :
java.util.concurrent.TimeoutException: Timed out after 1000 milliseconds.\n\tTimed out after 1000
milliseconds.\n\tCould not get reply within the specified timeout of 1000 milliseconds for command
Command(TokenizedCommand) getDistributionInfo to ats')
"""


@dataclass
class ExceptionEndInformation:
    type: str = "end"
    stacktrace: List[str] = field(default_factory=list)
    child: Optional["ExceptionInformation"] = None

    def __iter__(self) -> Iterator["ExceptionEndInformation"]:
        return self

    def __next__(self) -> "ExceptionEndInformation":
        raise StopIteration


class ExceptionRelation:
    END = 0
    DIRECT_CAUSE = 1
    SIDE_CAUSE = 2


@dataclass
class ExceptionInformation:
    type: str = "root"
    stacktrace: List[str] = field(default_factory=list)
    child: Union[
        "ExceptionInformation", "ExceptionEndInformation", None
    ] = ExceptionEndInformation(stacktrace=[])
    relation: int = ExceptionRelation.END

    def __iter__(self) -> Iterator["ExceptionInformation"]:
        self._actual_child = self.child
        return self

    def __next__(self) -> "ExceptionInformation":
        instance_return = self._actual_child
        assert instance_return is not None
        if isinstance(instance_return, ExceptionEndInformation):
            raise StopIteration
        assert self._actual_child is not None
        self._actual_child = self._actual_child.child
        return instance_return


def get_exception(exceptions_text: List[str], exception_info: List[str]) -> int:
    """
    :param exceptions_text:
    :param exception_info:
    :return:
    """
    line_text = exceptions_text.pop(0)
    line_text = line_text.strip()
    if (
        line_text
        == "During handling of the above exception, another exception occurred:"
    ):
        return ExceptionRelation.SIDE_CAUSE
    elif (
        line_text
        == "The above exception was the direct cause of the following exception:"
    ):
        return ExceptionRelation.DIRECT_CAUSE
    elif line_text.strip() == "EOF":
        return ExceptionRelation.END
    else:
        exception_info.append(line_text)
    return get_exception(exceptions_text, exception_info)


def set_hierarchy_exception(
    exceptions_text: List[str],
    parent_exception: ExceptionInformation,
    child_exception: bool = False,
) -> None:
    """
    :param exceptions_text:
    :param parent_exception:
    :param child_exception:
    :return:
    """
    raw_exception_info = []  # type: List[str]
    child_relation = get_exception(exceptions_text, raw_exception_info)
    if child_exception:
        exception_info = ExceptionInformation(
            type=raw_exception_info[-1],
            stacktrace=raw_exception_info[:],
            relation=child_relation,
        )
    else:
        exception_info = ExceptionInformation(
            type=raw_exception_info[0],
            stacktrace=raw_exception_info[:],
            relation=child_relation,
        )
    parent_exception.child = exception_info
    if len(exceptions_text):
        set_hierarchy_exception(exceptions_text, exception_info, child_exception=True)


def parse_exceptions_text(exception_text: str) -> Iterable[ExceptionInformation]:
    lines = exception_text.split("\n")
    exception_lines = [line for line in lines if line and line != "."]
    exception_lines.append("EOF")
    root = ExceptionInformation()
    set_hierarchy_exception(exception_lines, root)
    return root


if __name__ == "__main__":
    exceptions = parse_exceptions_text(exception_text)
    for exception in exceptions:
        print(exception.type, exception.stacktrace, exception.relation)

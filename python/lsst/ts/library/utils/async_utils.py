import asyncio

from lsst.ts.library.utils.logger import get_logger

_log = get_logger("examples.efd.data_aggregator")


async def _catcher(_function, *args, **kwargs):

    try:
        await _function(*args, **kwargs)
    except Exception as ex:
        _log.exception(f"Failed executing exception {_function.__name__}")


def async_function(function):
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            loop = None

        if loop and loop.is_running():
            _log.info('Async event loop already running. Adding coroutine to the event loop.')
            tsk = loop.create_task(_catcher(function, *args, **kwargs))
            # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
            # Optionally, a callback function can be executed when the coroutine completes
            tsk.add_done_callback(
                lambda t: _log.info(f'Task: {function.__name__}'))
        else:
            _log.info(f'Starting new event loop for function: {function}')
            asyncio.run(_catcher(function, *args, **kwargs))
    return wrapper
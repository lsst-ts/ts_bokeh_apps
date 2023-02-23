from typing import Protocol, Generic, TypeVar, Callable

__all__ = ['Observable']

T = TypeVar("T", contravariant=True)

class Observer(Protocol[T]):

    def notify(self, emitter: "Observable", value: T) -> None:
        raise NotImplementedError()


class Observable(Generic[T]):
    """
    """
    def __init__(self):
        self._observe_callbacks = []
        self._observers = []

    def attach(self, observer: Observer[T]):
        """
        :param observer:
        :return:
        """
        self._observers.append(observer)

    def attach_callable(self, function: Callable[[T], None]):
        """
        :param function:
        :return:
        """
        self._observe_callbacks.append(function)

    def detach_callable(self, function: Callable[[T], None]):
        """
        :param function:
        :return:
        """
        self._observers.remove(function)

    def detach(self, observer: Observer[T]):
        """
        :param observer:
        :return:
        """
        self._observers.remove(observer)

    def _notify(self, value: object):
        """
        :param value:
        :return:
        """
        for observer in self._observers:
            observer.notify(self, value)
        for observer in self._observe_callbacks:
            observer(value)


if __name__ == "__main__":
    class MyObservable(Observable[str]):
        pass


    class Obs:

        def __init__(self):
            super(Obs, self).__init__()

        def notify(self, emitter: "Observable", value: str):
            print("value")

    class MyObs:

        def __init__(self):
            super(Obs, self).__init__()

        def notify(self, emitter: "Observable", value: int):
            print("value")

    o = MyObservable()
    o.attach(Obs())
    o.attach_callable(MyObs().notify)
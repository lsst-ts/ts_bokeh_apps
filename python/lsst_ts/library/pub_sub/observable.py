
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable, TypeVar, Generic, List  # noqa: F401

__all__ = ['Observable']

T = TypeVar("T", contravariant=True)


class Observer(Generic[T]):

    def notify(self, emitter: 'Observable[T]', value: T) -> None:
        raise NotImplementedError()


class Observable(Generic[T]):
    """
    """
    def __init__(self) -> None:
        self._observe_callbacks = []  # type: List[Callable[[Observable[T], T], None]]
        self._observers = []  # type: List[Observer[T]]

    def attach(self, observer: Observer[T]) -> None:
        """
        :param observer:
        :return:
        """
        self._observers.append(observer)

    def attach_callable(self, function: 'Callable[[Observable[T], T], None]') -> None:
        """
        :param function:
        :return:
        """
        self._observe_callbacks.append(function)

    def detach_callable(self, function: 'Callable[[Observable[T], T], None]') -> None:
        """
        :param function:
        :return:
        """
        self._observe_callbacks.remove(function)

    def detach(self, observer: 'Observer[T]') -> None:
        """
        :param observer:
        :return:
        """
        self._observers.remove(observer)

    def _notify(self, value: T) -> None:
        """
        :param value:
        :return:
        """
        for observer in self._observers:
            observer.notify(self, value)
        for observer_callback in self._observe_callbacks:
            observer_callback(self, value)


if __name__ == "__main__":
    class MyObservable('Observable[str]'):
        pass

    class Obs(Observer[str]):

        def __init__(self) -> None:
            super(Obs, self).__init__()

        def notify(self, emitter: 'Observable[T]', value: str) -> None:
            print("value")

    class MyObs:

        def __init__(self) -> None:
            super().__init__()

        def notify(self, emitter: 'Observable[T]', value: int) -> None:
            print("value")

    o = MyObservable()
    o.attach(Obs())
    o.attach_callable(Obs().notify)

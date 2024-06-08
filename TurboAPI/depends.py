from typing import Callable


class Depends:
    def __init__(self, func: Callable, *args, **kwargs) -> None:
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        return self._func(*self._args, **self._kwargs)

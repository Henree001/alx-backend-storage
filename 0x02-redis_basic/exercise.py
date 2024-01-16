#!/usr/bin/env python3
"""Cache class definition."""
import redis
from uuid import uuid4
from functools import wraps
from typing import Callable, Union


def count_calls(method: Callable) -> Callable:
    """This function returns the wrapper function."""

    @wraps(method)
    def wrapper_function(self, *args, **kwargs):
        """
        This wrapper function counts the number of times methods
        of Cache class are called.
        """
        key = method.__qualname__
        self._redis.incr(key)

        return method(self, *args, **kwargs)

    return wrapper_function


def call_history(method: Callable) -> Callable:
    """This function returns a wrapper function."""

    @wraps(method)
    def wrapper_function(self, *args, **kwargs):
        """
        This function stores the history of inputs and outputs
        for a particular function.
        """

        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(output))

        return output

    return wrapper_function


def replay(method: Callable) -> None:
    # sourcery skip: use-fstring-for-concatenation, use-fstring-for-formatting
    """
    Replays the history of a function
    Args:
        method: The function to be decorated
    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode("utf-8"), o.decode("utf-8")))


class Cache:
    """Cache class."""

    def __init__(self) -> None:
        """Initialize."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis."""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Union[Callable, None] = None
    ) -> Union[str, bytes, int, float]:
        """Get data from Redis."""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Get a string from Redis."""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Get an integer from Redis."""
        return self.get(key, int)

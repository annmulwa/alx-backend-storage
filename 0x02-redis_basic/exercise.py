#!/usr/bin/env python3
'''
Using Redis
'''
import uuid
from functools import wraps
from typing import Callable, Union
import redis


def count_calls(method: Callable) -> Callable:
    '''
    decorator that takes a single method
    Callable argument and returns a Callable
    '''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
        function that increments the count for
        that key every time the method is called
        and returns the value returned by the
        original method.
        '''
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''
    has a single parameter named method
    that is a Callable and returns a Callable
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
        add its input parameters to one list in
        redis, and store its output into another list
        '''
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        output = method(self, *args, **kwargs)

        self._redis.rpush(input_key, str(args))
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


class Cache():
    '''
    A cache class
    '''
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        method should generate a random key
        (e.g. using uuid), store the input
        data in Redis using the random key
        and return the key.
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None)\
            -> Union[str, bytes, int, float]:
        '''
        convert the data back to the desired format.
        '''
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        '''
        convert the data back to str format
        '''
        variable = self._redis.get(key)
        return variable.decode("UTF-8")

    def get_int(self, key: str) -> int:
        '''
        convert the data back to int format
        '''
        variable = self._redis.get(key)
        try:
            variable = int(variable.decode("UTF-8"))
        except Exception:
            variable = 0
        return variable

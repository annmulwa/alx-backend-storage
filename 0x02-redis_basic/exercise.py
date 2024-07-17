#!/usr/bin/env python3
'''
Using Redis
'''
import uuid
from typing import Callable, Union
import redis


class Cache():
    '''
    A cache class
    '''
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

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

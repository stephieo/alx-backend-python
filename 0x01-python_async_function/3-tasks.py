#!/usr/bin/env python3
""" function to return """
import asyncio
from typing import Awaitable
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> Awaitable:
    """ returns a task object"""
    return asyncio.create_task(wait_random(max_delay))

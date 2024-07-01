#!/usr/bin/env python3
""" execute multiple coroutines"""
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """ generates n instances of  wait_random"""
    tasks = [asyncio.create_task(wait_random(max_delay)) for i in range(n)]
    # tasks = [task_wait_random(max_delay) for i in range(n)]

    results = []
    for task in asyncio.as_completed(tasks):
        result = await task
        results.append(result)
    return results

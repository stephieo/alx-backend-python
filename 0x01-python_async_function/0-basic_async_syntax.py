#!/usr/bin/env python3
""" simple async coroutine"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """returns an int after a delay"""
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay

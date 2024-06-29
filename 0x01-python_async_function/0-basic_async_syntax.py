#!/usr/bin/env python3
""" simple async coroutine"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> int:
    """returns an int after a delay"""
    delay = random.randint(0, max_delay)
    await asyncio.sleep(delay)
    return max_delay

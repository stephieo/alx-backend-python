#!/usr/bin/env python3
""" simple type annotated function"""
from typing import Callable

def mult_res(mult: float) -> float:
    return 2 * mult

def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """multiplier function """
    return mult_res
    
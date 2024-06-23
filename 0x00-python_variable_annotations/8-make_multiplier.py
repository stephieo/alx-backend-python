#!/usr/bin/env python3
""" simple type annotated function"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """multiplier function """
    def mult_res(mult: float) -> float:
        """sample function"""
        return multiplier * mult
    return mult_res

#!/usr/bin/env python3
""" simple type annotated function"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """sum of a list"""
    return sum(input_list)

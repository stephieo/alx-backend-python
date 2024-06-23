#!/usr/bin/env python3
""" simple type annotated function"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """ sum of list"""
    return sum(mxd_lst)

#!/usr/bin/env python3
""" simple type annotated function"""
from typing import Iterable, Sequence, Tuple, List


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ returns length of a list"""
    return [(i, len(i)) for i in lst]

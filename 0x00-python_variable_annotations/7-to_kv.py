#!/usr/bin/env python3
""" simple type annotated function"""
from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """simple function"""
    return (k, v**2)

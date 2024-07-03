#!/usr/bin/env python3
""" this module contains test cases for the  utils module"""
import unittest
from parameterized import parameterized
access_nested_map = __import__('utils').access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """this is a test case for the access_nested_map function"""
    @parameterized.expand([
        ({"a": 1}, "a", 1),
        ({"a": {"b": 2}}, "a", {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """checks that function gives expected output"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

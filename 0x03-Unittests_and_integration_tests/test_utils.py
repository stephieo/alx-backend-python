#!/usr/bin/env python3
""" this module contains test cases for the  utils module"""
import unittest
from parameterized import parameterized
from urllib import request
from unittest.mock import patch
access_nested_map = __import__('utils').access_nested_map
get_json = __import__('utils').get_json


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

    @parameterized.expand([
        ({}, "a", KeyError),
        ({"a": 1}, {"a", "b"}, KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """checks that function raises the expected errors"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """ tests the utils.get_json function"""
    @patch('requests.get')
    def test_get_json(self, mock_get):
        """ mocks the request.get methods"""
        cases = [("http://example.com", {"payload": True}),
                 ("http://holberton.io", {"payload": False})]
        for resp, url in cases:
            mock_get.return_value.json.return_value = resp
            test = get_json(url)
            self.assertEqual(test, resp)

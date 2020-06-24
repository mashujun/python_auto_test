import unittest


def get_test_suite(cases_dir):
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.discover(cases_dir))
    return suite


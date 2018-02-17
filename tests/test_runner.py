"""Main test runner
"""

import unittest

import test_webapi
import test_surepatch
import test_set_helper
import test_show_helper
import test_project_helper
import test_platform_helper
import test_components_helper

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(test_webapi)

suite.addTests(loader.loadTestsFromModule(test_surepatch))
suite.addTests(loader.loadTestsFromModule(test_set_helper))
suite.addTests(loader.loadTestsFromModule(test_show_helper))
suite.addTests(loader.loadTestsFromModule(test_project_helper))
suite.addTests(loader.loadTestsFromModule(test_platform_helper))
suite.addTests(loader.loadTestsFromModule(test_components_helper))

runner = unittest.TextTestRunner(verbosity=2)

result = runner.run(suite)

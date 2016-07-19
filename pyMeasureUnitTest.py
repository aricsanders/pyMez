#-----------------------------------------------------------------------------
# Name:        pyMeasureUnitTest
# Purpose:     To run unit tests on the pyMeasure Library
# Author:      Aric Sanders
# Created:     7/18/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" pyMeasureUnitTests Runs a series of unit tests on the modules in pyMeasure,
 before adding to the library add a unit test and check that all the others pass"""

#-----------------------------------------------------------------------------
# Standard Imports
import unittest
import re
#-----------------------------------------------------------------------------
# Third Party Imports
import pyMeasure.Code.DataHandlers.XMLModels
import pyMeasure.Code.Utils.Names
# for key,value in globals().copy()["pyMeasure"].__dict__.iteritems():
#     print(key,value)

#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions

#-----------------------------------------------------------------------------
# Module Classes
class TestNames(unittest.TestCase):
    """This Test case sees if all the tests in the modules in pyMeasure.Code.Utils.Names function properly"""
    def setUp(self):
        "Sets up the unit test"
        self.test_name="My_test name.xml"

    def tearDown(self):
        "Cleans up after the unit test"
        pass

    def test_split_filename(self):
        self.assertEqual(pyMeasure.Code.Utils.Names.split_filename(self.test_name),["My","test","name","xml"],
                         'pyMeasure.Code.Utils.Names.split_filename does not function as expected')

class TestXMLModels(unittest.TestCase):
    """This Test case sees if all the tests in the modules in pyMeasure.Code.Utils.Names function properly"""
    def setUp(self):
        "Sets up the unit test"

        self.module_tests=[]
        for key,value in globals().copy()["pyMeasure"].__dict__.iteritems():
            if re.match("test_",key):
                self.module_tests.append(key)

    def tearDown(self):
        "Cleans up after the unit test"
        pass
    def run_tests(self):
        print self.module_tests
        for item in self.module_tests:
            self.assertEqual(globals().copy()["pyMeasure"].__dict__[item](),True,"{0} failed".format(item))
#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    unittest.main()
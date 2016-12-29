#-----------------------------------------------------------------------------
# Name:        pyMeasureUnitTest
# Purpose:     To run unit tests on the pyMeasure Library
# Author:      Aric Sanders
# Created:     7/18/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" pyMeasureUnitTests Runs a series of unit tests on the modules in pyMeasure,
 before adding a module to the library add a unit test and check that all the others pass.
 All modules should be imported using import full.module.name and test classes should be
 named TestPyMeasureModuleName to prevent confusion and circular import statements """

#-----------------------------------------------------------------------------
# Standard Imports
import unittest
import re
#-----------------------------------------------------------------------------
# Third Party Imports
# All the modules should be imported here and each test case class should
# be a single module tests.
import pyMeasure.Code.DataHandlers.XMLModels
import pyMeasure.Code.DataHandlers.NISTModels
import pyMeasure.Code.DataHandlers.GeneralModels
import pyMeasure.Code.DataHandlers.StatistiCALModels
import pyMeasure.Code.DataHandlers.TouchstoneModels
import pyMeasure.Code.Utils.Names
# for key,value in globals().copy()["pyMeasure"].__dict__.iteritems():
#     print(key,value)

#-----------------------------------------------------------------------------
# Module Constants
TEST_CASE_CLASSES=["TestNames","TestXMLModels","TestGeneralModels"]
# IN_MODULE_TESTS=[]
# for key,value in globals().copy()["pyMeasure"].__dict__.iteritems():
#         if re.match("test_",key):
#             IN_MODULE_TESTS.append(key)
# print(IN_MODULE_TESTS)
#-----------------------------------------------------------------------------
# Module Functions
def build_suite(*test_classes):
    suites=[]
    for test in test_classes:
        suites.append(unittest.TestLoader().loadTestsFromTestCase(globals()[test]))
    return unittest.TestSuite(suites)

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
    def test_dictionary_to_xml(self):
        xml="<li>My list element</li>"
        self.assertEqual(pyMeasure.dictionary_to_xml({"li":"My list element"},char_between=''),
                         xml,"pyMeasure.dictionary_to_xml did not work")
    # def run_tests(self):
    #     print self.module_tests
    #     for item in self.module_tests:
    #         self.assertEqual(globals().copy()["pyMeasure"].__dict__[item](),
    #                          True,"{0} failed".format(item))

class TestGeneralModels(unittest.TestCase):
    """Unit tests for the General Models Module"""
    def setUp(self):
        self.test_string="This is a test string"
        self.test_string_list=["A first","A second", "A third list element"]
        self.test_data_list=[[1,2,3],[4,5,6]]

    def test_collapse_list(self):
        test_collapse=pyMeasure.Code.DataHandlers.GeneralModels.string_list_collapse(self.test_string_list)
        collapsed_string="A first\nA second\nA third list element"
        self.assertEqual(test_collapse,collapsed_string)
#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    suite=build_suite(*TEST_CASE_CLASSES)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #tests=TestAll()
    #tests.test_AsciiDataTable_equality()
#-----------------------------------------------------------------------------
# Name:        pyMezUnitTest
# Purpose:     To run unit tests on the pyMez Library
# Author:      Aric Sanders
# Created:     7/18/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" pyMezUnitTests Runs a series of unit tests on the modules in pyMez,
 before adding a module to the library add a unit test and check that all the others pass.
 All modules should be imported using import full.module.name and test classes should be
 named TestPyMeasureModuleName to prevent confusion and circular import statements

   Help
---------------
<a href="./index.html">`pyMez.Code.Utils`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""

#-----------------------------------------------------------------------------
# Standard Imports
import unittest
import re
#-----------------------------------------------------------------------------
# Third Party Imports
# All the modules should be imported here and each test case class should
# be a single module tests.
import pyMez.Code.DataHandlers.XMLModels
import pyMez.Code.DataHandlers.NISTModels
import pyMez.Code.DataHandlers.GeneralModels
import pyMez.Code.DataHandlers.StatistiCALModels
import pyMez.Code.DataHandlers.TouchstoneModels
import pyMez.Code.Utils.Names


#-----------------------------------------------------------------------------
# Module Constants
TEST_CASE_CLASSES=["TestNames","TestXMLModels","TestGeneralModels"]

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
    """This Test case sees if all the tests in the modules in pyMez.Code.Utils.Names function properly"""
    def setUp(self):
        "Sets up the unit test"
        self.test_name="My_test name.xml"

    def tearDown(self):
        "Cleans up after the unit test"
        pass

    def test_split_filename(self):
        self.assertEqual(pyMez.Code.Utils.Names.split_filename(self.test_name),["My","test","name","xml"],
                         'pyMez.Code.Utils.Names.split_filename does not function as expected')

class TestXMLModels(unittest.TestCase):
    """This Test case sees if all the tests in the modules in pyMez.Code.Utils.Names function properly"""
    def setUp(self):
        "Sets up the unit test"
        self.module_tests=[]
        for key,value in globals().copy()["pyMez"].__dict__.items():
            if re.match("test_",key):
                self.module_tests.append(key)

    def tearDown(self):
        "Cleans up after the unit test"
        pass
    def test_dictionary_to_xml(self):
        xml="<li>My list element</li>"
        self.assertEqual(pyMez.dictionary_to_xml({"li":"My list element"},char_between=''),
                         xml,"pyMez.dictionary_to_xml did not work")


class TestGeneralModels(unittest.TestCase):
    """Unit tests for the General Models Module"""
    def setUp(self):
        self.test_string="This is a test string"
        self.test_string_list=["A first","A second", "A third list element"]
        self.test_data_list=[[1,2,3],[4,5,6]]

    def test_collapse_list(self):
        test_collapse=pyMez.Code.DataHandlers.GeneralModels.string_list_collapse(self.test_string_list)
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
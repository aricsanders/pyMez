#-----------------------------------------------------------------------------
# Name:        Uncertainty
# Purpose:    To hold general functions and classes related to uncertainty
# Author:      Aric Sanders
# Created:     11/9/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Uncertainty is a collection of general classes and functions that pertain to uncertainty calculations.
 For specific uncertainty calculations look for modules with a modifier in the name such as  NISTUncertainty"""
#-----------------------------------------------------------------------------
# Standard Imports
import os
import sys

#-----------------------------------------------------------------------------
# Third Party Imports

#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions
def normalized_error(value_1,value_2,uncertainty,expansion_factor=1):
    """normalized error returns the  scalar normalized error (delta value/ (expansion_factor*uncertainty))"""
    return (value_2-value_1)/(uncertainty*expansion_factor)
def normalized_error_test(value_1,value_2,uncertainty,expansion_factor=1):
    """normalized error returns true if the scalar normalized error (delta value/ (expansion_factor*uncertainty))
    is less than or equal to one"""
    if normalized_error(value_1,value_2,uncertainty,expansion_factor)<=1:
        return True
    else:
        return False



#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass
    
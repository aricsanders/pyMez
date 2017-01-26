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
import math
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

def standard_error(value_1,uncertainty_value_1,value_2,uncertainty_value_2=0,expansion_factor=2):
    """calculates the standard errror (delta value/ (expansion factor * Sqrt(ua^2+ub^2)))"""
    return abs((value_2-value_1))/(math.sqrt(uncertainty_value_1**2+uncertainty_value_2**2)*expansion_factor)

def standard_error_data_table(table_1,table_2 ,**options):
    """Given two data tables finds the standard error for the intersection of the independent variable."""
    pass



#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass
    
#-----------------------------------------------------------------------------
# Name:        Fitting
# Purpose:     Functions and classes for fitting data
# Author:      Aric Sanders
# Created:     9/9/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Fitting is a module containing classes and fucntions for fitting data """

#-----------------------------------------------------------------------------
# Standard Imports
import os
import sys
#-----------------------------------------------------------------------------
# Third Party Imports
import numpy as np
try:
    import sympy
except:
    print("The module sympy either was not found or had an error"
          "Please put it on the python path, or resolve the error (http://www.sympy.org/en/index.html)")
    raise
try:
    import scipy
    import scipy.optimize
    import scipy.stats
except:
    print("The modules scipy.optimize and scipy.stats were not imported correctly"
          "Please scipy on the python path, or resolve the error "
          "(http://docs.scipy.org/doc/scipy/reference/index.html)")
    raise
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions
#TODO: These definitions of fits do not use the FittingFunction Class
# These fits are all of the form f(parameters,variables)
def line_function(a,x):
    "line function (y=a[1]x+a[0])"
    return a[1]*x+a[0]

def lorentzian_function(a,x):
    "a[0]=amplitude,a[1]=center,a[2]=FWHM"
    return a[0]*1/(1+(x-a[1])**2/(a[2]**2))

def gaussian_function(a,x):
    " a[0]=amplitude, a[1]=center, a[2]=std deviation"
    return a[0]*scipy.exp(-(x-a[1])**2/(2.0*a[2]**2))

def least_squares_fit(function,xdata,ydata,initial_parameters):
    """Returns a parameter list after fitting the data x_data,y_data
    with the function in the form of f(parameter_list,x)"""
    error_function=lambda a, xdata, ydata:function(a,xdata)-ydata
    a,success=scipy.optimize.leastsq(error_function, initial_parameters,args=(np.array(xdata),np.array(ydata)))
    return a

def calculate_residuals(fit_function,a,xdata,ydata):
    """Given the fit function, a parameter vector, xdata, and ydata returns the residuals as [x_data,y_data]"""
    output_x=xdata
    output_y=[fit_function(a,x)-ydata[index] for index,x in enumerate(xdata)]
    return [output_x,output_y]
#-----------------------------------------------------------------------------
# Module Classes
class FittingFunction():
    """FittingFunction is a class that holds a fitting function, it uses sympy to provide
     symbolic manipulation of the function and formatted output. If called it acts like a
     tradional python function"""
    def __init__(self):pass
#-----------------------------------------------------------------------------
# Module Scripts
def test_linear_fit(data=None):
    """Tests fitting a data set to a line, the data set is assumed to be in the form [[x_data,y_data]]"""
    if data is None:
        #x_data=np.linspace(-100,100,100)
        x_data=[i*1. for i in range(100)]
        y_data=[2.004*x+3 for x in x_data]
        data=[x_data,y_data]
        #print(data)
    initial_guess=[1,0]
    results=least_squares_fit(line_function,data[0],data[1],initial_guess)
    print("The fit of data is y={1:3.2g} x + {0:3.2g}".format(*results))


#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    test_linear_fit()
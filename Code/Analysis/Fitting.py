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
from types import *
#-----------------------------------------------------------------------------
# Third Party Imports

try:
    import numpy as np
except:
    print("The module numpy either was not found or had an error"
          "Please put it on the python path, or resolve the error")
    raise
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

def build_modeled_data_set(x_list,function_list):
    """build_modeled_data_set takes an input independent variable and a list
    of  functions and returns a data set of the form [..[xi,f1(xi),..fn(xi)]]
    it is meant to create a modeled data set. Requires that the list of functions is callable f(x) is defined"""
    out_data=[]
    for x in x_list:
        new_row=[]
        new_row.append(x)
        for function in function_list:
            if type(function(x)) in [np.ndarray,'numpy.array']:
                # to list is needed if the function returns np.array
                new_row.append(function(x).tolist())
            else:
                new_row.append(function(x))
        out_data.append(new_row)
    return out_data
#-----------------------------------------------------------------------------
# Module Classes
class FittingFunction():
    """FittingFunction is a class that holds a fitting function, it uses sympy to provide
     symbolic manipulation of the function and formatted output. If called it acts like a
     tradional python function"""
    def __init__(self):pass
    def __call__(self, *args, **kwargs):pass

class FunctionalModel(object):
    """FittingModel is a class that holds a fitting function, it uses sympy to provide
     symbolic manipulation of the function and formatted output. If called it acts like a
     tradional python function"""
    def __init__(self,**options):
        defaults= {"parameters":None,"variables":None,"equation":None,"parameter_values":{}}
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value
        # fix any lists
        for item in ["parameters","variables"]:
            if type(self.options[item]) is StringType:
                self.options[item]=re.split("\s+",self.options[item])
            self.__dict__[item]=self.options[item]
            self.__dict__[item+"_symbols"]=sympy.symbols(self.options[item])
            # this creates the python variables in the global namespace, may back fire with lots of variables
            for index,symbol in enumerate(self.__dict__[item+"_symbols"][:]):
                globals()[item[index]]=symbol
            self.options[item]=None
        self.equation=sympy.sympify(self.options["equation"])
        self.function=sympy.lambdify(self.parameters+self.variables,self.equation,'numpy')
        self.parameter_values=self.options["parameter_values"]
        self.options["parameter_values"]={}
    def __call__(self,*args,**keywordargs):
        """Controls the behavior when called as a function"""
        return self.function(*args,**keywordargs)

    def set_parameters(self,parameter_dictionary=None,**parameter_dictionary_keyword):
        """Sets the parameters to values in dictionary"""
        if parameter_dictionary is None:
            try:
                parameter_dictionary=parameter_dictionary_keyword
            except:
                pass
        self.parameter_values=parameter_dictionary
        self.function=sympy.lambdify(self.variables,self.equation.subs(self.parameter_values),'numpy')


    def clear_parameters(self):
        """Clears the parmeters specified by set_parameters"""
        self.function=sympy.lambdify(self.parameters+self.variables,self.equation,'numpy')
        self.parameter_values={}

    def fit_data(self,x_data,y_data,**options):
        defaults= {"initial_guess":{parameter:0 for parameter in self.parameters},"fixed_parameters":None}
        self.fit_options={}
        for key,value in defaults.iteritems():
            self.fit_options[key]=value
        for key,value in options.iteritems():
            self.fit_options[key]=value

        def fit_f(a,x):
            self.clear_parameters()
            input_list=[]
            for parameter in a:
                input_list.append(parameter)
            input_list.append(x)
            return self.function(*input_list)
        # this needs to be reflected in fit_parameters
        a0=[]
        for key in self.parameters[:]:
            a0.append(self.fit_options["initial_guess"][key])
        result=fit(fit_f,x_list,y_data,a0)
        fit_parameters=result.tolist()
        fit_parameter_dictionary={parameter:fit_parameters[index] for index,parameter in enumerate(self.parameters)}
        self.set_parameters(fit_parameter_dictionary)

    def __add__(self,other):
        """Defines Addition for the class"""
        parameters=list(set(self.parameters+other.parameters))
        variables=list(set(self.variables+other.variables))
        #print("{0} is {1}".format("parameters",parameters))
        #print("{0} is {1}".format("variables",variables))
        equation=self.equation+other.equation
        #print("{0} is {1}".format("equation",equation))
        new_function=FunctionalModel(parameters=parameters,variables=variables,equation=equation)
        return new_function
    def __sub__(self,other):
        """Defines Addition for the class"""
        parameters=list(set(self.parameters+other.parameters))
        variables=list(set(self.variables+other.variables))
        #print("{0} is {1}".format("parameters",parameters))
        #print("{0} is {1}".format("variables",variables))
        equation=self.equation-other.equation
        #print("{0} is {1}".format("equation",equation))
        new_function=FunctionalModel(parameters=parameters,variables=variables,equation=equation)
        return new_function
    def __mul__(self,other):
        """Defines Addition for the class"""
        parameters=list(set(self.parameters+other.parameters))
        variables=list(set(self.variables+other.variables))
        #print("{0} is {1}".format("parameters",parameters))
        #print("{0} is {1}".format("variables",variables))
        equation=self.equation*other.equation
        #print("{0} is {1}".format("equation",equation))
        new_function=FunctionalModel(parameters=parameters,variables=variables,equation=equation)
        return new_function

    def __pow__(self,other):
        """Defines Addition for the class"""
        parameters=list(set(self.parameters+other.parameters))
        variables=list(set(self.variables+other.variables))
        #print("{0} is {1}".format("parameters",parameters))
        #print("{0} is {1}".format("variables",variables))
        equation=self.equation**other.equation
        #print("{0} is {1}".format("equation",equation))
        new_function=FunctionalModel(parameters=parameters,variables=variables,equation=equation)
        return new_function

    def __div__(self,other):
        """Defines Addition for the class"""
        parameters=list(set(self.parameters+other.parameters))
        variables=list(set(self.variables+other.variables))
        #print("{0} is {1}".format("parameters",parameters))
        #print("{0} is {1}".format("variables",variables))
        equation=self.equation/other.equation
        #print("{0} is {1}".format("equation",equation))
        new_function=FunctionalModel(parameters=parameters,variables=variables,equation=equation)
        return new_function

    def __str__(self):
        """Controls the strign behavior of the function"""
        return str(self.equation.subs(self.parameter_values))

    def to_latek(self):
        """Returns a Latek form of the equation using current parameters"""
        return sympy.latex(self.equation.subs(self.parameter_values))
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
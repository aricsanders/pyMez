#-----------------------------------------------------------------------------
# Name:        Fitting
# Purpose:     Functions and classes for fitting data
# Author:      Aric Sanders
# Created:     9/9/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Fitting is a module containing classes and functions for fitting and simulating
data. The primary class to fit data and create functions is FunctionalModel.


 Examples
--------
    #!python
    >>line=FunctionalModel(variables='x',parameters='m b',equation='m*x+b')
    >>line(m=2,b=5,x=np.array([1,2,3]))

 <h3><a href="../../../Examples/html/Fitting_Example.html">Fitting Example</a></h3>

Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html)
+ [re](https://docs.python.org/2/library/re.html)
+ [types](https://docs.python.org/2/library/types.html)
+ [numpy](https://docs.scipy.org/doc/)
+ [scipy](https://docs.scipy.org/doc/)
+ [sympy](http://www.sympy.org/en/index.html)

Help
---------------
<a href="./index.html">`pyMez.Code.Analysis`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>
"""

#-----------------------------------------------------------------------------
# Standard Imports
import os
import sys
from types import *
import re
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))

try:
    from Code.Utils.Types import *
except:
    print("The module pyMez.Code.Utils.Types was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError

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
try:
    import matplotlib.pyplot as plt
except:
    print("The module matplotlib was not found,"
          "please put it on the python path")
#-----------------------------------------------------------------------------
# Module Constants
LAMBDIFY_MODULES = ["numpy",
                    {"besselj": sympy.besselj,
                     "bessely": sympy.bessely,
                     "besseli": sympy.besseli,
                     "besselk": sympy.besselk,
                     "hankel1": sympy.hankel1,
                     "hankel2": sympy.hankel2}]

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



class FunctionalModel(object):
    """FittingModel is a class that holds a fitting function, it uses sympy to provide
     symbolic manipulation of the function and formatted output. If called it acts like a
     traditional python function. Initialize the class with parameters, variables and an equation.
     Ex. line=FunctionalModel(variables='x', parameters='m b', equation='m*x+b'), to call as a function
     the parameters must be set. line(m=2,b=1,x=1)
     or
     line.set_parameters(m=1,b=2)
     line(1). To fit data use the .fit_data(x_data,y_data) method. This will automatically set the parameters to
     the fit values."""

    def __init__(self, **options):
        """Initializes the FunctionalModel, note if the equation passed has a special function bessel,etc.
        it will find it"""
        defaults = {"parameters": None,
                    "variables": None,
                    "equation": None,
                    "parameter_values": {},
                    "special_function": False}
        self.options = {}
        for key, value in defaults.items():
            self.options[key] = value
        for key, value in options.items():
            self.options[key] = value
        # fix any lists
        for item in ["parameters", "variables"]:
            if isinstance(self.options[item], StringType):
                self.options[item] = re.split("\s+", self.options[item])
            self.__dict__[item] = self.options[item]
            # ------------ This was not needed for multisine fit removed 11/27/2018
            # self.__dict__[item+"_symbols"]=sympy.symbols(self.options[item])
            # this creates the python variables in the global namespace, may back fire with lots of variables
            # for index,symbol in enumerate(self.__dict__[item+"_symbols"][:]):
            #     globals()[item[index]]=symbol
            # -----------------
            self.options[item] = None
        self.special_function = self.options["special_function"]
        self.equation = sympy.sympify(self.options["equation"])
        special_function_keys = list(LAMBDIFY_MODULES[1].keys())
        for key in special_function_keys:
            if re.search(key, str(self.options["equation"])):
                self.special_function = True
        if self.special_function:
            self.function = sympy.lambdify(self.parameters + self.variables, self.equation, modules=LAMBDIFY_MODULES)
        else:
            self.function = sympy.lambdify(self.parameters + self.variables, self.equation, "numpy")
        self.parameter_values = self.options["parameter_values"]
        self.options["parameter_values"] = {}

    def __call__(self, *args, **keywordargs):
        """Controls the behavior when called as a function"""
        return self.function(*args, **keywordargs)

    def set_parameters(self, parameter_dictionary=None, **parameter_dictionary_keyword):
        """Sets the parameters to values in dictionary"""
        if parameter_dictionary is None:
            try:
                parameter_dictionary = parameter_dictionary_keyword
            except:
                pass
        self.parameter_values = parameter_dictionary
        if self.special_function:
            self.function = np.vectorize(lambda x: sympy.N(sympy.lambdify(self.variables,
                                                                          self.equation.subs(self.parameter_values),
                                                                          modules=LAMBDIFY_MODULES)(x)))
        else:
            self.function = sympy.lambdify(self.variables, self.equation.subs(self.parameter_values),
                                           modules=LAMBDIFY_MODULES)

    def clear_parameters(self):
        """Clears the parmeters specified by set_parameters"""
        self.function = sympy.lambdify(self.parameters + self.variables, self.equation, modules=LAMBDIFY_MODULES)
        self.parameter_values = {}

    def fit_data(self, x_data, y_data, **options):
        """Uses the equation to fit the data, after fitting the data sets the parameters.
        """
        defaults = {"initial_guess": {parameter: 0.0 for parameter in self.parameters}, "fixed_parameters": None}
        self.fit_options = {}
        for key, value in defaults.items():
            self.fit_options[key] = value
        for key, value in options.items():
            self.fit_options[key] = value

        def fit_f(a, x):
            self.clear_parameters()
            input_list = []
            for parameter in a:
                input_list.append(parameter)
            if self.special_function:
                if isinstance(x, list):
                    out = np.array(list(map(lambda y: sympy.N(self.function(*(input_list + [y]))), x)),
                                   dtype=np.float64)
                    return out
                elif isinstance(x, np.ndarray):
                    out = np.array(list(map(lambda y: sympy.N(self.function(*(input_list + [y]))), x.tolist())),
                                   dtype=np.float64)
                    return out
                else:
                    out = sympy.N(self.function(*input_list))
                    return out
            else:
                input_list.append(x)
                return self.function(*input_list)

        # this needs to be reflected in fit_parameters
        a0 = []
        for key in self.parameters[:]:
            a0.append(self.fit_options["initial_guess"][key])
        a0 = np.array(a0)
        result = least_squares_fit(fit_f, x_data, y_data, a0)
        fit_parameters = result.tolist()
        fit_parameter_dictionary = {parameter: fit_parameters[index] for index, parameter in enumerate(self.parameters)}
        self.set_parameters(fit_parameter_dictionary)

    def __div__(self, other):
        return self.__truediv__(other)

    def __add__(self, other):
        """Defines addition for the class, if it is another functional model add the models else just change the
        equation"""
        if isinstance(other, FunctionalModel):
            parameters = list(set(self.parameters + other.parameters))
            variables = list(set(self.variables + other.variables))
            # print("{0} is {1}".format("parameters",parameters))
            # print("{0} is {1}".format("variables",variables))
            equation = self.equation + other.equation
            # print("{0} is {1}".format("equation",equation))
        else:
            parameters = self.parameters
            variables = self.variables
            equation = self.equation + other
        new_function = FunctionalModel(parameters=parameters, variables=variables, equation=equation)
        return new_function

    def __sub__(self, other):
        """Defines subtraction for the class"""
        if isinstance(other, FunctionalModel):
            parameters = list(set(self.parameters + other.parameters))
            variables = list(set(self.variables + other.variables))
            # print("{0} is {1}".format("parameters",parameters))
            # print("{0} is {1}".format("variables",variables))
            equation = self.equation - other.equation
            # print("{0} is {1}".format("equation",equation))
        else:
            parameters = self.parameters
            variables = self.variables
            equation = self.equation - other
        new_function = FunctionalModel(parameters=parameters, variables=variables, equation=equation)
        return new_function

    def __mul__(self, other):
        """Defines multiplication for the class"""
        if isinstance(other, FunctionalModel):
            parameters = list(set(self.parameters + other.parameters))
            variables = list(set(self.variables + other.variables))
            # print("{0} is {1}".format("parameters",parameters))
            # print("{0} is {1}".format("variables",variables))
            equation = self.equation * other.equation
            # print("{0} is {1}".format("equation",equation))
        else:
            parameters = self.parameters
            variables = self.variables
            equation = self.equation * other
        new_function = FunctionalModel(parameters=parameters, variables=variables, equation=equation)
        return new_function

    def __pow__(self, other):
        """Defines power for the class"""
        if isinstance(other, FunctionalModel):
            parameters = list(set(self.parameters + other.parameters))
            variables = list(set(self.variables + other.variables))
            # print("{0} is {1}".format("parameters",parameters))
            # print("{0} is {1}".format("variables",variables))
            equation = self.equation ** other.equation
            # print("{0} is {1}".format("equation",equation))
        else:
            parameters = self.parameters
            variables = self.variables
            equation = self.equation ** other
        new_function = FunctionalModel(parameters=parameters, variables=variables, equation=equation)
        return new_function

    def __truediv__(self, other):
        """Defines division for the class"""
        if isinstance(other, FunctionalModel):
            parameters = list(set(self.parameters + other.parameters))
            variables = list(set(self.variables + other.variables))
            # print("{0} is {1}".format("parameters",parameters))
            # print("{0} is {1}".format("variables",variables))
            equation = self.equation / other.equation
            # print("{0} is {1}".format("equation",equation))
        else:
            parameters = self.parameters
            variables = self.variables
            equation = self.equation / other
        new_function = FunctionalModel(parameters=parameters, variables=variables, equation=equation)
        return new_function

    def __str__(self):
        """Controls the string behavior of the function"""
        return str(self.equation.subs(self.parameter_values))

    def compose(self, other):
        """Returns self.equation.sub(variable=other)"""
        if len(self.variables) == 1:
            variables = other.variables
            parameters = list(set(self.parameters + other.parameters))
            equation = self.equation.subs({self.variables[0]: other})
            new_function = FunctionalModel(parameters=parameters, variables=variables, equation=equation)
            return new_function
        else:
            return None

    def to_latex(self):
        """Returns a Latex form of the equation using current parameters"""
        return sympy.latex(self.equation.subs(self.parameter_values))

    def plot_fit(self, x_data, y_data, **options):
        """Fit a data set and show the results"""
        defaults = {"title": True}
        plot_options = {}
        for key, value in defaults.items():
            plot_options[key] = value
        for key, value in options.items():
            plot_options[key] = value

        self.fit_data(x_data, y_data, **plot_options)
        figure = plt.figure("Fit")
        plt.plot(x_data, y_data, label="Raw Data")
        plt.plot(x_data, self.function(x_data), 'ro', label="Fit")
        plt.legend(loc=0)
        if plot_options["title"]:
            if plot_options["title"] is True:
                plt.title(str(self))
            else:
                plt.title(plot_options["title"])
        plt.show()
        return figure

    def d(self, respect_to=None, order=1):
        """Takes the derivative with respect to variable or parameter provided or defaults to first variable"""
        if respect_to is None:
            respect_to = self.variables[0]
        equation = self.equation.copy()
        for i in range(order):
            equation = sympy.diff(equation, respect_to)
        return FunctionalModel(parameters=self.parameters[:], variables=self.variables[:], equation=str(equation))

    def integrate(self, respect_to=None, order=1):
        """Integrates with respect to variable or parameter provided or defaults to first variable.
        Does not add a constant of integration."""
        if respect_to is None:
            respect_to = self.variables_symbols[0]
        equation = self.equation.copy()
        for i in range(order):
            equation = sympy.integrate(equation, respect_to)
        return FunctionalModel(parameters=self.parameters[:], variables=self.variables[:], equation=str(equation))

    # todo: This feature does not work because of the namspace of the parameters and variables
    # I don't know what name sympify uses when it creates the equation
    # def series(self,variable_or_parameter,value=0,order=6):
    #     """Calculates the symbolic series expansion of order around the variable or parameter value
    #     of the functional model. Returns a new FunctionalModel"""
    #     equation=sympy.series(self.equation,variable_or_parameter,value,order).removeO()
    #     parameters=self.parameters[:]
    #     variables=self.variables[:]
    #     return FunctionalModel(equation=equation,variables=variables,parameters=parameters)

    def limit(self, variable_or_parameter, point):
        """Finds the symbolic limit of the FunctionalModel for the variable or parameter approaching point"""
        equation = sympy.limit(self.equation, variable_or_parameter, point)
        parameters = self.parameters[:]
        variables = self.variables[:]
        return FunctionalModel(equation=equation, variables=variables, parameters=parameters)


class DataSimulator(object):
    """A class that simulates data. It creates a data set from a FunctionalModel with the parameters set,
    and an optional output noise. The attribute self.x has the x data and self.data has the result. The simulator may be
    called as a function on a single point or an numpy array."""
    def __init__(self,**options):
        """Intializes the DataSimulator class"""
        defaults= {"parameters":None,
                   "variables":None,
                   "equation":None,
                   "parameter_values":{},
                   "model":None,
                   "variable_min":None,
                   "variable_max":None,
                   "number_points":None,
                   "variable_step":None,
                   "output_noise_type":None,
                   "output_noise_width":None,
                   "output_noise_center":None,
                   "output_noise_amplitude":1.,
                   "random_seed":None,
                   "x":np.array([])}
        self.options={}
        for key,value in defaults.items():
            self.options[key]=value
        for key,value in options.items():
            self.options[key]=value
        # set the self.model attribute
        if self.options["model"]:
            self.model=self.options["model"]
        else:
            # try and create the model from the options
            try:
                self.model=FunctionalModel(variables=self.options["variables"],
                                           parameters=self.options["parameters"],
                                          equation=self.options["equation"])
            except:
                print("Could not form a model from the information given, either model has to be specified or"
                     "parameters, variables and equation has to be specified")
                # todo: make an error specific to this case
                raise
        if self.options["parameter_values"]:
            self.model.set_parameters(self.options["parameter_values"])
        self.x=self.options["x"]
        self.random_seed=self.options["random_seed"]
        output_noise_names=["type","center","width","amplitude"]
        for index,output_noise_name in enumerate(output_noise_names):
            self.__dict__["output_noise_{0}".format(output_noise_name)]=self.options["output_noise_{0}".format(output_noise_name)]
        self.set_output_noise()
        if self.options["variable_min"] and self.options["variable_max"]:
            self.set_x(variable_min=self.options["variable_min"],
                       variable_max=self.options["variable_max"],
                       number_points=self.options["number_points"],
                       variable_step=self.options["variable_step"])



        self.set_parameters=self.model.set_parameters
        self.clear_parameters=self.model.clear_parameters
        self.set_data()



    def set_x(self, variable_min=None, variable_max=None,number_points=None,variable_step=None):
        """Sets the dependent variable values, min, max and number of points or step"""
        if [variable_min,variable_max]==[None,None]:
            self.x=np.array([])
        elif isinstance(variable_min,list):
            self.x=variable_min
        else:
            if variable_step:
                number_points=(variable_max-variable_min)/variable_step
            self.x=np.linspace(variable_max,variable_min,number_points)
        self.set_output_noise()


    def set_output_noise(self,output_noise_type=None,output_noise_center=None,output_noise_width=None,output_noise_amplitude=1.):
        """Set the output noise distrubution. Possible types are gaussian, uniform, triangular, lognormal, with the
        assumption all are symmetric
        """
        output_noise_characteristics=[output_noise_type,output_noise_center,output_noise_width,output_noise_amplitude]
        output_noise_names=["type","center","width","amplitude"]
        for index,output_noise_characteristic in enumerate(output_noise_characteristics):
            if output_noise_characteristic:
                self.__dict__["output_noise_{0}".format(output_noise_names[index])]=output_noise_characteristic
        if self.output_noise_type is None or not self.x.any():
            self.output_noise=np.array([])
        else:
            # set the random seed
            np.random.seed(self.random_seed)

            # now handle the output types, all in np.random
            if re.search("gauss|normal",self.output_noise_type,re.IGNORECASE):
                self.output_noise=output_noise_amplitude*np.random.normal(self.output_noise_center,
                                                                    self.output_noise_width,len(self.x))
            elif re.search("uni|square|rect",self.output_noise_type,re.IGNORECASE):
                self.output_noise=output_noise_amplitude*np.random.uniform(self.output_noise_center-self.output_noise_width/2,
                                                                     self.output_noise_width+self.output_noise_width/2,
                                                                     len(self.x))
            elif re.search("tri",self.output_noise_type,re.IGNORECASE):
                self.output_noise=output_noise_amplitude*np.random.triangular(self.output_noise_center-self.output_noise_width/2,
                                                                     self.output_noise_center,
                                                                     self.output_noise_width+self.output_noise_width/2,
                                                                    len(self.x))
        self.set_data()



    def set_data(self):
        if self.model.parameter_values:
            if self.output_noise.any():
                out_data=self.model(self.x)+self.output_noise
            else:
                if self.x.any():
                    out_data=self.model(self.x)
                else:
                    out_data=[]
        else:
            out_data=[]
        self.data=out_data

    def get_data(self):
        return self.data[:]

    def __call__(self,x_data):
        """Returns the simulated data for x=x_data, to have deterministic responses, set self.random_seed"""
        if type(x_data) not in [np.array]:
            if isinstance(x_data, ListType):
                x_data=np.array(x_data)
            else:
                x_data=np.array([x_data])
        #print("{0} is {1}".format("x_data",x_data))
        self.x=x_data
        self.set_output_noise()
        self.set_data()
        out=self.data[:]
        if len(out)==1:
            out=out[0]
        return out

class Multicosine(FunctionalModel):
    """Multicosine creates a Functional Model of the form f(t) = A_1*cos(2*pi*frequency_list[0]*t+phi_1)+
    ... A_N*cos(2*pi*frequency_list[N]*t+phi_N). It requires a frequency_list to be passed on creation"""
    def __init__(self,frequency_list):
        # Constructing the equation string to pass to FunctionalModel
        number_terms = len(frequency_list)
        fit_function = ""
        for i in range(number_terms):
            if i < number_terms - 1:
                fit_function = fit_function + "A_{0}*cos(2*pi*{1}*t+phi_{0})+".format(i + 1, frequency_list[i])
            else:
                fit_function = fit_function + "A_{0}*cos(2*pi*{1}*t+phi_{0})".format(i + 1, frequency_list[i])
        # Construct the parameter List
        parameter_list = ["A_{0}".format(i + 1) for i in range(number_terms)] + ["phi_{0}".format(i + 1) for i in
                                                                                 range(number_terms)]
        FunctionalModel.__init__(self,parameters=parameter_list,variables="t",equation=fit_function)

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
    print(("The fit of data is y={1:3.2g} x + {0:3.2g}".format(*results)))

def test_Multicosine():
    """ Tests the creation of a Multicosine"""
    frequency_list=np.linspace(10**9,2*10**9,3)
    print("The frequecy_list is {0}".format(frequency_list))
    print("Creating Multicosine ....")
    multisine=Multicosine(frequency_list)
    print("The mutlisine is {0}".format(multisine))
    print("The latex form is "+ multisine.to_latex())



#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    test_linear_fit()
    test_Multicosine()
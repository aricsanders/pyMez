#-----------------------------------------------------------------------------
# Name:        alias.py
# Purpose:     Function that provides exec string to define common aliases for 
#              for functions
# Author:      Aric Sanders
# Created:     2/21/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Module that defines functions for handling alias definitions in Classes

Help
---------------
<a href="./index.html">`pyMez.Code.Utils`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""

#-------------------------------------------------------------------------------
# Standard imports

import re
import types

#-------------------------------------------------------------------------------
# Module Functions

def alias(object):
    """ Creates aliases that map all non built-in methods to  
    both lowerCapitalCase and all_lower_with_underscore naming conventions the
    output is a list of strings to be used with exec(list[i]) """
    
    old_names=[]
    split_name=[]
    exec_list=[]
    new_name=''
    
    # Get all the atributes without __ in the begining
    for attribute in dir(object):
        if not re.match('_',attribute):
            try:
                if isinstance(eval('object.%s'%attribute), types.MethodType):
                    old_names.append(attribute)
            except:pass
    # If they are camelCase make them all lower with underscores or vice versa
    for name in old_names:
        if re.search(r'[A-Z]+',name) and not re.search(r'_',name):
            split_upper_case=re.split(r'[A-Z]+',name)
            upper_matches=re.findall(r'[A-Z]+',name)
            for index,piece in enumerate(split_upper_case):
                if index<len(upper_matches):
                    new_name=new_name+piece+'_'+upper_matches[index].lower()
                else:
                    new_name=new_name+piece
            exec_list.append(('self.'+new_name+'='+'self.'+name))

        elif re.search(r'_',name):
            split_name=name.split('_')
            for index,piece in enumerate(split_name):
                if index==0:
                    new_name=piece
                else :
                    new_name=new_name+piece.title()
            exec_list.append(('self.'+new_name+'='+'self.'+name))
        #else: pass
    return exec_list

#-------------------------------------------------------------------------------
# Class Definitions

class MyTestClass():
    """ A class to test the alias function: call it in a for loop inside of 
    __init__() method """
    
    def __init__(self):
        self.littleAttribue=[]
        self.i_like_underscores=[]
        # this calls and executes the alias function
        for command in alias(self):
            exec(command)

    def myFunctionNumberOne(self):
        pass
    def my_function_number_two(self):
        pass
    def my_funtion_Number_three(self):
        pass

#-------------------------------------------------------------------------------
# Module Scripts
def test_alias():
    print(" Before making the instance the attributes defined are:")
    for attribute in dir(MyTestClass):
        print('Attribute Name: %s'%(attribute))
    new=MyTestClass()
 
    print(" After making the instance the attributes defined are:")
    for attribute in dir(new):
        print('Attribute Name: %s'%(attribute))
#-------------------------------------------------------------------------------
# Module Runner

if __name__ == '__main__':
    
    test_alias()
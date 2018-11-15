#-----------------------------------------------------------------------------
# Name:        PerformanceUtils
# Purpose:     To create tools for testing performance
# Author:      Aric Sanders
# Created:     8/18/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Types contains type definitions to fix python 2->3 migration issues

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

#-----------------------------------------------------------------------------
# Third Party Imports

#-----------------------------------------------------------------------------
# Module Constants
StringType=str
ListType=list
IntType=int
FloatType=float
ComplexType=complex
LongType=float
DictionaryType=dict
type_names=["StringType","ListType","IntType","FloatType","ComplexType","LongType","DictionaryType"]
#-----------------------------------------------------------------------------
# Module Functions

#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    for index,type in enumerate([StringType,ListType,IntType,FloatType,ComplexType,LongType,DictionaryType]):

        print("The types defined here are {0} : {1}".format(type_names[index],type))


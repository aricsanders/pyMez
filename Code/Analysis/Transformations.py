#-----------------------------------------------------------------------------
# Name:        Transformations
# Purpose:    To hold data manipulations that change the content.
# Author:      Aric Sanders
# Created:     2/27/2018
# License:     MIT License
#-----------------------------------------------------------------------------
""" Transformations is a module with tools for changing data from one format to another, while not
preserving the content. It complements pyMez.Code.DataHandlers.Translations, and can be added as jumps to graph models.



 Examples
--------
    #!python



Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html)
+ [re](https://docs.python.org/2/library/re.html)
+ [datetime](https://docs.python.org/2/library/datetime.html)
+ [math](https://docs.python.org/2/library/math.html)
+ [cmath](https://docs.python.org/2/library/cmath.html)
+ [numpy](https://docs.scipy.org/doc/)
+ [scipy](https://docs.scipy.org/doc/)
+ [pandas](http://pandas.pydata.org/)
+ [matplotlib](http://matplotlib.org/)
+ [pyMez](https://github.com/aricsanders/pyMez)

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
import sys
import os
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.DataHandlers.GeneralModels import *
except:
    print("The module pyMez.Code.DataHandlers.GeneralModels was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    from Code.DataHandlers.TouchstoneModels import *
except:
    print("The module pyMez.Code.DataHandlers.TouchstoneModels was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions
def SixteenTerm_to_EightTermList(s4p_model):
    """Returns two s2p's of the error boxes, with s2p number 1, the same as S11,S13,S31,S33 of error adaptor and
    s2p number 2 as S22,S24,S42,S44 of error adaptor"""
    # sparameter_complex=[Frequency[0],S11[1],S12[2],S13[3],S14[4],S21[5],S22[6],S23[7],S24[8],S31[9],
    # S32[10],S33[11],S34[12],S41[13],S42[14],S43[15],S44[16]]
    s2p_1_complex=[[row[0],row[1],row[3],row[9],row[11]] for row in s4p_model.sparameter_complex]
    s2p_2_complex=[[row[0],row[6],row[8],row[14],row[16]] for row in s4p_model.sparameter_complex]
    s2p_1=S2PV1(sparameter_complex=s2p_1_complex)
    s2p_2=S2PV1(sparameter_complex=s2p_2_complex)
    return [s2p_1,s2p_2]

def W2p_to_SwitchTerms(w2p):
    """Creates a s2p with switch terms in port1 (reverse), port2 (foward) format given a w2p of a thru."""
    reA1_D2_index=w2p.column_names.index("reA1_D2")
    imA1_D2_index=w2p.column_names.index("imA1_D2")
    reB1_D2_index=w2p.column_names.index("reB1_D2")
    imB1_D2_index=w2p.column_names.index("imB1_D2")
    port_1=[complex(row[reA1_D2_index],row[imA1_D2_index])/complex(row[reB1_D2_index],row[imB1_D2_index]) for row in w2p.data]
    reA2_D1_index=w2p.column_names.index("reA2_D1")
    imA2_D1_index=w2p.column_names.index("imA2_D1")
    reB2_D1_index=w2p.column_names.index("reB2_D1")
    imB2_D1_index=w2p.column_names.index("imB2_D1")
    port_2=[complex(row[reA2_D1_index],row[imA2_D1_index])/complex(row[reB2_D1_index],row[imB2_D1_index]) for row in w2p.data]
    complex_sparameters=[]
    for row_index,row in enumerate(w2p.data[:]):
        new_row=[row[0],port_1[row_index],port_2[row_index]]+[complex(0,0),complex(0,0)]
        complex_sparameters.append(new_row)
    s2p_out=S2PV1(None,sparameter_complex=complex_sparameters)
    return s2p_out

def W2p_to_S2p(w2p):
    """Creates a s2p with given a w2p assumes data columns are [Frequency,reA1_D1,imA1_D1,reB1_D1,imB1_D1...imB2_D2]
    Returns the 3 -reciever sparameters or b1/a1 etc."""
    complex_sparameters=[]
    for row_index,row in enumerate(w2p.data[:]):
        # B1_D1/A1_D1
        S11=complex(row[3],row[4])/complex(row[1],row[2])
        # B2_D1/A1_D1
        S21=complex(row[7],row[8])/complex(row[1],row[2])
        # B1_D2/A2_D2
        S12=complex(row[11],row[12])/complex(row[13],row[14])
        # B2_D2/A2_D2
        S22=complex(row[15],row[16])/complex(row[13],row[14])
        new_row=[row[0],S11,S12,S21,S22]
        complex_sparameters.append(new_row)
    s2p_out=S2PV1(None,sparameter_complex=complex_sparameters)
    return s2p_out

def W1p_to_S1p(w1p):
    """Creates a s1p with given a w1p assumes data columns are [Frequency,reA1_D1,imA1_D1,reB1_D1,imB1_D1]
    returns a S1PV1 model with columns [Frequency,reS11,imS11]"""
    complex_sparameters=[]
    for row_index,row in enumerate(w1p.data[:]):
        # B1_D1/A1_D1
        S11=complex(row[3],row[4])/complex(row[1],row[2])
        new_row=[row[0],S11]
        complex_sparameters.append(new_row)
    s1p_out=S1PV1(None,sparameter_complex=complex_sparameters)
    return s1p_out

def S2p_to_S1p(s2p,column="S11"):
    """Creates an s1p from an s2p by taking column and frequency, column can be any value in ["S11","S21","S12","S22"]"""
    columns=["S11","S21","S12","S22"]
    s2p.change_data_format("RI")
    index=columns.index(column)+1
    sparameter_complex=[]
    for row_index,row in enumerate(s2p.sparameter_complex[:]):
        sparameter_complex.append([row[0],row[index]])
    options=s2p.options.copy()
    options["column_names"]=["Frequency","reS11","imS11"]
    options["sparameter_complex"]=sparameter_complex
    options["number_ports"]=1
    options["extension"]="s1p"
    s1p_out=S1PV1(None,**options)
    return s1p_out

def S1ps_to_S2p(S11_s1p,S22_s1p,S21_fill_value=complex(0,0)):
    """Creates an s2p from two s1ps by filling S11 with S11_s1p and S22 with S22_s1p and S21, and S12 with S21_fill_value,
    Default is 0+ 0i. Assumes both have the same frequency list. """
    #first make sure both s1p 's  are in the right format
    S11_s1p.change_data_format("RI")
    S22_s1p.change_data_format("RI")
    #check the frequency lists
    if len(S11_s1p.data)!=len(S22_s1p.data):
        raise
    sparameter_complex=[]
    for row_index, row in enumerate(S11_s1p.data):
        new_row=[row[0],
                 complex(row[1],row[2]),
                 S21_fill_value,
                 S21_fill_value,
                 complex(S22_s1p.data[row_index][1],S22_s1p.data[row_index][2])]
        sparameter_complex.append(new_row)
    options={}
    options["sparameter_complex"]=sparameter_complex
    s2p=S2PV1(None,**options)
    return s2p

#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass
    
#-----------------------------------------------------------------------------
# Name:        Transformations
# Purpose:    To hold data manipulations that change the content.
# Author:      Aric Sanders
# Created:     2/27/2018
# License:     MIT License
#-----------------------------------------------------------------------------
""" Transformations is a module with tools for changing data from one format to another, while not
preserving the content. It complements translations, and can be added as jumps to graph models.



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
<a href="../../../Examples/Html/Examples_Home.html">Examples Home</a> |
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
    """Creates a s2p with given a w2p assumes data columns are [Frequency,reA1_D1,imA1_D1,reB1_D1,imB1_D1...imB2_D2]"""
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
#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass
    
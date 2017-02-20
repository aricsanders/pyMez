"""
InstrumentControl is a subpackage designed for communication between a computer and the outside world. It wraps NIVisa
using the pyvisa module and integrates this wrapper with xml based instrument sheets found in
`pyMeasure.Code.DataHandlers.XMLModels` examples of the xml can be found in pyMeasure/Instruments folder.

Examples
--------
    !#python
    >>from pyMeasure import *
    >>new_instrument=VisaInstrument("GPIB::21")
    >>print(new_instrument.idn)
    >>print(instrument.ask('*IDN?'))

Help
---------------
<a href="./index.html">`pyMeasure.Code.DataHandlers`</a>
<div>
<a href="../../../pyMeasure_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Reference_Index.html">Index of all Functions and Classes in pyMeasure</a>
</div>
"""
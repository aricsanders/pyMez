"""
InstrumentControl is a subpackage designed for communication between a computer and the outside world. It wraps NIVisa
using the pyvisa module and integrates this wrapper with xml based instrument sheets found in
`pyMez.Code.DataHandlers.XMLModels` examples of the xml can be found in pyMez/Instruments folder.

Examples
--------
    !#python
    >>from pyMez import *
    >>new_instrument=VisaInstrument("GPIB::21")
    >>print(new_instrument.idn)
    >>print(instrument.ask('*IDN?'))

Help
---------------
<a href="../index.html">`pyMez.Code`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples</a> |
<a href="../../../Reference_Index.html">Index </a>
</div>
"""
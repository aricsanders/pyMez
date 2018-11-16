"""
The Analysis subpackage contains modules designed to change the content of objects created using a Model. For instance,
a function that interpolates data from a table and returns a new table would live in Analysis/Interpolation.py . If
a function or class is designed to only change the format of an object and not its content it should reside
in DataHandlers. Any module in the Analysis subpackage can import from DataHandlers, Utils or third party libraries,
 however should not import from FrontEnds or Instrument control.

 Examples
--------
<a href="../../../Examples/html/Calrep_Example.html"> How to calrep a raw data file</a>

Import Structure
----------------
Analysis typically import from Utils and DataHandlers but __NOT__ from  InstrumentControl or FrontEnds

Help
-----
<a href="../index.html">`pyMez.Code`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples</a> |
<a href="../../../Reference_Index.html">Index </a>
</div>
"""
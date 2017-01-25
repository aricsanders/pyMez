"""
The Analysis subpackage contains modules designed to change the content of objects created using a Model. For instance,
a function that interpolates data from a table and returns a new table would live in Analysis/Interpolation.py . If
a function or class is designed to only change the format of an object and not its content it should reside
in DataHandlers. Any module in the Analysis subpackage can import from DataHandlers, Utils or third party libraries,
 however should not import from FrontEnds or Instrument control.
"""
"""
The DataHandlers subpackage is designed to manipulate data, by allowing different data types to be opened,
created, saved and updated. The subpackage is further divided into modules grouped by a common theme. Classes for data
that are already on disk normally follows the following pattern:
`instance=ClassName(file_path,**options)`

For Example to
open a XML file that you don't know the model, use

`xml=pyMez.Code.DataHandlers.XMLModels.XMLBase('MyXML.xml')'

or

`xml=XMLBase('MyXML.xml')`

All data models normally have save(), str() and if appropriate show() methods.



Examples
--------
<a href="../../../Examples/How_To_Open_S2p.html"> How to open a s2p file </a>

Import Structure
----------------
DataHandlers typically import from Utils but __NOT__ from Analysis, InstrumentControl or FrontEnds

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





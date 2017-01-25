"""The DataHandlers subpackage is designed to manipulate data, by allowing different data types to be opened,
created, saved and updated. The subpackage is further divided into modules grouped by a common theme. Classes for data
that are already on disk normally follows the following pattern instance=ClassName(file_path,**options). For Example to
open a XML file that you don't know the model, use xml=pyMeasure.Code.DataHandlers.XMLModels.XMLBase('MyXML.xml').

All data models normally have save(), str() and if appropriate show() methods.

DataHandlers typically import from Utils but NOT from Analysis, InstrumentControl or FrontEnds

"""




__all__=["GeneralModels","NISTModels","TouchstoneModels","Translations"]
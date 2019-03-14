#-----------------------------------------------------------------------------
# Name:        Reports
# Purpose:    
# Author:      Aric Sanders
# Created:     1/26/2018
# License:     MIT License
#-----------------------------------------------------------------------------
"""Reports is a module dedicated to generating reports after data collection or analysis. It contains models for
basic html reports and the checkstandard reporting process.

  Examples
--------
    #!python
    >>report=HTMLReport()
    >>report.embedd_image("my.png",image_mode="PngFile")
    >>report.show()


Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html)
+ [re](https://docs.python.org/2/library/re.html)
+ [math](https://docs.python.org/2/library/math.html)
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
import os
import sys
import math
import re
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.Analysis.SParameter import *
except:
    print("Code.Analysis.SParameter did not import correctly")
    raise ImportError
try:
    from Code.Analysis.Uncertainty import *
except:
    print("Code.Analysis.Uncertainty did not import correctly")
    raise ImportError
try:
    from Code.DataHandlers.NISTModels import *
except:
    print("Code.DataHandlers.NISTModels did not import correctly")
    raise ImportError
try:
    from Code.DataHandlers.XMLModels import *
except:
    print("Code.DataHandlers.XMLModels did not import correctly")
    raise ImportError
try:
    from Code.DataHandlers.HTMLModels import *
except:
    print("Code.DataHandlers.HTMLModels did not import correctly")
    raise ImportError
try:
    from Code.DataHandlers.GraphModels import *
except:
    print("Code.DataHandlers.GraphModels did not import correctly")
    raise ImportError
try:
    from bokeh.plotting import figure
    from bokeh.embed import components
except:
    pass
#-----------------------------------------------------------------------------
# Module Constants

TWO_PORT_NR_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Two_Port_NR_Check_Standard.csv"
COMBINED_ONE_PORT_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Combined_One_Port_Check_Standard.csv"
COMBINED_TWO_PORT_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Combined_Two_Port_Check_Standard.csv"
COMBINED_POWER_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Combined_Power_Check_Standard.csv"
ONE_PORT_CALREP_CSV=r"C:\Share\Converted_DUT\One_Port_DUT.csv"
TWO_PORT_CALREP_CSV=r"C:\Share\Converted_DUT\Two_Port_DUT.csv"
POWER_3TERM_CALREP_CSV=r"C:\Share\Converted_DUT\Power_3Term_DUT.csv"
POWER_4TERM_CALREP_CSV=r"C:\Share\Converted_DUT\Power_4Term_DUT.csv"

DEFAULT_TOGGLE_SCRIPT="""<script type="text/javascript">
    function toggleId(id,$link){
    $node = document.getElementById(id);
    if (!$node)
    return;
    if (!$node.style.display || $node.style.display == 'none') {
    $node.style.display = 'block';
    $link.value = '-';
    } else {
    $node.style.display = 'none';
    $link.value = '+';
    }
  }
  </script>"""

DEFAULT_TOGGLE_STYLE="""<style>
  .toggleButton {
      background-color: white;
      border: 2px solid black;
       border-radius: 8px;
       color:red;
	   }
   .toggleButton:hover {
    box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
	}
    </stlye>"""
ONE_PORT_DTYPE={'Frequency':'float',
                 'Direction':'str',
                 'Connect':'str',
                 'System_Id':'str',
                 'System_Letter':'str',
                 'Connector_Type_Calibration':'str',
                 'Connector_Type_Measurement':'str',
                 'Measurement_Type':'str',
                 'Measurement_Date':'str',
                 'Measurement_Time':'str',
                 'Program_Used':'str',
                 'Program_Revision':'str',
                 'Operator':'str',
                 'Calibration_Name':'str',
                 'Calibration_Date':'str',
                 'Port_Used':'int',
                 'Number_Connects':'str',
                 'Number_Repeats':'str',
                 'Nbs':'str',
                 'Number_Frequencies':'str',
                 'Start_Frequency':'float',
                 'Device_Description':'str',
                 'Device_Id':'str',
                 'Measurement_Timestamp':'str',
                }
#-----------------------------------------------------------------------------
# Module Functions
def bokeh_parse_format_string(format_string):
    """Returns a string with color and a list with string styles [color,[style1,style2..]]to be given to bokeh plot"""
    style_dictionary={"*":"asterisk",
                     "o":"circle",
                     "o+":"circle_cross",
                     "ox":"circle_x",
                     "+":"cross",
                     "--":"dash",
                     "d":"diamond",
                     "d+":"diamond_cross",
                     "v":"inverted_triangle",
                     "sq":"square",
                     "sq+":"square_cross",
                     "sqx":"square_x",
                     "^":"triangle",
                     "x":"x",
                     "-":"line"}
    color_dictionary={"r":"red",
                      "b":"blue",
                      "k":"black",
                      "w":"white",
                      "g":"green",
                      "c":"cyan",
                      "m":"magenta",
                      "y":"yellow"}
    remaining_code=format_string
    color="blue"
    for color_code in color_dictionary.keys():
        if re.match(color_code,remaining_code):
            color=color_dictionary[color_code]
            remaining_code=remaining_code.replace(color_code,"")
    styles=[]
    if "--" in remaining_code:
        style="dash"
        styles.append(style)
        remaining_code=remaining_code.replace("--","")

    i=0
    sorted_style_keys=sorted(style_dictionary.keys())[::-1]
    while ((remaining_code!="") or (i<len(style_dictionary.keys())-1)):
        style_key=sorted_style_keys[i]

        if re.search(re.escape(style_key),remaining_code):
            styles.append(style_dictionary[style_key])
            remaining_code=remaining_code.replace(style_key,"")
        i+=1
    return [color,styles]
#-----------------------------------------------------------------------------
# Module Classes
class HTMLReport(HTMLBase):
    def add_toggle_script(self, script=DEFAULT_TOGGLE_SCRIPT):
        """Adds a javascript template toggle script to the body of the HTML"""
        self.append_to_body(script)

    def add_toggle_style(self, style=DEFAULT_TOGGLE_STYLE):
        """Adds a css to format the javascript template, should be done once"""
        self.append_to_head(style)

    def add_toggle(self, tag_id=None):
        """Adds a toggle button that toggles the element with id tag_id. This can be used many times """
        toggle = '<input type="button" class="toggleButton"  value="+" onclick="toggleId(\'{0}\',this)">'.format(tag_id)
        self.append_to_body(toggle)

    def embedd_image(self, image, image_mode="MatplotlibFigure", **options):
        """Embedds an image in the report. image_mode can be  MatplotlibFigure (a reference to the figure class),
        Image (the PIL class),
        Base64 (a string of the values),
        Png, Jpg, Bmp Tiff(the file name),
        or a Ndarray of the image values"""
        # might change this to self.ImageGraph and use it elsewhere
        image_graph = ImageGraph()
        image_graph.set_state(image_mode, image)
        image_graph.move_to_node("EmbeddedHtml")
        self.append_to_body(image_graph.data)

    def embedd_image_figure(self, image, image_mode="MatplotlibFigure", figure_id="image", caption="", style="",
                            **options):
        """Embedds an image in the report. image_mode can be  MatplotlibFigure (a reference to the figure class),
        Image (the PIL class),
        Base64 (a string of the values),
        Png, Jpg, Bmp Tiff(the file name),
        or a Ndarray of the image values. The image is in a <figure id=figure_id> tag"""
        # might change this to self.ImageGraph and use it elsewhere
        image_graph = ImageGraph()
        image_graph.set_state(image_mode, image)
        image_graph.move_to_node("EmbeddedHtml")
        self.append_to_body("<figure id='{0}' style='{3}'>{1}<figcaption>{2}</figcaption></figure>".format(figure_id,
                                                                                                           image_graph.data,
                                                                                                           caption,
                                                                                                           style))

    def add_download_link(self, content_string, text="Download File", suggested_name="test.txt",
                          mime_type="text/plain"):
        """Adds a download link to the report"""
        self.append_to_body(String_to_DownloadLink(content_string, text=text,
                                                   suggested_name=suggested_name,
                                                   mime_type=mime_type))

    def clear(self):
        """Clears all content in the HTML"""
        element_list = self.root.getchildren()
        for child in element_list:
            self.root.remove(child)


class BokehReport(HTMLReport):
    def __init__(self):
        self.cdn_script_string = """<script src="https://cdn.pydata.org/bokeh/release/bokeh-0.13.0.min.js"></script>"""
        self.cdn_css_string = """<link href="https://cdn.pydata.org/bokeh/release/bokeh-0.13.0.min.css" rel="stylesheet" type="text/css">"""
        HTMLReport.__init__(self)
        self.add_head()
        self.add_body()
        self.append_to_head(self.cdn_css_string)
        self.append_to_head(self.cdn_script_string)
        self.figures = []
        self.div_elements = []
        self.script_elements = []

    def plot(self, x_data, y_data, format="", **options):
        """Creates an interactive plot using bokeh and appends to the body"""
        defaults = {"tools": "pan,box_zoom,reset,save",
                    "title": None,
                    "plot_width": 400,
                    "plot_height": 400,
                    "styles": ["line"],
                    "color": "gray",
                    "figure_index": False,
                    "glyph_options": {}}
        self.plot_options = {}
        for key, value in defaults.items():
            self.plot_options[key] = value
        for key, value in options.items():
            self.plot_options[key] = value
        figure_option_keys = ["tools", "title", "plot_width", "plot_height", "active_drag", "active_inspect",
                              "active_scroll", "active_tap", "tooltips"]
        figure_options = {}
        for key in self.plot_options.keys():
            if key in figure_option_keys:
                figure_options[key] = self.plot_options[key]

        if self.plot_options["figure_index"] is not False:
            plot = self.figures[self.plot_options["figure_index"]]
        else:
            plot = figure(**figure_options)
            self.figures.append(plot)
        if format:
            [color, styles] = bokeh_parse_format_string(format)
        else:
            [color, styles] = [self.plot_options["color"], self.plot_options["styles"]]
        for style in styles:
            if style in ["line"]:
                plotter = getattr(plot, style)
                plotter(x_data, y_data, line_color=color, **self.plot_options["glyph_options"])
            elif style is "dash":
                plot.line(x_data, y_data, line_dash="dashed")
            else:
                plotter = getattr(plot, style)
                plotter(x_data, y_data, fill_color=color, line_color=color, **self.plot_options["glyph_options"])

        script, div = components(plot)

        if self.plot_options["figure_index"] is not False:
            figure_index = self.plot_options["figure_index"]
            self.root.head.remove(self.script_elements[figure_index])
            self.append_to_head(str(script))
            self.script_elements[figure_index] = self.root.head.getchildren()[-1]
            new_div_element = lxml.etree.fromstring(str(div))
            self.div_elements[figure_index].attrib["id"] = new_div_element.attrib["id"]
        else:
            self.append_to_head(str(script))
            self.append_to_body(str(div))
            self.div_elements.append(self.root.body.getchildren()[-1])
            self.script_elements.append(self.root.head.getchildren()[-1])

class CheckStandardReport(HTMLReport):
    """Class that creates a report based on a calibrated measurement of a checkstandard. Input can be a file path to
    any of the ascii data
    types returned by the modified measlp program or a multiconnect mulitdirectional set of
    measurements in magnitude / angle format.
    The locations of the
    CheckStandard data bases in csv format and the directory of the results files are required.
    The report is composed of:
    1. A plot of the raw file
    2. A plot of the file with calrep style errors
    3. A plot comparing the file with calrep style errors to the old results database
    4. A plot comparing the difference of the file to the old results database
    5. A plot comparing the file with calrep style errors to the mean of the new database with outliers excluded
    6. A history plot of the check standard for the current measurement and the last n measurements (default is 5)
    7. A complete history plot of the check standard
    8. A set of download links in text and the formats set in options

    If no file is specified and a checkstandard_name is, then only history and means of that checkstandard are shown in the
    report"""

    def __init__(self, file_path=None, **options):
        """Initializes the CheckStandardReport Class"""
        defaults = {"Device_Id": "CTN112",
                    "results_directory": r'C:\Share\resfiles',
                    "one_port_csv": COMBINED_ONE_PORT_CHKSTD_CSV,
                    "two_port_csv": COMBINED_TWO_PORT_CHKSTD_CSV,
                    "two_port_nr_csv": TWO_PORT_NR_CHKSTD_CSV,
                    "power_csv": COMBINED_POWER_CHKSTD_CSV,
                    "outlier_removal": True,
                    "last_n": 5,
                    "download_formats": ["Csv"],
                    "conversion_options":{
                                    "nodes": ['CsvFile', 'ExcelFile'],
                                    "extensions": [ 'csv', 'xlsx'],
                                    "mime_types": ['text/plain',
                                                   'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']}
                    }
        self.options = {}
        for key, value in defaults.items():
            self.options[key] = value
        for key, value in options.items():
            self.options[key] = value
        self.conversion_defaults = {"base_name": None,
                                    "nodes": ['XmlFile', 'CsvFile', 'ExcelFile', 'OdsFile', 'MatFile', 'HtmlFile',
                                              'JsonFile'],
                                    "extensions": ['xml', 'csv', 'xlsx', 'ods', 'mat', 'html', 'json'],
                                    "mime_types": ['application/xml', 'text/plain',
                                                   'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                                   'application/vnd.oasis.opendocument.spreadsheet',
                                                   'application/x-matlab-data', 'text/html', 'application/json']}
        # html_options={}
        if self.options["conversion_options"] is None:
            self.conversion_options=self.conversion_defaults
        else:
            self.conversion_options=self.options["conversion_options"]
        HTMLReport.__init__(self, None, **self.options)
        self.plots = []
        self.plot_ids = []
        self.plot_titles = []
        self.plot_captions = []
        # set up dtypes for pandas
        one_port_dtype = ONE_PORT_DTYPE
        # this reads the NISTModels constant
        if COMBINE_S11_S22:
            one_port_dtype["arg"] = 'float'
            one_port_dtype["mag"] = 'float'
        else:
            one_port_dtype["argS11"] = 'float'
            one_port_dtype["magS11"] = 'float'
            one_port_dtype["argS22"] = 'float'
            one_port_dtype["magS22"] = 'float'
        # create a history dictionary.
        # print("{0} is {1}".format("self.options",self.options))
        self.history_dict = {'1-port': pandas.read_csv(self.options["one_port_csv"], dtype=one_port_dtype),
                             '2-port': pandas.read_csv(self.options["two_port_csv"]),
                             '2-portNR': pandas.read_csv(self.options["two_port_nr_csv"]),
                             'power': pandas.read_csv(self.options["power_csv"])}

        if file_path is None:
            # plot the results file
            self.build_checkstandard_report()
        else:
            self.build_comparison_report(file_path)

    def build_checkstandard_report(self):
        """Builds the report for the options Device_Id"""
        self.raw_measurement=None
        self.calrep_measurement=None
        self.clear()
        self.plots = []
        self.plot_ids = []
        self.plot_captions = []
        self.plot_titles = []
        measurement_type = self.options["Device_Id"][-3]
        if re.match("1", measurement_type):
            self.options["Measurement_Type"] = "1-port"
        elif re.match("2", measurement_type):
            self.options["Measurement_Type"] = "2-port"
        elif re.match("p", measurement_type, re.IGNORECASE):
            self.options["Measurement_Type"] = "power"
        print(("{0} is {1}".format("measurement_type",measurement_type)))
        try:
            self.results_file = ResultFileModel(os.path.join(self.options["results_directory"], self.options["Device_Id"]))
        except:
            self.results_file=ResultFileModel(None)
        options = {"Device_Id": self.options["Device_Id"], "System_Id": None, "Measurement_Timestamp": None,
                   "Connector_Type_Measurement": None,
                   "Measurement_Date": None, "Measurement_Time": None, "outlier_removal": False}
        if re.search('2-port', self.options["Measurement_Type"], re.IGNORECASE):
            history_key = '2-port'
            options["column_names"] = ['Frequency', 'magS11', 'argS11', 'magS21', 'argS21', 'magS22', 'argS22']

        elif re.search('1-port', self.options["Measurement_Type"], re.IGNORECASE):
            history_key = '1-port'
            if COMBINE_S11_S22:
                options["column_names"] = ['Frequency', 'magS11', 'argS11']
            else:
                options["column_names"] = ['Frequency', 'magS11', 'argS11', 'magS22', 'argS22']
        elif re.search('Dry Cal|Thermistor|power', self.options["Measurement_Type"], re.IGNORECASE):
            history_key = 'power'
            options["column_names"] = ['Frequency', 'magS11', 'argS11', 'Efficiency']
        # print history[history_key][:5]
        # print history_key
        database = self.history_dict[history_key]
        self.device_history = database[database["Device_Id"] == self.options["Device_Id"]]
        if self.options["outlier_removal"]:
            self.outlier_removal()
        self.mean_frame = mean_from_history(self.device_history, **options)
        self.plots.append(plot_checkstandard_history(self.device_history))
        self.plot_ids.append("completeHistory")
        self.plot_titles.append("The Complete History of {0}".format(self.options["Device_Id"]))
        self.plot_captions.append("""Figure {0}. Every measurement of {1} currently
        in the database.""".format(len(self.plots), self.options["Device_Id"]))

        self.plots.append(plot_checkstandard_history(self.device_history,
                                                     min_num=len(self.get_measurement_dates()) - self.options[
                                                         "last_n"] - 1,
                                                     max_num=len(self.get_measurement_dates()) - 1,
                                                     extra_plots=[self.results_file,
                                                                  self.mean_frame],
                                                     extra_plot_labels=["Historical Database", "Mean of New Database"],
                                                     extra_plot_formats=["r--", "k^"]))
        self.plot_ids.append("partialHistory")
        self.plot_titles.append("""The last {0} measurements of {1}
        compared with the historical database and mean. """.format(self.options["last_n"], self.options["Device_Id"]))
        self.plot_captions.append("""Figure {0}. Last  {1} measurements of {2}
        compared with historical database and mean""".format(len(self.plots),
                                                             self.options["last_n"], self.options["Device_Id"]))

        self.add_toggle_support()
        summary_text = """
        This device has been measured {0} times from {1} to {2}""".format(len(self.get_measurement_dates()),
                                                                          min(self.get_measurement_dates()),
                                                                          max(self.get_measurement_dates()))
        self.add_report_heading()
        self.append_to_body({"tag": "p", "text": summary_text})

        download_options={"mime_types":self.conversion_options["mime_types"],
         "download_formats":self.conversion_options["nodes"],
         "download_extensions":self.conversion_options["extensions"],
         "clear_before": False,
         "download_files": [self.results_file,
                            self.mean_frame, self.device_history],
         "download_files_input_format": ["AsciiDataTable", "DataFrame",
                                         "DataFrame"],
         "download_files_base_names": ["Historical_Database.txt",
                                       "Mean_Database.txt",
                                       "Device_History.txt"],
         "style": "display:none;border:1;"}
        self.add_download_table(**download_options)
        self.add_all_plots()

    def build_comparison_report(self, raw_file_path=None):
        """Builds the report for a raw file comparison, requires a raw_file_path to process"""
        self.clear()
        self.plots = []
        self.plot_ids = []
        self.plot_captions = []
        self.plot_titles = []
        self.raw_measurement_model = sparameter_power_type(raw_file_path)
        self.raw_measurement = globals()[self.raw_measurement_model](raw_file_path)
        # print("{0} is {1}".format("self.raw_measurement.column_names",self.raw_measurement.column_names))
        table = self.raw_measurement
        self.options["Device_Id"] = table.metadata["Device_Id"]
        self.plots.append(self.raw_measurement.show())
        self.plot_ids.append("rawMeasurement")
        self.plot_titles.append("Raw Measurement of {0}".format(self.options["Device_Id"]))
        self.plot_captions.append("""Figure {0}. Raw measurement of {1}. The measurement of check standard {1}
        in a calibrated mode.""".format(len(self.plots), self.options["Device_Id"]))
        self.calrep_measurement = calrep(self.raw_measurement)
        self.plots.append(plot_calrep(self.calrep_measurement))
        self.plot_ids.append("clarepMeasurement")
        self.plot_titles.append("Plot of {0} with uncertainty".format(self.options["Device_Id"]))
        self.plot_captions.append("""Figure {0}. Measurement of {1}. The measurement of check standard {1}
        with nist total uncertainty.""".format(len(self.plots), self.options["Device_Id"]))
        self.plots.append(plot_calrep_uncertainty(self.calrep_measurement))
        self.plot_ids.append("clarepUncert")
        self.plot_titles.append("Plot  Uncertainty Components".format(self.options["Device_Id"]))
        self.plot_captions.append("""Figure {0}. Uncertainty Components.
        The uncertainty in measurement of check standard {1}
        .""".format(len(self.plots), self.options["Device_Id"]))
        try:
            self.results_file = ResultFileModel(os.path.join(self.options["results_directory"],
                                                             self.calrep_measurement.metadata["Device_Id"]))
        except:
            self.results_file = None
        options = {"Device_Id": table.metadata["Device_Id"], "System_Id": table.metadata["System_Id"],
                   "Measurement_Timestamp": None,
                   "Connector_Type_Measurement": table.metadata["Connector_Type_Measurement"],
                   "Measurement_Date": None, "Measurement_Time": None, "outlier_removal": False}
        if re.search('2-port',
                     table.metadata["Measurement_Type"],
                     re.IGNORECASE) and not re.search('2-portNR',
                                                      table.metadata["Measurement_Type"],
                                                      re.IGNORECASE):
            history_key = '2-port'
            options["column_names"] = ['Frequency', 'magS11', 'argS11', 'magS21', 'argS21', 'magS22', 'argS22']
        elif re.search('2-portNR', table.metadata["Measurement_Type"], re.IGNORECASE):
            history_key = '2-portNR'
            options["column_names"] = ['Frequency', 'magS11', 'argS11', 'magS12', 'argS12', 'magS21', 'argS21',
                                       'magS22', 'argS22']
        elif re.search('1-port', table.metadata["Measurement_Type"], re.IGNORECASE):
            history_key = '1-port'
            if COMBINE_S11_S22:
                options["column_names"] = ['Frequency', 'magS11', 'argS11']
            else:
                options["column_names"] = ['Frequency', 'magS11', 'argS11', 'magS22', 'argS22']
        elif re.search('Dry Cal|Thermistor|power', table.metadata["Measurement_Type"], re.IGNORECASE):
            history_key = 'power'
            options["column_names"] = ['Frequency', 'magS11', 'argS11', 'Efficiency']
        # print history[history_key][:5]
        # print history_key
        database = self.history_dict[history_key]
        self.device_history = database[database["Device_Id"] == self.options["Device_Id"]]
        if self.options["outlier_removal"]:
            self.outlier_removal()
        self.mean_frame = mean_from_history(self.device_history.copy(), **options)
        # print mean_frame
        self.difference_frame = raw_difference_frame(table, self.mean_frame)
        # print("{0} is {1}".format("self.raw_measurement.column_names",self.raw_measurement.column_names))
        # print difference_frame
        self.plots.append(raw_comparison_plot_with_residuals(table, self.mean_frame, self.difference_frame))
        self.plot_ids.append("rawSummary")
        self.plot_titles.append("Summary of Measurement and Mean of Complete Database with Resisduals")
        self.plot_captions.append("""Figure {0}. Summary of Measurement and Mean with Resisduals.
        Data for all measurements are being used""".format(len(self.plots)))
        #         stop_time=datetime.datetime.now()
        #         diff=stop_time-start_time
        self.plots.append(plot_calrep_results_comparison(self.calrep_measurement, self.results_file,
                                                         display_legend=True))
        self.plot_ids.append("compareWithUncertainty")
        self.plot_titles.append("Measurement with Uncertainties compared with Historical Database")
        self.plot_captions.append("""Figure {0}. Measurement with Uncertainties compared with Historical Database.
        This is the current selection criteria""".format(len(self.plots)))

        self.plots.append(plot_calrep_results_difference_comparison(self.calrep_measurement,
                                                                    self.results_file,
                                                                    display_legend=True))
        self.plot_ids.append("compareWithUncertaintyDifference")
        self.plot_titles.append("The Difference of Measurement with Uncertainties compared with Historical Database")
        self.plot_captions.append("""Figure {0}. The Difference of Measurement with Uncertainties
        compared with Historical Database.
        This is the current selection criteria.""".format(len(self.plots)))

        column_names = return_calrep_value_column_names(self.calrep_measurement)
        error_column_names = return_calrep_error_column_names(column_names)
        self.standard_error = standard_error_data_table(self.calrep_measurement, self.results_file,
                                                        table_1_uncertainty_column_names=error_column_names,
                                                        value_column_names=column_names, expansion_factor=1)
        number_columns_pass = list(self.standard_error.get_conformation_dictionary().values()).count(True)
        number_columns = len(list(self.standard_error.get_conformation_dictionary().values()))
        good = int(round(float(number_columns_pass - 1) / float(number_columns - 1)))
        pass_fail = ""
        if good:
            pass_fail = "PASSES"
        else:
            pass_fail = "FAILS"
        self.plots.append(self.standard_error.show())
        self.plot_ids.append("standardErrror")
        self.plot_titles.append(
            "The Standard Error of Measurement with Uncertainties compared with Historical Database")
        self.plot_captions.append("""Figure {0}. The Standard Error of Measurement with Uncertainties
        compared with Historical Database.
        This is the current selection criteria.""".format(len(self.plots)))

        self.plots.append(plot_checkstandard_history(self.device_history))
        self.plot_ids.append("completeHistory")
        self.plot_titles.append("The Complete History of {0}".format(self.options["Device_Id"]))
        self.plot_captions.append("""Figure {0}. Every measurement of {1} currently
        in the database.""".format(len(self.plots), self.options["Device_Id"]))

        self.plots.append(plot_checkstandard_history(self.device_history,
                                                     min_num=len(self.get_measurement_dates()) - self.options[
                                                         "last_n"] - 1,
                                                     max_num=len(self.get_measurement_dates()) - 1,
                                                     extra_plots=[self.results_file,
                                                                  self.mean_frame],
                                                     extra_plot_labels=["Historical Database", "Mean of New Database"],
                                                     extra_plot_formats=["r--", "k^"]))
        self.plot_ids.append("partialHistory")
        self.plot_titles.append("""The last {0} measurements of {1}
        compared with the historical database and mean. """.format(self.options["last_n"], self.options["Device_Id"]))
        self.plot_captions.append("""Figure {0}. Last  {1} measurements of {2}
        compared with historical database and mean""".format(len(self.plots),
                                                             self.options["last_n"], self.options["Device_Id"]))

        self.add_toggle_support()
        summary_text = """This is a summary of the measurement of {0} made on {1} by {2}. This measurement
        {3} the checkstandard process.
        This device has been measured {4} times from {5} to {6}""".format(self.options["Device_Id"],
                                                                          self.raw_measurement.metadata[
                                                                              "Measurement_Date"],
                                                                          self.raw_measurement.metadata["Operator"],
                                                                          pass_fail,
                                                                          len(self.get_measurement_dates()),
                                                                          min(self.get_measurement_dates()),
                                                                          max(self.get_measurement_dates()))
        self.add_report_heading()
        self.append_to_body({"tag": "p", "text": summary_text})

        self.add_download_table(download_extensions=self.conversion_options["extensions"],
                                download_formats=self.conversion_options["nodes"],
                                mime_types=self.conversion_options["mime_types"])
        self.add_table_border_style()
        self.add_metadata_section()
        self.add_all_plots()

    def get_measurement_dates(self):
        """Returns measurement dates from self.device_history"""
        dates = sorted(self.device_history["Measurement_Timestamp"].unique())
        self.measurement_dates = dates[:]
        return dates

    def outlier_removal(self):
        """Removes outliers frome self.device_history"""
        mean_s11 = np.mean(self.device_history["magS11"])
        std_s11 = np.std(self.device_history["magS11"])
        self.device_history = self.device_history[self.device_history["magS11"] < (mean_s11 + 3 * std_s11)]
        self.device_history = self.device_history[self.device_history["magS11"] > (mean_s11 - 3 * std_s11)]

    def add_all_plots(self, **options):
        """Adds all plots in the attribute self.plots"""
        defaults = {"clear_before": False,
                    "style": "display:none",
                    "figure_width": 14}
        add_options = {}
        for key, value in defaults.items():
            add_options[key] = value
        for key, value in options.items():
            add_optionss[key] = value
        if add_options["clear_before"]:
            self.clear()
        for index, plot in enumerate(self.plots):
            id_text = self.plot_ids[index]
            self.append_to_body({"tag": "hr"})
            self.append_to_body({"tag": "h2", "text": self.plot_titles[index]})
            self.add_toggle(id_text)
            plot.set_figwidth(add_options["figure_width"])
            self.embedd_image_figure(plot, figure_id="{0}".format(id_text),
                                     style=add_options["style"], caption=self.plot_captions[index])
            self.append_to_body({"tag": "hr"})

    def add_report_heading(self, heading_text=None, **options):
        """Adds a heading to the report, clears the report by default"""
        defaults = {"clear_before": False}
        add_options = {}
        for key, value in defaults.items():
            add_options[key] = value
        for key, value in options.items():
            add_options[key] = value
        if add_options["clear_before"]:
            self.clear()
        if heading_text is None:
            heading_text = "Check Standard Report for {0}".format(self.options["Device_Id"])
        self.append_to_body({"tag": "h1", "text": heading_text})

    def add_toggle_support(self):
        """Adds a toggle style and script to the report"""
        self.add_toggle_script()
        self.add_toggle_style()

    def add_download_table(self,
                           download_formats=["CsvFile", "ExcelFile"],
                           download_extensions=["csv", "xlsx"],
                           mime_types=["text/plain",
                                       'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
                           **options):
        """Adds a table of downloadable files"""
        defaults = {"clear_before": False,
                    "download_files": [self.raw_measurement, self.calrep_measurement, self.results_file,
                                       self.mean_frame, self.device_history],
                    "download_files_input_format": ["AsciiDataTable", "AsciiDataTable", "AsciiDataTable", "DataFrame",
                                                    "DataFrame"],
                    "download_files_base_names": ["Raw_Measurement.txt",
                                                  "Measurement_NIST_Uncertainties.txt",
                                                  "Historical_Database.txt",
                                                  "Mean_Database.txt",
                                                  "Device_History.txt"],
                    "style": "display:none;border:1;"}

        add_options = {}
        for key, value in defaults.items():
            add_options[key] = value
        for key, value in options.items():
            add_options[key] = value
        if add_options["clear_before"]:
            self.clear()
        self.append_to_body({"tag": "h2", "text": "Downloads"})
        self.add_toggle("downloads")
        table_graph = TableGraph()
        # convert all data to AsciiDataTable format
        download_table = "<table id='downloads' style='{0}'>".format(add_options["style"])
        for index, download in enumerate(add_options["download_files"][:]):
            try:
                if add_options["download_files_input_format"][index] not in ["AsciiDataTable"]:
                    table_graph.set_state(add_options["download_files_input_format"][index], download)
                    table_graph.move_to_node("AsciiDataTable")
                    download = table_graph.data.copy()
                # now we cycle throught the download formats, for each file we load the graph and then create the download links
                ascii_download = String_to_DownloadLink(string=str(download),
                                                        mime_type="text/plain",
                                                        suggested_name=add_options["download_files_base_names"][index],
                                                        text=add_options["download_files_base_names"][index])
                #print(("{0} is {1}".format("index", index)))
                table_graph.set_state("AsciiDataTable", download)

                download_links = TableGraph_to_Links(table_graph,
                                                     base_name=add_options["download_files_base_names"][index],
                                                     nodes=download_formats,
                                                     extensions=download_extensions,
                                                     mime_types=mime_types)

                download_table = download_table + "<tr><td>{0}</td><td>{1}</td></tr>".format(ascii_download, download_links)
            except:
                print("Could not add file ")
        download_table = download_table + "</table>"
        self.append_to_body(download_table)
        self.append_to_body({"tag": "hr"})

    def add_metadata_section(self, style="display:none;border: 1px solid black;"):
        """Adds a metadata section if self.raw_measurement exits"""
        try:
            self.append_to_body({"tag": "h2", "text": "Measurement Metadata"})
            self.add_toggle("metadata")
            self.append_to_body({"tag": "hr"})
            meta_table = "<table id='metadata' style='{0}'>".format(style)
            for key, value in self.raw_measurement.metadata.items():
                meta_table = meta_table + "<tr><td>{0}</td><td>{1}</td></tr>".format(key, value)
            meta_table = meta_table + "</table>"
            self.append_to_body(meta_table)
        except:
            pass

    def add_table_border_style(self):
        """Adds a css style tag to the head of the sheet to display all borders"""
        self.append_to_head({"tag": "style", "text": """table, th, td {
        border: 1px solid black;}"""})


#-----------------------------------------------------------------------------
# Module Scripts
def test_CheckStandardReport(raw_file_path=os.path.join(TESTS_DIRECTORY,'CTN208.R1_062614')):
        """Tests the checkstandard report class"""
        report=CheckStandardReport(raw_file_path)
        report.show()

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    test_CheckStandardReport()
    
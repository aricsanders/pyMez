#-----------------------------------------------------------------------------
# Name:        Reports
# Purpose:    
# Author:      Aric Sanders
# Created:     1/26/2018
# License:     MIT License
#-----------------------------------------------------------------------------
"""Reports is a module dedicated to generating reports after data collection or analysis

  Examples
--------
    #!python


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
<a href="../../../Examples/Html/Examples_Home.html">Examples Home</a> |
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
#-----------------------------------------------------------------------------
# Module Constants
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
        image_graph.move_to_node("embeddedHTML")
        self.append_to_body(image_graph.data)

    def embedd_image_figure(self, image, image_mode="MatplotlibFigure", figure_id="image", caption="", **options):
        """Embedds an image in the report. image_mode can be  MatplotlibFigure (a reference to the figure class),
        Image (the PIL class),
        Base64 (a string of the values),
        Png, Jpg, Bmp Tiff(the file name),
        or a Ndarray of the image values. The image is in a <figure id=figure_id> tag"""
        # might change this to self.ImageGraph and use it elsewhere
        image_graph = ImageGraph()
        image_graph.set_state(image_mode, image)
        image_graph.move_to_node("embeddedHTML")
        self.append_to_body("<figure id='{0}'>{1}<figcaption>{2}</figcaption></figure>".format(figure_id,
                                                                                               image_graph.data,
                                                                                               caption))

    def add_download_link(self, content_string, text="Download File", suggested_name="test.txt",
                          mime_type="text/plain"):
        """Adds a download link to the report"""
        self.append_to_body(String_to_DownloadLink(content_string, text=text,
                                                   suggested_name=suggested_name,
                                                   mime_type=mime_type))


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
                    }
        self.options = {}
        for key, value in defaults.iteritems():
            self.options[key] = value
        for key, value in options.iteritems():
            self.options[key] = value

        # html_options={}

        HTMLReport.__init__(self, None, **self.options)
        self.plots = {}
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
        self.clear()
        measurement_type = self.options["Device_Id"][-3]
        if re.match("1", measurement_type):
            self.options["Measurement_Type"] = "1-port"
        elif re.match("2", measurement_type):
            self.options["Measurement_Type"] = "2-port"
        elif re.match("p", measurement_type, re.IGNORECASE):
            self.options["Measurement_Type"] = "2-port"

        self.results_file = ResultFileModel(os.path.join(self.options["results_directory"], self.options["Device_Id"]))
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
            options["column_names"] = ['Frequency', 'magS11', 'argS11', 'Efficiency', 'Calibration_Factor']
        # print history[history_key][:5]
        # print history_key
        database = self.history_dict[history_key]
        self.device_history = database[database["Device_Id"] == self.options["Device_Id"]]

        self.mean_frame = mean_from_history(self.device_history, **options)

    def build_comparison_report(self, raw_file_path=None):
        """Builds the report for a raw file comparison, requires a raw_file_path to process"""
        self.clear()
        self.raw_measurement_model = sparameter_power_type(raw_file_path)
        self.raw_measurement = globals()[self.raw_measurement_model](raw_file_path)
        # print("{0} is {1}".format("self.raw_measurement.column_names",self.raw_measurement.column_names))
        table = self.raw_measurement
        self.plots["raw_plot"] = self.raw_measurement.show();
        self.calrep_measurement = calrep(self.raw_measurement)
        self.plots["calrep_plot"] = plot_calrep(self.calrep_measurement);
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
            options["column_names"] = ['Frequency', 'magS11', 'argS11', 'Efficiency', 'Calibration_Factor']
        # print history[history_key][:5]
        # print history_key
        database = self.history_dict[history_key]
        self.device_history = database[database["Device_Id"] == self.options["Device_Id"]]

        self.mean_frame = mean_from_history(self.device_history.copy(), **options)
        # print mean_frame
        self.difference_frame = raw_difference_frame(table, self.mean_frame)
        # print("{0} is {1}".format("self.raw_measurement.column_names",self.raw_measurement.column_names))
        # print difference_frame
        self.plots["raw_compare_figure"] = raw_comparison_plot_with_residuals(table, self.mean_frame,
                                                                              self.difference_frame)
        #         stop_time=datetime.datetime.now()
        #         diff=stop_time-start_time
        self.plots["old_database"] = plot_calrep_results_comparison(self.calrep_measurement, self.results_file,
                                                                    display_legend=True);
        self.plots["old_database_difference"] = plot_calrep_results_difference_comparison(self.calrep_measurement,
                                                                                          self.results_file,
                                                                                          display_legend=True);

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
#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass
    
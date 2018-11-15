#-----------------------------------------------------------------------------
# Name:        StatistiCALModels
# Purpose:    A wrapper for the StatistiCAL com object and some python classes and functions for interacting with it.
# Author:      Aric Sanders
# Created:     5/25/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" A wrapper for the StatistiCAL com object and some python classes and functions for interacting with it. More
information on statistical can be found at
 http://www.nist.gov/ctl/rf-technology/related-software.cfm

 Help
---------------
<a href="./index.html">`pyMez.Code.DataHandlers`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""
#-----------------------------------------------------------------------------
# Standard Imports
import sys
import os
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    import win32com.client
    import pythoncom
    WINDOWS_WRAPPER = True
    """Constant set to true if win32com and pythoncom modules are available.
    If they are not available the com interface is not defined."""
except:
    print("The win32com package is required to run StatistiCAL models")
    WINDOWS_WRAPPER=False
    # raise ImportError
try:
    from Code.DataHandlers.GeneralModels import *
except:
    print("pyMez.Code.DataHandlers.GeneralModels is required to run StatistiCAL models")
    raise ImportError
#-----------------------------------------------------------------------------
# Module Constants
SOLUTION_VECTOR_COLUMN_NAMES=["Frequency","rePort1S1_11","imPort1S1_11","rePort1S1_22","imPort1S1_22",
                              "rePort1S1_21","imPort1S1_21","rePort2S1_11","imPort2S1_11","rePort2S1_22","imPort2S1_22",
                              "rePort2Sqrt(S2_21*S2_12)","imPort2Sqrt(S2_21*S2_12)",
                              "rePort2Sqrt(S2_21/S2_12)","imPort2Sqrt(S2_21/S2_12)","reEffEps","imEffEps",
                              "reReflectionCoefficient","imReflectionCoefficient","reAdapterS11","imAdapterS11",
                              "reAdapterS22","imAdapterS22","reAdapterS21","imAdapterS21","reDUTS11","imDUTS11",
                              "reDUTS22","imDUTS22","reDUTS21","imDUTS21","reDUTS12","imDUTS12","reXTalkVNA-VNA",
                              "imXTalkVNA-VNA","reXTalkVNA-DUT","imXTalkVNA-DUT","reXTalkDUT-VNA","imXTalkDUT-VNA",
                              "reXTalkDUT-DUT","imXTalkDUT-DUT"]
"Column names for the solution vector returned by statistiCAL"
#-----------------------------------------------------------------------------
# Module Functions

#-----------------------------------------------------------------------------
# Module Classes
class StatistiCALError(Exception):
    """Error Class for the StatistiCAL Wrapper"""
    pass
if WINDOWS_WRAPPER:
    class StatistiCALWrapper():
        """The StatistiCALWrapper Class is a python wrapper on a StatistiCAL COM object, it requires the win32com python
        package to function. Class Methods and Attributes are documented in programmer's corner in the Statistical
        help.
        The Following are documented there:
        StatistiCAL.NumberOfODRPACKErrors
        StatistiCAL.SuppressErrorMessages
        StatistiCAL.ShowErrorMessages
        StatistiCAL.OpenMenu(ByVal FileName As String)
        StatistiCAL.AddToMenu(ByVal FileName As String)
        StatistiCAL.ClearStatistiCALMenu
        StatistiCAL.CalibrateData
        StatistiCAL.ShowStatistiCAL
        StatistiCAL.HideStatistiCAL
        StatistiCAL.QuitStatistiCAL
        StatistiCAL.InFocusWhileCalculating
        StatistiCAL.OutOfFocusWhileCalculating
        StatistiCAL.SaveStatistiCALReportToFile(ByVal FileName As String)
        StatistiCAL.SaveODRPACKReportToFile(ByVal FileName As String)
        StatistiCAL.SaveSolutionVectorToFile(ByVal FileName As String)
        StatistiCAL.SaveDUTSParToFile(ByVal FileName As String)
        StatistiCAL.SaveStandardUncertToFile(ByVal FileName As String)
        StatistiCAL.SaveCovarianceMatrixToFile(ByVal FileName As String)
        StatistiCAL.SaveVNACalCoefToFile(ByVal FileName As String)
        StatistiCAL.SaveCoverageFactorsToFile(ByVal FileName As String)
        StatistiCAL.SaveResidualsToFile(ByVal FileName As String)
        StatistiCAL.Successful - Always check this after a command to ensure that StatistiCAL was able to complete the
        command successfully

         """
        def __init__(self):
            """Intialize the instance of StatistiCAL"""
            # This is different than the name used in the help file, I found it by looking at regedit in windows
            try:

                pythoncom.CoInitialize()
                self.application=win32com.client.Dispatch('StatistiCAL_Plus.StatistiCAL_Plus_Cnt')
                self.Successful=self.application.Successful
                self.NumberOfODRPACKErrors=self.application.NumberOfODRPACKErrors
            except:
                raise
                raise StatistiCALError('The COM object representing StatistiCAL failed to intialize')

        def Sucess(self):
            """Checks to see if the last command by the com object executed succesfully"""
            return self.application.Successful

        def SuppressErrorMessages(self):
            """Suppresses the Error Messages Created by Statistical"""
            try:
                self.application.SuppressErrorMessages()
            except:
                raise StatistiCALError('Unable to Suppress Error Meassages')
        def ShowErrorMessages(self):
            """Shows the Error Messages Created by Statistical"""
            try:
                self.application.ShowErrorMessages()
            except:
                raise

        def OpenMenu(self,file_name=None):
            """Opens the menu specified by file_name in StatistiCAL"""
            try:
                if file_name is None:
                    raise StatistiCALError('Please Specify Menu Name')
                else:
                    self.application.OpenMenu(file_name)
            except:
                raise

        def AddToMenu(self,file_name=None):
            """Adds the file specified by file_name to a menu in StatistiCAL"""
            try:
                if file_name is None:
                    raise StatistiCALError('Please Specify Menu Name')
                else:
                    self.application.AddToMenu(file_name)
            except:
                raise

        def ClearStatistiCALMenu(self):
            """Clears the Current StatistiCAL menu"""
            try:
                self.application.ClearStatistiCALMenu()
            except:
                raise

        def CalibrateData(self):
            """Calibrates the data using the menu data and the standard definitions"""
            try:
                self.ShowStatistiCAL()
                self.application.CalibrateData()
                print(("The command executed sucessfully {0}".format(self.Succesfull())))

            except :
                # This a little lazy, I should catch com_error but I don't know its parent module
                pass
                #raise


        def ShowStatistiCAL(self):
            """Shows the visual basic 6 GUI of StatistiCAL"""
            try:
                self.application.ShowStatistiCAL()
            except:
                raise

        def HideStatistiCAL(self):
            """Hides the visual basic 6 GUI of StatistiCAL"""
            try:
                self.application.HideStatistiCAL()
            except:
                raise

        def QuitStatistiCAL(self):
            """Quits the visual basic 6 GUI of StatistiCAL"""
            try:
                self.application.QuitStatistiCAL()
                del self
            except:
                raise
        def InFocusWhileCalculating(self):
            """Keeps the visual basic 6 GUI of StatistiCAL in focus while calculating"""
            try:
                self.application.InFocusWhileCalculating()
            except:
                raise

        def OutOfFocusWhileCalculating(self):
            """Keeps the visual basic 6 GUI of StatistiCAL out of focus while calculating"""
            try:
                self.application.InFocusWhileCalculating()
            except:
                raise


        def SaveStatistiCALReportToFile(self,file_name=None):
            """Saves the statistiCAL report to file_name"""
            try:
                if file_name is None:
                    raise StatistiCALError('Please Specify File Name')
                else:
                    self.application.SaveStatistiCALReportToFile(file_name)
            except:
                raise

        def SaveODRPACKReportToFile(self,file_name=None):
            """Saves the ODRPACK report to file_name"""
            try:
                if file_name is None:
                    raise StatistiCALError('Please Specify File Name')
                else:
                    self.application.SaveODRPACKReportToFile(file_name)
            except:
                raise

        def SaveSolutionVectorToFile(self,file_name=None):
            """Saves the solution vector to file_name"""
            try:
                if file_name is None:
                    raise StatistiCALError('Please Specify File Name')
                else:
                    self.application.SaveSolutionVectorToFile(file_name)
            except:
                raise

        def SaveDUTSParToFile(self,file_name=None):
            """Saves the device under test(s) specified in standards to file_name"""
            try:
                if file_name is None:
                    raise StatistiCALError('Please Specify File Name')
                else:
                    self.application.SaveDUTSParToFile(file_name)
            except:
                raise

        def SaveStandardUncertToFile(self,file_name=None):
            """Saves the standard uncertainity to file_name"""
            try:
                if file_name is None:
                    raise StatistiCALError('Please Specify File Name')
                else:
                    self.application.SaveStandardUncertToFile(file_name)
            except:
                raise

        def SaveCovarianceMatrixToFile(self,file_name=None):
            """Saves the covariance matrix to file_name"""
            try:
                if file_name is None:
                    raise StatistiCALError('Please Specify File Name')
                else:
                    self.application.SaveCovarianceMatrixToFile(file_name)
            except:
                raise

        def SaveVNACalCoefToFile(self,file_name=None):
            """Saves the VNA Calibration Coefficents to file_name"""
            try:
                if file_name is None:
                    raise StatistiCALError('Please Specify Menu Name')
                else:
                    self.application.SaveVNACalCoefToFile(file_name)
            except:
                raise

        def SaveCoverageFactorsToFile(self,file_name=None):
            """Saves the coverage factors to file_name"""
            try:
                if file_name is None:
                    raise StatistiCALError('Please Specify Menu Name')
                else:
                    self.application.SaveCoverageFactorsToFile(file_name)
            except:
                raise

        def SaveResidualsToFile(self,file_name=None):
            """Saves the residuals to file_name"""
            try:
                if file_name is None:
                    raise StatistiCALError('Please Specify Menu Name')
                else:
                    self.application.SaveResidualsToFile(file_name)
            except:
                raise

    class CalibrateDUTWrapper():
        def __init__(self):
            """Intialize the instance of CalibrateDUT"""
            # This is different than the name used in the help file, I found it by looking at regedit in windows
            try:
                self.application=win32com.client.Dispatch('CalibrateDUT.CalibrateDUT_Control')
                self.Successful=self.application.Successful
            except:
                #raise
                raise StatistiCALError('The COM object representing CalbirateDUT failed to intialize')

        def SetCalCoef(self,CalibrationFilePath):
            """Sets the calibration file path """
            self.application.SetCalCoef()


class StatistiCALMenuModel():
    """Holds a menu file for statistiCAL, the serialized form is a file with a different value on each line.
    File names need to be the fully qualified path to work.
    The StatistiCAL menu format follows.
From menu 'Set calibration parameters'
1. Tier: set to 1 or 2
2. Capacitance in pF/cm
3. Estimated scattering parameters of error box 1
4. Estimated scattering parameters of error box 2
5. Estimated effective dielectric constant

From menu 'Select error format'
6. Input error format (default=3)
                   Put in 0 to select sigma real, sigma imag, and correlation coef.

                   Put in 1 to select in-phase and quadrature errors.
                   Put in 2 to use uniform weighting for the measurements and the S-parameters of the stds.
                   Put in 3 to use uniform weighting for the measurments and to fix the S-parameters of the stds.
7. Output error format
                   Put in 0 to select sigma real, sigma imag, and correlation coef.
                   Put in 1 to select in-phase and quadrature errors.


From menu 'Set systematic errors'
8. First-tier error set 1 selection type (default=0)
                   0 = no systematic errors
                   1 = TRL reference impedance error, input = Re(gamma) Im(Gamma)
                   2 = positively correlated reference plane error, input = S21 I/Q
                   3 = negatively correlated reference plane error, input = S21 I/Q
                   4 = uncorrelated reference plane error, input = S21 I/Q
                   5 = positively correlated series inductance errors         (New in version 1.1)

                   6 = negatively correlated series inductance errors
                   7 = unorrelated series inductance errors         (New in version 1.1)
                   8 = positively correlated shunt capacitance errors         (New in version 1.1)
                   9 = negatively correlated shunt capacitance errors         (New in version 1.1)
                   10 = unorrelated shunt capacitance errors         (New in version 1.1)
                   11 = SOLT uncorrelated port 1 and 2 errors, input = S11,S22,S21

                   12 = read in entire covariance matrix (only allowed once)
(Note: These 12 terms were expanded in StatistiCAL version 1.1 from the definitions in StatistiCAL versions 1.0,
and are not backward compatible.)
9. First-tier error set 1 selection value
10. First-tier error set 2 selection type
11. First-tier error set 2 selection value
12. First-tier error set 3 selection type
13. First-tier error set 3 selection value
14. First-tier error set 4 selection type

15. First-tier error set 4 selection value
16. First-tier error set 5 selection type
17. First-tier error set 5 selection value
18. Second-tier error set 1 selection type
19. Second-tier error set 1 selection value
20. Second-tier error set 2 selection type
21. Second-tier error set 2 selection value
22. Second-tier error set 3 selection type
23. Second-tier error set 3 selection value
24. Second-tier error set 4 selection type
25. Second-tier error set 4 selection value

26. Second-tier error set 5 selection type
27. Second-tier error set 5 selection value

From menu 'Options'
28. Minimum acceptable residual standard deviation for StatistiCAL to consider a solution valid (0=default)
29. Number of degrees of freedom associated with systematic errors (0=default)
30. Coupling correction control (StatistiCAL Plus only)
  Digit 1 Iterative refinement of calibration and crosstalk terms together (not recommended)
  Digit 2 Force coupling terms to zero but find uncertainty

  Digit 3 Turn on crosstalk terms
  Digit 4 Use internal model (instead of conventional 16-term model)
  Digit 5 Use optimistic crosstalk uncertainties (not recommended)
  Digit 6 Use a symmetirc crosstalk model
31. Supress search for better starting values of error-box parameters.  (1=true, 0=false=default)
32. The file or values of the k factor used to override the default values determined by StatistiCAL
(StatistiCAL Plus only)
33. Minumum acceptable estimate passed to ODRPACK. (0=default)

34. Descriptive title for the calibration.
35. Estimate of error-box transmission coeffiecient amplitude used for starting point search.
36. Streamline starting point search pattern.  (1=true, 0=false=default)
37. ODRPACK error template. (0=default)

Relative paths
38. Path and file name that this menu was saved to. This is used to find relative paths.

New additions to 'Options'
39. Factor that we multiply deviations of actual epsilon effective from
guess before adding them to the actual standard deviation and deciding on quality of this result.

40. MultiCal configureation switch (StatistiCAL Plus only)
  0 ODRPACK engine
  1 MultiCal starting guess with ODRPACK refinement
  2 MultiCal engine with uncertainty
  3 MultiCal engine (debug mode)
41. Reference-plane position. (StatistiCAL Plus only)
42. k-factor override switch. 0=default, 1=override StatistiCAL Plus k-factor guess (StatistiCAL Plus only,
not recommended)
Currently undefined (5 total)
43-47

Number of calibration standards
48.  Number of thrus, nthru

49.  Number of lines, nline
50.  Number of reflects, nrefl
51.  Number of reciprocal (adapter) standards, nrecip
52.  Number of loads, nload
53.  Number of general attenuator calibration standards, natt
54.  Number of DUT measurements, ndut
55.  Number of isolation standards, niso
56.  number of switch-term standards, nswi
57.  Total number of standards and DUTs, ntot

        For each of the 40 calibration standards i=1,2,...,40 listed in menu 'Define calibration standards'
        we have the following 51 variables stored in the menu:

        1. Length of standard in cm
            2. Type of calibration standard, StdType(i)
                Type 0: Ignore standard.
                Type 1: Thru. Must have zero length. (See also Thru calibration standard)
                Type 2: Line. Requires that cap be set to line capacitance. (See also Line calibration standard)
                Type 3: Reflect. These have equal but unknown reflection coeficients at each port. (S11=S22, S21=S12=0)
                            Each reflect adds in two unknown elements
                            to the beta vector. (See also Reflect calibration standard)

                Type 4: Load. Like reflects except that reflection coefficients are known.
                (S21=S12=0) (See also Load calibration standard)
                Type 5: Reciprocal Adapter calibration standard.
                (S21=S12 is only thing known about this standard) (See also Reciprocal calibration standard)
                Type 6: Attenuator.
                Like a load except that reflection and transmission coeficients are known.
                (S21=S12) (See also Attenuator calibration standard)
                Type 7: Unknown DUTs (loads) on ports 1&2 (S21=S12=0) (See also DUTs)

        Type 8: Reciprocal but otherwise unknown two-port DUT. (S21=S12)
                            This device adds some calibration information (S21=S12).
                             It can be used as a standard/DUT in first-tier calibrations for adapter removal problems.
                Type 9: Unknown two-port DUT, no restrictions.
                Type 10: Isolation standard. (See also Isolation calibration standard)
                               Note that type 10 has the isolation measurements in S21 and S12.
                Type 11: Switch terms. (See also Switch-term file format)

            Type 12: Crosstalk standard (S21=S12=0) (See also Crosstalk calibration standard)
            Type 13: Crosstalk standard (S21=S12<>0) (See also Crosstalk calibration standard)
            Note that type 11 has Frequency (GHz), GammaF=a2/b2, GammaR=a1/b1, 0+j0, 0+j0, as generated by MultiCal.
            3. Raw measurement file, nFile(i)
            4. Error in raw measurement file, nFile_e(i)
            5. Standard definition file, nFile_def(i)
            6. Error in standard definition, nFile_def_e(i)

            Logical parameters defining file or model status (=1 means activated, =0 means deactivated)
            7. Raw measurement file, LFile(i)
            8. Error in raw measurement file, LFile_e(i)
            9. Standard definition file, LFile_def(i)
            10. Error in standard definition, LFile_def_e(i)
            11. Model, LFile_def_model(i)
            The 40 model parameters defining the calibration standard
            12. Transmission line t (ps) for port 1 load (or entire std for an attenuator)
            13. Transmission line Z0 (ohms) for port 1 load (or entire std for an attenuator)
            14. Transmission line series resistance (Gohm/s) for port 1 load (or entire std for an attenuator)
            15. Use HP approximation switch (checked=1, unchecked =0) for port 1 load (or entire std for an attenuator)
            16. Capacitor #1 C0 for port 1 load
            17. Capacitor #1 C1 for port 1 load
            18. Capacitor #1 C2 for port 1 load
            19. Capacitor #1 C3 for port 1 load
            20. Capacitor #2 C0 for port 1 load
            21. Capacitor #2 C1 for port 1 load
            22. Capacitor #2 C2 for port 1 load
            23. Capacitor #2 C3 for port 1 load
            24. Inductor L0 for port 1 load
            25. Inductor L1 for port 1 load
            26. Inductor L2 for port 1 load
            27. Inductor L3 for port 1 load
            28. Resistor R0 for port 1 load
            29. Resistor R1 for port 1 load
            30. Resistor R2 for port 1 load
            31. Resistor R3 for port 1 load
            32. Transmission line t (ps) for port 2 load
            33. Transmission line Z0 (ohms) for port 2 load
            34. Transmission line series resistance (Gohm/s) for port 2 load
            35. Use HP approximation switch (checked=1, unchecked =0) for port 2 load
            36. Capacitor #1 C0 for port 2 load
            37. Capacitor #1 C1 for port 2 load
            38. Capacitor #1 C2 for port 2 load
            39. Capacitor #1 C3 for port 2 load
            40. Capacitor #2 C0 for port 2 load
            41. Capacitor #2 C1 for port 2 load
            42. Capacitor #2 C2 for port 2 load
            43. Capacitor #2 C3 for port 2 load
            44. Inductor L0 for port 2 load
            45. Inductor L1 for port 2 load
            46. Inductor L2 for port 2 load
            47. Inductor L3 for port 2 load
            48. Resistor R0 for port 2 load
            49. Resistor R1 for port 2 load
            50. Resistor R2 for port 2 load
            51. Resistor R3 for port 2 load
        Next standard i

"""
    def __init__(self,file_path=None,**options):
        "Sets up the menu class"
        # menu items is the list of properties to be set
        if file_path is None:
            self.menu_data=["" for i in range(2097)]
            self.path=None
        else:
            in_file=open(file_path,'r')
            self.menu_data=in_file.read().splitlines()
            in_file.close()
            self.path=file_path


    def __str__(self):
        "Controls the behavior of the menu when a string function such as print is called"
        out_string=""
        for value in self.menu_data[:]:
            out_string=out_string+str(value)+"\n"
        return out_string
    def save(self,file_path=None):
        """Saves the menu to file_path, defaults to self.path attribute"""
        if file_path is None:
            file_path=self.path
        out_file=open(file_path,'w')
        out_file.write(str(self))
        out_file.close()

    def set_line(self,line_number,value):
        "Sets the line specified by line_number to value"
        self.menu_data[line_number-1]=value

    def get_line(self,line_number):
        "gets the line specified by line_number "
        return self.menu_data[line_number-1]

    def set_tier(self,tier=1):
        """Sets the tier of the calibration, 1 or 2 """
        if str(tier) not in ["1","2"]:
            raise TypeError("The value must be 1 or 2")
        else:
            self.menu_data[0]=str(tier)
    def get_tier(self):
        """Gets the tier of the calibration, 1 or 2 """
        return self.menu_data[0]

    def set_capacitance(self,capacitance):
        """Sets the capacitance in pf/cm"""
        self.menu_data[1]=str(capacitance)

    def get_capacitance(self):
        """Gets the capacitance in pf/cm"""
        return self.menu_data[1]

    def set_estimated_scattering_parameters_error_box_1(self,file_path):
        "Sets the file_path to the estimated scattering parameters of error box 1"
        self.menu_data[2]=file_path

    def get_estimated_scattering_parameters_error_box_1(self):
        "Gets the file_path to the estimated scattering parameters of error box 1"
        return self.menu_data[2]

    def set_estimated_scattering_parameters_error_box_2(self,file_path):
        "Sets the file_path to the estimated scattering parameters of error box 2"
        self.menu_data[3]=file_path

    def get_estimated_scattering_parameters_error_box_2(self):
        "Gets the file_path to the estimated scattering parameters of error box 2"
        return self.menu_data[3]

    def set_estimated_dielectric_constant(self,file_path):
        "Sets the file_path to the estimated dielectric constant"
        self.menu_data[4]=file_path

    def get_estimated_dielectric_constant(self):
        "Gets the file_path to the estimated dielectric constant"
        return self.menu_data[4]

    def set_input_error_format(self,error_format=3):
        """ Sets the input error format
        Put in 0 to select sigma real, sigma imag, and correlation coef.
        Put in 1 to select in-phase and quadrature errors.
        Put in 2 to use uniform weighting for the measurements and the S-parameters of the stds.
        Put in 3 to use uniform weighting for the measurments and to fix the S-parameters of the stds.
        """
        self.menu_data[5]=str(error_format)

    def get_input_error_format(self):
        """ Gets the input error format
        Put in 0 to select sigma real, sigma imag, and correlation coef.
        Put in 1 to select in-phase and quadrature errors.
        Put in 2 to use uniform weighting for the measurements and the S-parameters of the stds.
        Put in 3 to use uniform weighting for the measurments and to fix the S-parameters of the stds.
        """
        return self.menu_data[5]

    def set_output_error_format(self,error_format=0):
        """Output error format
                   Put in 0 to select sigma real, sigma imag, and correlation coef.
                   Put in 1 to select in-phase and quadrature errors."""
        self.menu_data[6]=str(error_format)

    def set_systematic_errors(self,error_type=0):
        """First-tier error set 1 selection type (default=0)
                   0 = no systematic errors
                   1 = TRL reference impedance error, input = Re(gamma) Im(Gamma)
                   2 = positively correlated reference plane error, input = S21 I/Q
                   3 = negatively correlated reference plane error, input = S21 I/Q
                   4 = uncorrelated reference plane error, input = S21 I/Q
                   5 = positively correlated series inductance errors         (New in version 1.1)

                   6 = negatively correlated series inductance errors
                   7 = unorrelated series inductance errors         (New in version 1.1)
                   8 = positively correlated shunt capacitance errors         (New in version 1.1)
                   9 = negatively correlated shunt capacitance errors         (New in version 1.1)
                   10 = unorrelated shunt capacitance errors         (New in version 1.1)
                   11 = SOLT uncorrelated port 1 and 2 errors, input = S11,S22,S21

                   12 = read in entire covariance matrix (only allowed once)
        (Note: These 12 terms were expanded in StatistiCAL version 1.1
        from the definitions in StatistiCAL versions 1.0, and are not backward compatible.)
        """
        self.menu_data[7]=str(error_type)

    def set_description(self,description):
        """Sets the sample description """
        self.menu_data[33]=description
    def get_description(self):
        """Gets the sample description """
        return self.menu_data[33]
    def set_number_dut(self,description):
        """Sets the number of duts """
        self.menu_data[53]=description
    def get_number_dut(self):
        """Gets the number of duts """
        return self.menu_data[53]
    def set_standard(self,standard_number=1,**options):
        """Sets the calibration standard defintion, pass all the variables in the options dictionary,
        options={1:length of standard,2:type of standard, etc}
        For each of the 40 calibration standards i=1,2,...,40 listed in menu 'Define calibration standards'
        we have the following 51 variables stored in the menu:

        1. Length of standard in cm
            2. Type of calibration standard, StdType(i)
                Type 0: Ignore standard.
                Type 1: Thru. Must have zero length. (See also Thru calibration standard)
                Type 2: Line. Requires that cap be set to line capacitance. (See also Line calibration standard)
                Type 3: Reflect. These have equal but unknown reflection coeficients at each port. (S11=S22, S21=S12=0)
                            Each reflect adds in two unknown elements to the beta vector.
                            (See also Reflect calibration standard)

        Type 4: Load. Like reflects except that reflection coefficients are known. (S21=S12=0)
        (See also Load calibration standard)
                Type 5: Reciprocal Adapter calibration standard. (S21=S12 is only thing known about this standard)
                (See also Reciprocal calibration standard)
                Type 6: Attenuator. Like a load except that reflection and transmission coeficients are known. (S21=S12)
                (See also Attenuator calibration standard)
                Type 7: Unknown DUTs (loads) on ports 1&2 (S21=S12=0) (See also DUTs)

        Type 8: Reciprocal but otherwise unknown two-port DUT. (S21=S12)
                            This device adds some calibration information (S21=S12).
                             It can be used as a standard/DUT in first-tier calibrations for adapter removal problems.
                Type 9: Unknown two-port DUT, no restrictions.
                Type 10: Isolation standard. (See also Isolation calibration standard)
                               Note that type 10 has the isolation measurements in S21 and S12.
                Type 11: Switch terms. (See also Switch-term file format)

            Type 12: Crosstalk standard (S21=S12=0) (See also Crosstalk calibration standard)
            Type 13: Crosstalk standard (S21=S12<>0) (See also Crosstalk calibration standard)
            Note that type 11 has Frequency (GHz), GammaF=a2/b2, GammaR=a1/b1, 0+j0, 0+j0, as generated by MultiCal.
            3. Raw measurement file, nFile(i)
            4. Error in raw measurement file, nFile_e(i)
            5. Standard definition file, nFile_def(i)
            6. Error in standard definition, nFile_def_e(i)

            Logical parameters defining file or model status (=1 means activated, =0 means deactivated)
            7. Raw measurement file, LFile(i)
            8. Error in raw measurement file, LFile_e(i)
            9. Standard definition file, LFile_def(i)
            10. Error in standard definition, LFile_def_e(i)
            11. Model, LFile_def_model(i)
            The 40 model parameters defining the calibration standard
            12. Transmission line t (ps) for port 1 load (or entire std for an attenuator)
            13. Transmission line Z0 (ohms) for port 1 load (or entire std for an attenuator)
            14. Transmission line series resistance (Gohm/s) for port 1 load (or entire std for an attenuator)
            15. Use HP approximation switch (checked=1, unchecked =0) for port 1 load (or entire std for an attenuator)
            16. Capacitor #1 C0 for port 1 load
            17. Capacitor #1 C1 for port 1 load
            18. Capacitor #1 C2 for port 1 load
            19. Capacitor #1 C3 for port 1 load
            20. Capacitor #2 C0 for port 1 load
            21. Capacitor #2 C1 for port 1 load
            22. Capacitor #2 C2 for port 1 load
            23. Capacitor #2 C3 for port 1 load
            24. Inductor L0 for port 1 load
            25. Inductor L1 for port 1 load
            26. Inductor L2 for port 1 load
            27. Inductor L3 for port 1 load
            28. Resistor R0 for port 1 load
            29. Resistor R1 for port 1 load
            30. Resistor R2 for port 1 load
            31. Resistor R3 for port 1 load
            32. Transmission line t (ps) for port 2 load
            33. Transmission line Z0 (ohms) for port 2 load
            34. Transmission line series resistance (Gohm/s) for port 2 load
            35. Use HP approximation switch (checked=1, unchecked =0) for port 2 load
            36. Capacitor #1 C0 for port 2 load
            37. Capacitor #1 C1 for port 2 load
            38. Capacitor #1 C2 for port 2 load
            39. Capacitor #1 C3 for port 2 load
            40. Capacitor #2 C0 for port 2 load
            41. Capacitor #2 C1 for port 2 load
            42. Capacitor #2 C2 for port 2 load
            43. Capacitor #2 C3 for port 2 load
            44. Inductor L0 for port 2 load
            45. Inductor L1 for port 2 load
            46. Inductor L2 for port 2 load
            47. Inductor L3 for port 2 load
            48. Resistor R0 for port 2 load
            49. Resistor R1 for port 2 load
            50. Resistor R2 for port 2 load
            51. Resistor R3 for port 2 load """
        # line that the standard definition starts
        line_offset=(int(standard_number)-1)*51+56
        for key,value in options.items():
            self.menu_data[line_offset+int(key)]=value

    def get_standard(self,standard_number=1):
        """Gets the calibration standard defintion for the specified standard number"""
        text="""
        For each of the 40 calibration standards i=1,2,...,40 listed in menu 'Define calibration standards'
        we have the following 51 variables stored in the menu:

            1. Length of standard in cm {0}
            2. Type of calibration standard, {1}
                StdType(i)
                Type 0: Ignore standard.
                Type 1: Thru. Must have zero length. (See also Thru calibration standard)
                Type 2: Line. Requires that cap be set to line capacitance. (See also Line calibration standard)
                Type 3: Reflect. These have equal but unknown reflection coeficients at each port. (S11=S22, S21=S12=0)
                            Each reflect adds in two unknown elements to the beta vector.
                            (See also Reflect calibration standard)

                Type 4: Load. Like reflects except that reflection coefficients are known. (S21=S12=0)
                (See also Load calibration standard)
                Type 5: Reciprocal Adapter calibration standard. (S21=S12 is only thing known about this standard)
                (See also Reciprocal calibration standard)
                Type 6: Attenuator. Like a load except that reflection and transmission coeficients are known. (S21=S12)
                (See also Attenuator calibration standard)
                Type 7: Unknown DUTs (loads) on ports 1&2 (S21=S12=0) (See also DUTs)

                Type 8: Reciprocal but otherwise unknown two-port DUT. (S21=S12)
                            This device adds some calibration information (S21=S12).
                             It can be used as a standard/DUT in first-tier calibrations for adapter removal problems.
                Type 9: Unknown two-port DUT, no restrictions.
                Type 10: Isolation standard. (See also Isolation calibration standard)
                               Note that type 10 has the isolation measurements in S21 and S12.
                Type 11: Switch terms. (See also Switch-term file format)

                Type 12: Crosstalk standard (S21=S12=0) (See also Crosstalk calibration standard)
                Type 13: Crosstalk standard (S21=S12<>0) (See also Crosstalk calibration standard)
            Note that type 11 has Frequency (GHz), GammaF=a2/b2, GammaR=a1/b1, 0+j0, 0+j0, as generated by MultiCal.
            3. Raw measurement file, nFile(i){2}
            4. Error in raw measurement file, nFile_e(i) {3}
            5. Standard definition file, nFile_def(i) {4}
            6. Error in standard definition, nFile_def_e(i) {5}

            Logical parameters defining file or model status (=1 means activated, =0 means deactivated)
            7. Raw measurement file, LFile(i) {6}
            8. Error in raw measurement file, LFile_e(i) {7}
            9. Standard definition file, LFile_def(i) {8}
            10. Error in standard definition, LFile_def_e(i){9}
            11. Model, LFile_def_model(i) {10}
            The 40 model parameters defining the calibration standard
            12. Transmission line t (ps) for port 1 load (or entire std for an attenuator) {11}
            13. Transmission line Z0 (ohms) for port 1 load (or entire std for an attenuator) {12}
            14. Transmission line series resistance (Gohm/s) for port 1 load (or entire std for an attenuator) {13}
            15. Use HP approximation switch (checked=1, unchecked =0) for port 1 load (or entire std for an attenuator) {14}
            16. Capacitor #1 C0 for port 1 load {15}
            17. Capacitor #1 C1 for port 1 load {16}
            18. Capacitor #1 C2 for port 1 load {17}
            19. Capacitor #1 C3 for port 1 load {18}
            20. Capacitor #2 C0 for port 1 load {19}
            21. Capacitor #2 C1 for port 1 load {20}
            22. Capacitor #2 C2 for port 1 load {21}
            23. Capacitor #2 C3 for port 1 load {22}
            24. Inductor L0 for port 1 load {23}
            25. Inductor L1 for port 1 load {24}
            26. Inductor L2 for port 1 load {25}
            27. Inductor L3 for port 1 load {26}
            28. Resistor R0 for port 1 load {27}
            29. Resistor R1 for port 1 load {28}
            30. Resistor R2 for port 1 load {29}
            31. Resistor R3 for port 1 load {30}
            32. Transmission line t (ps) for port 2 load {31}
            33. Transmission line Z0 (ohms) for port 2 load {32}
            34. Transmission line series resistance (Gohm/s) for port 2 load {33}
            35. Use HP approximation switch (checked=1, unchecked =0) for port 2 load {34}
            36. Capacitor #1 C0 for port 2 load {35}
            37. Capacitor #1 C1 for port 2 load {36}
            38. Capacitor #1 C2 for port 2 load {37}
            39. Capacitor #1 C3 for port 2 load {38}
            40. Capacitor #2 C0 for port 2 load {39}
            41. Capacitor #2 C1 for port 2 load {40}
            42. Capacitor #2 C2 for port 2 load {41}
            43. Capacitor #2 C3 for port 2 load {42}
            44. Inductor L0 for port 2 load {43}
            45. Inductor L1 for port 2 load {44}
            46. Inductor L2 for port 2 load {45}
            47. Inductor L3 for port 2 load {46}
            48. Resistor R0 for port 2 load {47}
            49. Resistor R1 for port 2 load {48}
            50. Resistor R2 for port 2 load {49}
            51. Resistor R3 for port 2 load {50}"""
        line_offset=(int(standard_number)-1)*51+57
        return text.format(*self.menu_data[line_offset:line_offset+52])
    def remove_duts(self):
        "Removes all standards that are type 6-8"
        # set number duts to 0
        self.menu_data[53]=0
        # remove all of the standards
        for standard_number in range(1,40):
            line_offset=(int(standard_number)-1)*51+57
            standard_type=self.menu_data[line_offset:line_offset+52][1]
            if int(standard_type) in [6,7,8]:
                # set the standard to all 0's
                standard_setting={str(i):0 for i in range(1,51)}
                for i in range(3,6):
                    standard_setting[str(i)]=""
                self.set_standard(standard_number,**standard_setting)

    def rebase_file_names(self,new_directory):
        """Replaces all file name directories with new_directory"""
        pass


class StatistiCALSolutionModel(AsciiDataTable):
    """StatistiCALSolutionModel is a class for handling the files created by StatistiCAL Save Solution Vector.
       StatistiCAL generates a solution to the VNA calibration problem, the standard uncertainties of each component of
       the solution, and a covariance matrix for the solution. This covariance matrix includes information on the
       correlations between all of the elements of the solution vector. These results can be accessed from the Results
       pull-down menu.

        Elements of the solution vector are given in real/imaginary format. Elements of the standard uncertainties and
        correlation matrix are given either in real/imaginary or in-phase/quadrature format, based on your choice of
        uncertainty format in the Options>Select Error Formats pull-down menu.

        The solution vector, standard uncertainties, and correlation matrix are ordered as follows:
        1,2	Port 1 error box S1_11
        3,4	Port 1 error box S1_22
        5,6	Port 1 error box S1_21
        7,8	Port 2 error box S2_11
        9,10	Port 2 error box S2_22
        11,12	Port 2 error box sqrt(S2_21*S2_12)
        13,14	Port 2 error box k = sqrt(S2_21/S2_12)
        15,16	Effective Dielectric Constant (Calibrations using line standards only)
        17,18	Reflection coefficient of the reflect (Calibrations using reflects only)

        19,20	Adapter S11 (Calibrations using adapters only)
        21,22	Adapter S22 (Calibrations using adapters only)
        23,24	Adapter S21 (Calibrations using adapters only)
        25,26	DUT S11 (Calibrations using DUTs only)
        27,28	DUT S22 (Calibrations using DUTs only)
        29,30	DUT S21 (Calibrations using DUTs with transmission only)
        31,32	DUT S12 (Calibrations using nonreciprocal DUTs only)

        The solution vector for StatistiCAL Plus (see Solving for crosstalk terms with StatistiCAL Plus) contains the
        following additional crosstalk terms:

        33,34	VNA-VNA	sqrt(S12*S21)
        35,36	VNA-DUT		S14 = S41
        37,38	DUT-VNA		sqrt(S23*S32)
        39,40	DUT-DUT		S34 = S43

        """
    def __init__(self,file_path,**options):
        "Initializes StatistiCALSolutionModel"
        defaults= {"data_delimiter": " ", "column_names_delimiter": ",", "specific_descriptor": 'Solution',
                   "general_descriptor": 'Vector', "extension": 'txt', "comment_begin": "!", "comment_end": "\n",
                   "header": None,
                   "column_names":SOLUTION_VECTOR_COLUMN_NAMES, "column_names_begin_token":"!","column_names_end_token": "\n", "data": None,
                   "row_formatter_string": None, "data_table_element_separator": None,"row_begin_token":None,
                   "row_end_token":None,"escape_character":None,
                   "data_begin_token":None,"data_end_token":None,
                   "column_types":['float' for i in range(len(SOLUTION_VECTOR_COLUMN_NAMES))],
                   "reciprocal":True
                   }
        #"column_types":['float' for i in range(len(SOLUTION_VECTOR_COLUMN_NAMES))]
        #print("The len(SOLUTION_VECTOR_COLUMN_NAMES) is {0}".format(len(SOLUTION_VECTOR_COLUMN_NAMES)))
        self.options={}
        for key,value in defaults.items():
            self.options[key]=value
        for key,value in options.items():
            self.options[key]=value
        if file_path is not None:
            self.path=file_path
            self.__read_and_fix__()
        AsciiDataTable.__init__(self,None,**self.options)
        if file_path is not None:
            self.path=file_path

    def __read_and_fix__(self):
            """Reads in the data and fixes any problems with delimiters, etc"""
            in_file=open(self.path,'r')
            lines=[]
            for line in in_file:
                lines.append([float(x) for x in line.rstrip().lstrip().split(" ")])
            in_file.close()
            self.options["data"]=lines
            self.complex_data=[]
            self.S1=[]
            self.S2=[]
            self.eight_term_correction=[]
            try:
                for row in  self.options["data"]:
                    frequency=[row[0]]
                    # take all rows that are not frequency
                    complex_numbers=row[1:]
                    #print np.array(complex_numbers[1::2])
                    # create a complex data type
                    complex_array=np.array(complex_numbers[0::2])+1.j*np.array(complex_numbers[1::2])
                    #print(len(complex_array.tolist()))
                    self.complex_data.append(frequency+complex_array.tolist())
                    # fill S1 and S2 for later
                    # S1=frequency,S1_11,S1_21,_S1_12,S1_22
                    S1=frequency+[complex_array[0],complex_array[2],complex_array[2],complex_array[1]]
                    self.S1.append(S1)
                    a=complex_array[5]
                    b=complex_array[6]
                    # S2=frequency,S2_11,S2_21,_S2_12,S2_22
                    if self.options["reciprocal"]:
                        S2=frequency+[complex_array[3],a,a,complex_array[4]]
                        self.S2.append(S2)
                        eight_term=frequency+[complex_array[0],complex_array[2],complex_array[2],complex_array[1]]+[complex_array[3],a,a,complex_array[4]]
                        self.eight_term_correction.append(eight_term)
                    else:
                        S2=frequency+[complex_array[3],a*b,a/b,complex_array[4]]
                        self.S2.append(S2)
                        eight_term=frequency+[complex_array[0],complex_array[2],complex_array[2],complex_array[1]]+[complex_array[3],a*b,a/b,complex_array[4]]
                        self.eight_term_correction.append(eight_term)
                    #print("The len(frequency+complex_array.tolist()) is {0}".format(len(frequency+complex_array.tolist())))
            except IndexError:
                print("The data was not fully formed. Please make sure that all rows are the same length."
                      "If the file is not properly formed, then run statisticAL again (make sure "
                      "you ShowStatistiCAL first)")
                raise
#-----------------------------------------------------------------------------
# Module Scripts
if WINDOWS_WRAPPER:
    def test_StatistiCALWrapper():
        """ Tests the wrapper class for the COM object """
        print("Initializing an instance of Statistical")
        statiscal_app=StatistiCALWrapper()
        print(statiscal_app.Successful)
        statiscal_app.ShowStatistiCAL()
if WINDOWS_WRAPPER:
    def test_CalibrateDUTWrapper():
        """ Tests the wrapper class for the COM object """
        print("Initializing an instance of Statistical")
        calibrate_app=CalibrateDUTWrapper()

def test_StatistiCALSolutionModel(file_path="Solution_Plus.txt"):
    """Tests the StatistiCALSolutionModel"""
    os.chdir(TESTS_DIRECTORY)
    new_solution=StatistiCALSolutionModel(file_path)
    print(("The solution's column names are {0}".format(new_solution.column_names)))
    print(("The solution is {0}".format(new_solution)))
    print(("{0} is {1}".format("new_solution.complex_data",new_solution.complex_data)))
    print(("{0} is {1}".format("new_solution.S1",new_solution.S1)))
#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    test_StatistiCALWrapper()
    #test_CalibrateDUTWrapper()
    #test_StatistiCALSolutionModel("Solution_Plus_2.txt")

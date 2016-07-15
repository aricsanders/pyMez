#-----------------------------------------------------------------------------
# Name:        StatistiCALModels
# Purpose:    A wrapper for the StatistiCAL com object and some python classes and functions for interacting with it.
# Author:      Aric Sanders
# Created:     5/25/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" A wrapper for the StatistiCAL com object and some python classes and functions for interacting with it. More
information on statistical can be found at
 http://www.nist.gov/ctl/rf-technology/related-software.cfm """
#-----------------------------------------------------------------------------
# Standard Imports

#-----------------------------------------------------------------------------
# Third Party Imports
try:
    import win32com.client
except:
    print("The win32com package is required to run StatistiCAL models")
    raise ImportError
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions

#-----------------------------------------------------------------------------
# Module Classes
class StatistiCALError(Exception):
    """Error Class for the StatistiCAL Wrapper"""
    pass
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
            self.application=win32com.client.Dispatch('StatistiCAL_Plus.StatistiCAL_Plus_Cnt')
            self.Successful=self.application.Successful
            self.NumberOfODRPACKErrors=self.application.NumberOfODRPACKErrors
        except:
            #raise
            raise StatistiCALError('The COM object representing StatistiCAL failed to intialize')
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
            self.application.CalibrateData()
        except:
            raise

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
            out_string=out_string+value+"\n"
        return out_string

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
        line_offset=(int(standard_number)-1)*51+57
        for key,value in options.iteritems():
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
            11. Model, LFile_def_model(i) {9}
            The 40 model parameters defining the calibration standard {10}
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
            
#-----------------------------------------------------------------------------
# Module Scripts
def test_StatistiCALWrapper():
    """ Tests the wrapper class for the COM object """
    print("Initializing an instance of Statistical")
    statiscal_app=StatistiCALWrapper()
    print statiscal_app.Successful
    statiscal_app.ShowStatistiCAL()

def test_CalibrateDUTWrapper():
    """ Tests the wrapper class for the COM object """
    print("Initializing an instance of Statistical")
    calibrate_app=CalibrateDUTWrapper()

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    test_StatistiCALWrapper()
    #test_CalibrateDUTWrapper()
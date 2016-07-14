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
    ommand successfully

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
    #test_StatistiCALWrapper()
    test_CalibrateDUTWrapper()
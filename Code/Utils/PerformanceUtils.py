#-----------------------------------------------------------------------------
# Name:        PerformanceUtils
# Purpose:     To create tools for testing performance
# Author:      Aric Sanders
# Created:     8/18/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" PerformanceUtils contains functions and classes for testing the performance of
 code in pyMez

   Help
---------------
<a href="./index.html">`pyMez.Code.Utils`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""

#-----------------------------------------------------------------------------
# Standard Imports
import datetime
import time
#-----------------------------------------------------------------------------
# Third Party Imports

#-----------------------------------------------------------------------------
# Module Constants
def timer(function):
    """Timer is meant to be a decorator for a function or method that prints its time"""

    def timed(*args,**keywordargs):
        start_time=datetime.datetime.now()
        result=function(*args,**keywordargs)
        stop_time=datetime.datetime.now()
        print(("The function {0} started at {1} and ended at {2}".format(function.__name__,
                                                                        start_time,
                                                                        stop_time)))
        diff=stop_time-start_time
        print(("It took {0} seconds to run".format(diff.total_seconds())))
        return result

    return timed
#-----------------------------------------------------------------------------
# Module Functions

#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts
def test_timer():
    @timer
    def wait_5s():
        time.sleep(5)

    wait_5s()
def test_timer_with_args():
    time_to_wait=1
    @timer
    def wait_around(wait):
        time.sleep(wait)

    wait_around(time_to_wait)
#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    #test_timer()
    test_timer_with_args()
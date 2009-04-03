# -*- coding: utf-8 -*-
"""
The obspy.mseed plotting test suite.
"""

from obspy.mseed import libmseed
import inspect
import os
import unittest


class LibMSEEDPlottingTestCase(unittest.TestCase):
    """
    Test cases for Libmseed plotting.
    """
    def setUp(self):
        # Directory where the test files are located
        path = os.path.dirname(inspect.getsourcefile(self.__class__))
        self.path = os.path.join(path, 'data')
        
        outpath = os.path.dirname(inspect.getsourcefile(self.__class__))
        self.outpath = os.path.join(outpath, 'output')
    
    def tearDown(self):
        pass
    
    def test_LibMSEEDPlotting(self):
        """
        Creates plotted examples in tests/output directory
        """
        mseed = libmseed()
        mseed_file = os.path.join(self.path, 'BW.BGLD..EHE.D.2008.001')
        gap_file = os.path.join(self.path, 'BW.RJOB..EHZ.D.2009.056')
        small_file = os.path.join(self.path, 'test.mseed')
        small_gap_file = os.path.join(self.path, 'gaps.mseed')
        
        #Calculate full minmaxlist once and use it for caching.
        minmaxlist = mseed.graphCreateMinMaxTimestampList(mseed_file, 777)
        
        #Full graph with user defined colors and size.
        mseed.graph_create_graph(mseed_file, outfile = os.path.join(
            self.outpath, 'full_graph_777x222px_orange_and_turquoise'),
            size = (777, 222), color = '#ffcc66', bgcolor = '#99ffff',
            minmaxlist = minmaxlist)
        
        #Same graph as before but returned as a binary string.
        imgstring = mseed.graph_create_graph(mseed_file, size = (777, 222),
            format = 'png', color = '#ffcc66', bgcolor = '#99ffff',
            minmaxlist = minmaxlist)
        imgfile = open(os.path.join(self.outpath,
            'full_graph_777x222px_orange_and_turquoise.png'))
        self.assertEqual(imgstring, imgfile.read())
        imgfile.close()
        
        #Same graph as above but green with transparent background
        mseed.graph_create_graph(mseed_file, os.path.join(self.outpath,
            'full_graph_777x222px_green_and_transparent'), size = (777, 222),
            transparent = True, minmaxlist = minmaxlist, color = '#99ff99')
        
        #Graph with user defined start and endtime both outside the graph.
        mstg = mseed.readTraces(mseed_file, dataflag = 0)
        starttime = mstg.contents.traces.contents.starttime
        endtime = mstg.contents.traces.contents.endtime
        #Graph begins one day before the file and ends one day after the file.
        stime = mseed.mseedtimestringToDatetime(starttime - 86400 * 1e6)
        etime = mseed.mseedtimestringToDatetime(endtime + 86400 * 1e6)
        #Create graph
        mseed.graph_create_graph(mseed_file, os.path.join(self.outpath, 
            'graph_800x200px_with_one_empty_day_before_and_after_graph'),\
            starttime = stime, endtime = etime)
        
        #Graph that plots the last six hours of the Mini-SEED file.
        mstg = mseed.readTraces(mseed_file, dataflag = 0)
        endtime = mstg.contents.traces.contents.endtime
        starttime = mseed.mseedtimestringToDatetime(endtime - 21600 * 1e6)
        #Create graph
        mseed.graph_create_graph(mseed_file, os.path.join(self.outpath, 
            'graph_800x200px_last_six_hours_two_gray_shades'),\
            starttime = starttime, color = '0.7',
            bgcolor = '0.2')
        
        #Graph with a large gap inbetween
        mseed.graph_create_graph(file = gap_file,
            outfile = os.path.join(self.outpath, 
            'graph_888x222px_with_gap_two_blue_shades'), size = (888, 222),
            color = 'royalblue', bgcolor = 'lightsteelblue')
        
        #Small graph with only 11947 datasamples. It works reasonably well but
        #the plotting method is designed to plot files with several million
        #datasamples.
        mseed.graph_create_graph(file = small_file, outfile = 
            os.path.join(self.outpath,
            'small_graph_with_very_few_datasamples'))
        
        #Small graph with several small gaps
        mseed.graph_create_graph(file = small_gap_file, outfile =
            os.path.join(self.outpath,
            'small_graph_with_small_gaps_yellow'), color = 'y')
        
    def test_PlottingOutputFormats(self):
        """
        Test various output formats.
        """
        mseed = libmseed()
        mseed_file = os.path.join(self.path,
                                  'BW.BGLD..EHE.D.2008.001.first_record')
        #Calculate full minmaxlist once and use it for caching.
        minmaxlist = mseed.graphCreateMinMaxTimestampList(mseed_file, 50)
        # PDF
        data = mseed.graph_create_graph(mseed_file, format = 'pdf',\
                                        size = (50, 50),\
                                        minmaxlist = minmaxlist)
        self.assertEqual(data[0:4], "%PDF")
        # PS
        data = mseed.graph_create_graph(mseed_file, format = 'ps',\
                                        size = (50, 50),\
                                        minmaxlist = minmaxlist)
        self.assertEqual(data[0:4], "%!PS")
        # PNG
        data = mseed.graph_create_graph(mseed_file, format = 'png',\
                                        size = (50, 50),\
                                        minmaxlist = minmaxlist)
        self.assertEqual(data[1:4], "PNG")
        # SVG
        data = mseed.graph_create_graph(mseed_file, format = 'svg',\
                                        size = (50, 50),\
                                        minmaxlist = minmaxlist)
        self.assertEqual(data[0:5], "<?xml")
        
def suite():
    return unittest.makeSuite(LibMSEEDPlottingTestCase, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
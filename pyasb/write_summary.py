
"""
SkyMap module

Auxiliary functions to plot the SkyMap
____________________________

This module is part of the PyASB project, 
created and maintained by Miguel Nievas [UCM].
____________________________
"""

from __future__ import print_function


# NOTE: The following 2 functions should be moved to separate file or at least to a new class
# NOTE: Maybe should be rewrite as follows?:
# 1.) Create the file with the header
# 2.) Iterative add lines

class Summary(object):
    def __init__(self,Image,InputOptions,ImageAnalysis,InstrumentCalibration,
                 ImageSkyBrightness,CloudCoverage):
        self.summarize_results(InputOptions, Image, ImageAnalysis,\
            InstrumentCalibration, ImageSkyBrightness, CloudCoverage)
        self.save_summary_to_file(Image.ImageInfo)

    def summarize_results(self,InputOptions, Image, ImageAnalysis,
                          InstrumentCalibration, ImageSkyBrightness, CloudCoverage):

        sum_date   = str(Image.ImageInfo.fits_date)
        sum_filter = str(Image.ImageInfo.used_filter)
        sum_stars  = str(InstrumentCalibration.BouguerFit.Regression.Nstars_initial)
        sum_gstars = str("%.1f"%float(InstrumentCalibration.BouguerFit.Regression.Nstars_rel))
        sum_zpoint = \
         str("%.3f"%float(InstrumentCalibration.BouguerFit.Regression.mean_zeropoint))+' +/- '+\
         str("%.3f"%float(InstrumentCalibration.BouguerFit.Regression.error_zeropoint))
        sum_extinction = \
         str("%.3f"%float(InstrumentCalibration.BouguerFit.Regression.extinction))+' +/- '+\
         str("%.3f"%float(InstrumentCalibration.BouguerFit.Regression.error_extinction))
        sum_skybrightness = \
         str("%.3f"%float(ImageSkyBrightness.SBzenith))+' +/- '+\
         str("%.3f"%float(ImageSkyBrightness.SBzenith_err))
        sum_cloudcoverage = \
         str("%.3f"%float(CloudCoverage.mean_cloudcover))+' +/- '+\
         str("%.3f"%float(CloudCoverage.error_cloudcover))
        
        self.summary_content = \
            [sum_date, sum_filter,sum_stars, sum_gstars, \
            sum_zpoint, sum_extinction, sum_skybrightness, sum_cloudcoverage]

    def save_summary_to_file(self,ImageInfo):
        try:
            assert(ImageInfo.summary_path!=False)
        except:
            print('Skipping write summary to file')
        else:
            print('Write summary to file')
            
            content = ['#Date, Filter, Stars, % Good Stars, ZeroPoint, Extinction, SkyBrightness, CloudCoverage\n']
            for line in self.summary_content:
                content_line = ""
                for element in line:
                    content_line += element
                content.append(content_line+", ")
            
            if ImageInfo.summary_path == "screen":
                print(content)
            else:
                summary_filename = str("%s/Summary_%s_%s_%s.txt" %(\
                    ImageInfo.summary_path, ImageInfo.obs_name,\
                    ImageInfo.fits_date, ImageInfo.used_filter))

                summaryfile = open(summary_filename,'w+')
                summaryfile.writelines(content)
                summaryfile.close()
        


# PyASB launcher module
#
# Concatenate processes
# ____________________________
#
# This module is part of the PyASB project,
# created and maintained by Miguel Nievas [UCM].


import signal
import sys
import inspect

from .input_options import ReadOptions
from .image_info import ImageInfo
from .help import PlatformHelp

from .load_fitsimage import FitsImage
from .astrometry import ImageCoordinates
from .bouguer_fit import BouguerFit
from .sky_brightness import SkyBrightness, SkyBrightnessGraph
from .skymap_plot import SkyMap
from .cloud_coverage import CloudCoverage, StarCatalog
from .write_summary import Summary
from .read_config import ConfigOptions
from .user import main

config_file_default = 'config.cfg'


# ~~~~~~~~~~ Halt handler ~~~~~~~~~~~
def handler(signum, frame):
    print 'Signal handler called with signal', signum
    print "CTRL-C pressed"
    raise SystemExit
    # sys.exit(0)

signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)


#@profile
class LoadImage(object):

    def __init__(self, InputOptions, ImageInfo, ConfigOptions, configs, input_file=None):
        # Load Image file list
        if input_file == None:
            input_file = InputOptions.fits_filename_list[0]

        ''' Load fits image '''
        self.FitsImage = FitsImage(input_file)
        # Local copy of ImageInfo. We will process it further.
        self.ImageInfo = ImageInfo
        self.ImageInfo.read_header(self.FitsImage.fits_Header)
        self.ImageInfo.config_processing_specificfilter(ConfigOptions, configs)

        try:
            self.FitsImage.subtract_corners_background = True
            self.FitsImage.reduce_science_frame(
                self.ImageInfo.darkframe,
                self.ImageInfo.sel_flatfield,
                MasterBias=None,
                ImageInfo=self.ImageInfo)
        except:
            # raise
            print(inspect.stack()[0][2:4][::-1])
            print('Cannot reduce science frame')

        # Flip image if needed
        self.FitsImage.flip_image_if_needed(self.ImageInfo)

        self.FitsImage.__clear__()
        self.output_paths(InputOptions)

    def output_paths(self, InputOptions):
        # Output file paths (NOTE: should be moved to another file or at least separated function)
        # Photometric table

        path_list = [
            "photometry_table_path", "skymap_path", "bouguerfit_path",
            "skybrightness_map_path", "skybrightness_table_path",
            "cloudmap_path", "clouddata_path", "summary_path"]

        for path in path_list:
            try:
                setattr(self.ImageInfo, path, getattr(InputOptions, path))
            except:
                try:
                    getattr(InputOptions, path)
                except:
                    setattr(self.ImageInfo, path, False)

#@profile


class ImageAnalysis(object):

    def __init__(self, Image):
        ''' Analize image and perform star astrometry & photometry. 
            Returns ImageInfo and StarCatalog'''
        self.StarCatalog = StarCatalog(Image.ImageInfo)

        if (Image.ImageInfo.calibrate_astrometry == True):
            Image.ImageInfo.skymap_path = "screen"
            TheSkyMap = SkyMap(Image.ImageInfo, Image.FitsImage)
            TheSkyMap.setup_skymap()
            TheSkyMap.set_starcatalog(self.StarCatalog)
            TheSkyMap.astrometry_solver()

        self.StarCatalog.process_catalog_specific(
            Image.FitsImage, Image.ImageInfo)
        self.StarCatalog.save_to_file(Image.ImageInfo)
        TheSkyMap = SkyMap(Image.ImageInfo, Image.FitsImage)
        TheSkyMap.setup_skymap()
        TheSkyMap.set_starcatalog(self.StarCatalog)
        TheSkyMap.complete_skymap()

'''#@profile
class MultipleImageAnalysis():
    def __init__(self,InputOptions):
        class StarCatalog_():
            StarList = []
            StarList_woPhot = []
        
        InputFileList = InputOptions.fits_filename_list
        
        for EachFile in InputFileList:
            EachImage = LoadImage(EachFile)
            EachAnalysis = ImageAnalysis(EachImage)
            self.StarCatalog.StarList.append(EachAnalysis.StarCatalog.StarList)
            self.StarCatalog.StarList_woPhot.append(EachAnalysis.StarCatalog.StarList_woPhot)
'''

#@profile


class InstrumentCalibration(object):

    def __init__(self, ImageInfo, StarCatalog):
        try:
            self.BouguerFit = BouguerFit(ImageInfo, StarCatalog)
        except Exception as e:
            print(inspect.stack()[0][2:4][::-1])
            print('Cannot perform the Bouguer Fit. Error is: ')
            print type(e)
            print e
            exit(0)
            # raise


#@profile
class MeasureSkyBrightness(object):

    def __init__(self, FitsImage, ImageInfo, BouguerFit):
        ImageCoordinates_ = ImageCoordinates(ImageInfo)
        TheSkyBrightness = SkyBrightness(
            FitsImage, ImageInfo, ImageCoordinates_, BouguerFit)
        TheSkyBrightnessGraph = SkyBrightnessGraph(
            TheSkyBrightness, ImageInfo, BouguerFit)

        '''
        TheSkyBrightness = SkyBrightness(ImageInfo)
        TheSkyBrightness.load_mask(altitude_cut=10)
        TheSkyBrightness.load_sky_image(FitsImage)
        #TheSkyBrightness.calibrate_image(FitsImage,ImageInfo,BouguerFit)
        TheSkyBrightness.zernike_decomposition(BouguerFit,npoints=5000,order=10)
        '''

        self.SBzenith = TheSkyBrightness.SBzenith
        self.SBzenith_err = TheSkyBrightness.SBzenith_err

#@profile


def perform_complete_analysis(InputOptions, ImageInfoCommon, ConfigOptions, configs, input_file):
    # Load Image into memory & reduce it.
        # Clean (no leaks)
    Image_ = LoadImage(
        InputOptions, ImageInfoCommon, ConfigOptions, configs, input_file)

    # Look for stars that appears in the catalog, measure their fluxes. Generate starmap.
    # Clean (no leaks)
    ImageAnalysis_ = ImageAnalysis(Image_)

    print('Image date: ' + str(Image_.ImageInfo.date_string) +
          ', Image filter: ' + str(Image_.ImageInfo.used_filter))

    # Create the needed classes for the summary write
    class InstrumentCalibration_:

        class BouguerFit:

            class Regression:
                mean_zeropoint = -1
                error_zeropoint = -1
                extinction = -1
                error_extinction = -1
                Nstars_rel = -1
                Nstars_initial = -1

    try:
        # Calibrate instrument with image. Generate fit plot.
        # Clean (no leaks)
        InstrumentCalibration_ = InstrumentCalibration(
            Image_.ImageInfo,
            ImageAnalysis_.StarCatalog)
    except:
        class ImageSkyBrightness:
            SBzenith = '-1'
            SBzenith_err = '-1'

    else:
        # Measure sky brightness / background. Generate map.
        ImageSkyBrightness = MeasureSkyBrightness(
            Image_.FitsImage,
            Image_.ImageInfo,
            InstrumentCalibration_.BouguerFit)

    #
    #    Even if calibration fails,
    #    we will try to determine cloud coverage
    #    and write the summary
    #

    # Detect clouds on image
    ImageCloudCoverage = CloudCoverage(
        Image_,
        ImageAnalysis_,
        InstrumentCalibration_.BouguerFit)

    Summary_ = Summary(Image_, InputOptions, ImageAnalysis_,
                       InstrumentCalibration_, ImageSkyBrightness, ImageCloudCoverage)


if __name__ == '__main__':

    import ConfigParser as configparser

    input_options = main()
    print input_options
    #PlatformHelp_ = PlatformHelp()
    #input_options = ReadOptions(sys.argv)

    configs = configparser.SafeConfigParser(defaults={'a': '100'})
    configs.read('config.ini')

    config_options = ConfigOptions(input_options.configfile)

    image_info_common = ImageInfo()
    image_info_common.config_processing_common(config_options, input_options)

    for input_file in input_options.fits_filename_list:
        perform_complete_analysis(
            input_options, image_info_common, config_options, configs, input_file)

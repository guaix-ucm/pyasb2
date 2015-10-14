
# PyASB help module
#
# Build and show program help
# ____________________________
#
# This module is part of the PyASB project,
# created and maintained by Miguel Nievas [UCM].
# ____________________________


from .info import __shortname__, __longname__, __version__


class PlatformHelp(object):

    def __init__(self):
        self.make_title()
        self.make_welcome()
        self.make_requisites()
        self.make_options()

    def make_title(self):
        nameversion = 10 * '#' + 3 * ' ' + __shortname__ + \
            ' v' + __version__ + 3 * ' ' + 10 * '#'
        self.separator = len(nameversion) * '#'
        self.title = nameversion

    def make_welcome(self):
        self.welcome = 'Welcome to ' + \
            __shortname__ + ' (' + __longname__ + ')\n'

    def make_requisites(self):
        self.requisites = \
            'Requisites: Python 2.7; Scipy; Numpy;\n' +\
            '  Matplotlib; Pyfits; Pyephem\n\n'

    def make_options(self):
        self.options = \
            '-h: print this help message\n\n' +\
            '-i input_allsky_image: \n' +\
            '  All Sky image you want to be analyzed\n\n' +\
            '-c config_file: \n' +\
            '  Use alternative config file\n\n' +\
            '-d [year,month,day]:\n' +\
            '  Date to be analyzed (AstMon-UCM only)\n' +\
            '  month and day are optional\n\n' +\
            '-om output_map_image path:\n' +\
            '  Output star map image, full or relative path\n' +\
            '  if no output file, show the map on screen\n\n' +\
            '-ot output_photometric_table path:\n' +\
            '  Output photometric table full or relative path\n' +\
            '  if no output file, show the table on screen\n\n' +\
            '-or output_results_summary path:\n' +\
            '  Summary of analysis, fit parameters and zenith SB\n' +\
            '  full or relative path. If no output file, \n' +\
            '  show the table on screen\n\n' +\
            '-ob output_bouguerfit_graph path:\n' +\
            '  Output bouguer-fit graph, full or relative path.\n' +\
            '  If no output file, show the graph on screen\n\n' +\
            '-ocm output_cloudmap_image path:\n' +\
            '  Output cloud map image, full or relative path\n' +\
            '  if no output file, show the map on screen\n\n' +\
            '-oct output_clouddata_table path:\n' +\
            '  Output cloud data table, full or relative path\n' +\
            '  if no output file, show the map on screen\n\n' +\
            '-os output_skybrightness_graph path:\n' +\
            '  Output Sky Brightness graph, full or relative path\n' +\
            '  if no output file, show the graph on screen\n\n' +\
            '-ost output_skybrightness_table path:\n' +\
            '  Output Sky Brightness table, full or relative path\n' +\
            '  if no output file, show the graph on screen\n\n'

    def show_help(self):
        print(
            self.separator + '\n' + self.title + '\n' + self.separator + '\n' + self.welcome +
            self.requisites + self.options + self.separator)

    def incorrect_parameter(self, parameter):
        print('ERROR. Incorrect parameter: ' + str(parameter))
        self.show_help()

    def date_or_file_input_error(self):
        print('ERROR. Date or file input')
        self.show_help()

    def no_parameters_error(self):
        print('ERROR. No input parameters especified')
        self.show_help()


# PyASB launcher module
#
# Concatenate processes
# ____________________________
#
# This module is part of the PyASB project,
# created and maintained by Miguel Nievas [UCM].
# ____________________________


class ConfigOptions(object):
    ''' Add and remove options '''
    def __init__(self, config_file):
        self.file_options = []
        self.read_config_file(config_file)

    def add_option(self, param, value):
        self.file_options.append([param, value])

    def remove_option(self, param, value):
        self.file_options.pop([param, value])

    def add_param_value(self, textline):
        line_split = textline.split("=")
        param = line_split[0].replace(' ', '')
        value = line_split[1]
        if '"' not in value and "'" not in value:
            value = value.replace(' ', '')
        value = value.replace('"', '')
        value = value.replace("'", '')
        value = value.replace('\r', '')
        value = value.replace('\n', '')
        self.add_option(param, value)

    def read_config_file(self, config_file):
        print('Trying to open config file ...'),
        raw_config = open(config_file, 'r').readlines()
        print('OK')
        for line in xrange(len(raw_config)):
            raw_config[line] = raw_config[line].replace("\n", "")
            if len(raw_config[line].split("=")) == 2:
                if raw_config[line][0] != "#":
                    self.add_param_value(raw_config[line])

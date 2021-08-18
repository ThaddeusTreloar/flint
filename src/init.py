from os import listdir
import indicator
import error as e
import settings as s

def loadIndicators(settings):

    indicators_source = listdir("/indicators")

    for file in indicators_source:
        
        try:
            settings.indicators[file.rstrip(".py")] = indicator(file).validate()

        except error.NotImplementedError as err:
            print(err.msg) 

def init() -> (bool, str, s.SettingsObject):

    __SETTINGS = s.SettingsObject()
    funcionExit: tuple = __SETTINGS.loadConfigFile("./config.yaml")

    if funcionExit[0] == False:
        
        return False, funcionExit[1], None

    return True, None, __SETTINGS
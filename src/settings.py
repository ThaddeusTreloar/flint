
from yaml import safe_load_all, safe_dump
from error import InsufficientArgumentsError, ConfigLoadError
import generics

class SettingsObject():
    
    def __init__(self) -> None:

        self.MYSQL_HOST:    str = "localhost"
        self.MYSQL_USER:    str = "root"
        self.MYSQL_DB:      str = "alchemists-sieve"
        self.YF_API_KEY:    str = ""
        self.AV_API_KEY:    str = ""
        self.INST_RANGE:    0
        self.PREDICT_RANGE: 0
        self.INTERVAL_RANGE: 0
        self.DATA_ENGINE:   str = ""
        self.TICKER:        str = ""
        self.INTERVAL_U:    ""
        self.INTERVAL_N:    0

        self.kernel:        kernel.Kernel = None
        self.input:         input.Input = None
        self.output:        output.Output = None

def loadDataEngine():
    pass

def validateTickerCode(ticker_code):
    #return true if ticker valid otherwise false
    return True

def set_ticker(args, settings):

    if len(args) < 1 or not args[0]:
        raise InsufficientArgumentsError("set ticker requires 1 argument <ticker_code>")

    if validateTickerCode(args[0]):
        settings.TICKER = args[0].upper()
        return True, None
    else:
        return False, None

def set_interval(args, settings):
    '''
    Set interval time frame for time series
    '''
    interval_n = ""
    interval_u = ""

    for char in args[0]:
        if char.isdigit():
            interval_n += char
        else:
            interval_u += char

    settings.INTERVAL_N = int(interval_n)
    settings.INTERVAL_U = interval_u

    return True, None

def loadConfigFile(file_path: str) -> (SettingsObject, str):

    settings = SettingsObject()

    try:

        with open(file_path, "r") as file:  

            raw_yaml = next(safe_load_all(file))

            config = raw_yaml['config']

            settings.MYSQL_HOST = config["MYSQL_HOST"]
            settings.MYSQL_USER = config["MYSQL_USER"]
            settings.MYSQL_DB = config["MYSQL_DB"]
            settings.AV_API_KEY = config["AV_API_KEY"]
            settings.YF_API_KEY = config["YF_API_KEY"]
            settings.INST_RANGE = config["INST_RANGE"]
            settings.PREDICT_RANGE = config["PREDICT_RANGE"]
            settings.INTERVAL_RANGE = config["INTERVAL_RANGE"]
            settings.DATA_ENGINE = config["DATA_ENGINE"]

            return settings

    except Exception:
        raise ConfigLoadError(None)

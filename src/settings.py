from yaml import safe_load_all, safe_dump
from error import InsufficientArgumentsError

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

    def loadConfigFile(self, FILEPATH: str) -> (bool, str):

        try:
            with open(FILEPATH, "r") as FILE:
            
                rawYaml= next(safe_load_all(FILE))

                config = rawYaml['config']

                self.MYSQL_HOST = config["MYSQL_HOST"]
                self.MYSQL_USER = config["MYSQL_USER"]
                self.MYSQL_DB = config["MYSQL_DB"]
                self.AV_API_KEY = config["AV_API_KEY"]
                self.YF_API_KEY = config["YF_API_KEY"]
                self.INST_RANGE = config["INST_RANGE"]
                self.PREDICT_RANGE = config["PREDICT_RANGE"]
                self.INTERVAL_RANGE = config["INTERVAL_RANGE"]
                self.DATA_ENGINE = config["DATA_ENGINE"]

                return True, None
        
        except Exception as error:
            return False, error

def loadDataEngine():
    pass

def validateTickerCode(ticker_code):
    #return true if ticker valid otherwise false
    return True

def setTicker(args, settings):

    if len(args) < 1 or not arg[0]:
        raise InsufficientArgumentsError("set ticker requires 1 argument <ticker_code>")

    if validateTickerCode(args[0]):
        settings.TICKER = args[0].upper()
        return True, None
    else:
        return False, None

def setInterval(args, settings):

    interval_n  = ""
    interval_u  = ""

    for char in args[0]:
        if char.isdigit():
            interval_n += char
        else:
            interval_u += char

    settings.INTERVAL_N = int(interval_n)
    settings.INTERVAL_U = interval_u

    return True, None

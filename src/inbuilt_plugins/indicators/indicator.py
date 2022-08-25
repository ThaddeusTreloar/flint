import error as e
import settings as s
import functools

class Indicator:

    def __init__(self, config_path):
        self.name
        self.description  
        self.calc_function
        self.fields       
        self.values   
        self.load_settings(config_path)

    def set(self, field, value):

        self.values[field] = value
    
    def load_settings(self):

        #some yaml shit

        config_file = null

        self.name               = config_file["name"]
        self.description        = config_file["description"]
        self.calc_function      = config_file["calc_function"]
        self.fields             = config_file["fields"]
        self.values             = config_file["values"]

    def calc_function(self):
        raise error.NotImplementedFunction("calc_function not implemented for %s" % (self.name))

    def validate(self):
        self.calc_function()


def setIndicatorValue(args, settings):

    return settings.indicators[args.next].set(args.next(), args.next())

def calculateIndicators(ticker_data, settings):

    ticker_data = [x for x in reversed(ticker_data["eod"])]
    sma_list = []

    for i in range( 0, len(ticker_data)-settings.INST_RANGE):
        sum = functools.reduce(lambda a, b: a+b, ticker_data[i+1:i+1+settings.INST_RANGE]) 
        sma_list.insert(0, sum/settings.INST_RANGE)

    return {
        "sma"   : sma_list,
    }

def list():
    pass
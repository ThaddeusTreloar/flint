from sys import argv
from util import panic
import init

def main():

    #systemArguments = argv
    #systemArgumentsNo = len(systemArguments)

    settings = init.init()
    
    settings.kernel.start(settings)

    '''
    ticker_code = input("Enter a ticker code: ")

    ticker_data = yhf.openTicker(ticker_code, __SETTINGS)
    instrument_data = indicators.calculateIndicators(ticker_data, __SETTINGS)
    ticker_data["sma"] = instrument_data["sma"]

    learn(ticker_data, __SETTINGS)    
    '''
if __name__ == "__main__":
    main()
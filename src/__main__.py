from sys import argv

import init
import sources.yahoo_finance as yhf
import console

def main():

    systemArguments = argv
    systemArgumentsNo = len(systemArguments)

    functionExit, errorStr, __SETTINGS = init.init()

    if errorStr != None:
        print(errorStr)
        exit(1)


    console.openConsole(__SETTINGS)

    '''
    ticker_code = input("Enter a ticker code: ")

    ticker_data = yhf.openTicker(ticker_code, __SETTINGS)
    instrument_data = indicators.calculateIndicators(ticker_data, __SETTINGS)
    ticker_data["sma"] = instrument_data["sma"]

    learn(ticker_data, __SETTINGS)    
    '''
if __name__ == "__main__":
    main()
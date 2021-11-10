import requests
import json

from generics.source import Source

class Yahoo(Source):

    def __init__(self):
        pass


def openTicker(ticker_code: str, settings):

    
    interval_unit = input("Enter required interval unit (m, d, mo, wk): ")
    interval_frame = input("Enter required interval frame (1d, 2d, 3d): ")

    url = "https://rest.yahoofinanceapi.com/v8/finance/spark"
    
    params = {
        "interval": interval_frame+interval_unit,
        "range"   : str(int(settings.INTERVAL_RANGE) + settings.INST_RANGE + settings.PREDICT_RANGE)+interval_unit,
        "symbols" : ticker_code+".AX",
        "region"  : "AU"
    }

    headers = {
        'x-api-key': settings.YF_API_KEY
    }

    response = requests.request("GET", url, headers=headers, params=params)

    data = json.loads(response.content)

    return {
        "timestamp" : data[ticker_code+".AX"]["timestamp"],
        "eod"       : data[ticker_code+".AX"]["close"][0:int(settings.INTERVAL_RANGE) + settings.INST_RANGE],
        "test-data" : data[ticker_code+".AX"]["close"][int(settings.INTERVAL_RANGE) + settings.INST_RANGE:],
        "data-raw"  : data[ticker_code+".AX"]["close"]
    }

def returnInstance():
    return Yahoo()
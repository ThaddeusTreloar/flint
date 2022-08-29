import requests
import json

from generics.source import ApiSource
from abstract.settings import Settings
from typing import Any


class eoddata(ApiSource):

    @property
    def threadable(self) -> bool:
        return True

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def api_url(self) -> str:
        "https://rest.yahoofinanceapi.com/v8/finance/spark"

    @property
    def description(self):
        return 'A source module that retrieves data from the eoddata.com.'

    @property
    def local_command_set(self) -> dict[str, object]:
        return self.local_command_set_

    def __init__(self, global_settings: Settings, parent_handler: Any):
        super().__init__(global_settings, parent_handler, "yahoo_finance")
        self.local_command_set_: dict[str, object] = {
            "help": self.help,
        }

    def buildQuery(self, *args) -> str:
        ...

    def sendRequest(self, query: str, *args) -> str:
        ...

    def help(self, args: str) -> str:
        return "source.yahoo_finance does not currently provide any save functionality"


def openTicker(ticker_code: str, settings):

    interval_unit = input("Enter required interval unit (m, d, mo, wk): ")
    interval_frame = input("Enter required interval frame (1d, 2d, 3d): ")

    url = "https://rest.yahoofinanceapi.com/v8/finance/spark"

    params = {
        "interval": interval_frame+interval_unit,
        "range": str(int(settings.INTERVAL_RANGE) + settings.INST_RANGE + settings.PREDICT_RANGE)+interval_unit,
        "symbols": ticker_code+".AX",
        "region": "AU"
    }

    headers = {
        'x-api-key': settings.YF_API_KEY
    }

    response = requests.request("GET", url, headers=headers, params=params)

    data = json.loads(response.content)

    return {
        "timestamp": data[ticker_code+".AX"]["timestamp"],
        "eod": data[ticker_code+".AX"]["close"][0:int(settings.INTERVAL_RANGE) + settings.INST_RANGE],
        "test-data": data[ticker_code+".AX"]["close"][int(settings.INTERVAL_RANGE) + settings.INST_RANGE:],
        "data-raw": data[ticker_code+".AX"]["close"]
    }


def validateTickerCode(ticker_code):
    # return true if ticker valid otherwise false
    return True


def set_ticker(args, settings):

    if len(args) < 1 or not args[0]:
        util.unimplemented()
        # raise InsufficientArgumentsError("set ticker requires 1 argument <ticker_code>")

    if validateTickerCode(args[0]):
        #settings.ticker = args[0].upper()
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

    settings.interval_n = int(interval_n)
    settings.interval_u = interval_u

    return True, None


from requests import get, Request
from json.decoder import JSONObject
from generics.source import ApiSource
from abstract.settings import Settings
from typing import Any, Optional
from pathlib import Path

from pandas import DataFrame


class AlphaVantage(ApiSource):

    @property
    def module_dir_slug(self) -> Path:
        return Path("alphavantage")

    @property
    def threadable(self) -> bool:
        return True

    @property
    def api_key(self) -> str:
        return self.local_settings.api_key

    @property
    def api_url(self) -> str:
        return "https://www.alphavantage.co/query?"

    @property
    def description(self):
        return 'A source module that retrieves data from the alphavantage api.'

    @property
    def local_command_set(self) -> dict[str, object]:
        return self._local_command_set

    def __init__(self, global_settings: Settings, parent_handler: Any, config_path: Path = None):
        self._local_command_set: dict[str, object] = {
            "help": self.help,
            "get": {
                "daily": {
                    "full": self.dailyFullQuery,
                    "compact": self.dailyCompactQuery,
                    "help": self.dailyHelp
                }
            }
        }
        super().__init__(global_settings, parent_handler, config_path)

        self.daily_query_template = "function=TIME_SERIES_DAILY&symbol={}&outputsize={}&apikey={}"

    def buildQuery(self, query: str, *args) -> str:
        return self.api_url+query.format(*args)

    def sendRequest(self, query: str) -> str:
        return get(query)

    def dailyFullQuery(self, symbol: str) -> Optional[DataFrame]:
        request: Request = self.submit(self.daily_query_template,
                                       symbol, "full", self.api_key)

        if request.ok:
            df: DataFrame = DataFrame.from_dict(
                request.json(), orient="columns")
            print(df)
            return df
        else:
            # Do some handling
            return None

    def dailyCompactQuery(self, symbol: str) -> Optional[DataFrame]:
        request: Request = self.submit(self.daily_query_template,
                                       symbol, "compact", self.api_key)

        if request.ok:
            df: DataFrame = DataFrame.from_dict(
                request.json(), orient="columns")
            print(df)
        else:
            # Do some handling
            return None

    def help(self, args: str) -> str:
        return "source.yahoo_finance does not currently provide any save functionality"

    @staticmethod
    def dailyHelp() -> str:
        return "Gets historical time series data.\n\
            Compact retrieves the last 100 data points.\n\
            Full retrieves all historical data."


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
        # settings.ticker = args[0].upper()
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

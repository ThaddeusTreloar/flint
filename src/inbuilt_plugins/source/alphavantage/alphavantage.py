
from json import loads
from traceback import print_tb
from numpy import empty
from result import Err, Ok, Result
from sklearn.ensemble import RandomTreesEmbedding
from generics.actor import Actor
from generics.producer import Producer
from generics.source import ApiSource, ApiSourceSettings, PackageSource, Source
from abstract.settings import Settings
from typing import Any, Dict, List, Optional, Tuple, Union
from pathlib import Path
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.timeseries import TimeSeries
from pandas import DataFrame
from requests import Session
from csv import reader


class AlphaVantageSettings(ApiSourceSettings):

    @property
    def config_namespace(self) -> str:
        return "alphavantage"

    def __init__(self, global_settings: Any, plugins_dir_slug: str, module_name: str, config_path: Path = None) -> None:
        self.output_format: str = "pandas"
        self.indexing_type: str = "integer"
        super().__init__(global_settings, plugins_dir_slug, module_name, config_path)

    def interperateSetting(self, key, value) -> Tuple[str, Any]:

        match key:
            case "indexing_type":
                match value:
                    case "integer" | "date":
                        return key, value
                    case _:
                        print(
                            f"AlphaVantage indexing_type <{value}> not valid. Try 'date' or 'integer'\n\
                            defaulting to 'integer'...")
                        return key, "integer"
            case "output_format":
                match value:
                    case "pandas" | "json":
                        return key, value
                    case _:
                        print(
                            f"AlphaVantage output_format <{value}> not valid. Try 'pandas' or 'json'\n\
                            defaulting to 'pandas'...")
                        return key, "integer"
            case _:
                return key, value


class AlphaVantage(Source, ApiSource, Producer, PackageSource, Actor):

    @property
    def api_key(self) -> str:
        return self.local_settings.api_key

    @property
    def function_params(self) -> Dict[str, Union[str, Dict]]:
        return {
            "interval": {
                "daily": "daily",
                "intraday": {
                    "1min": "1min"
                }
            }
        }

    @property
    def formats(self) -> List[str]:
        return ["dataframe", "json"]

    @property
    def local_command_set(self) -> dict[str, object]:
        return self._local_command_set

    def __init__(self, global_settings: Settings, parent_handler: Any):
        self._local_command_set: dict[str, object] = {
            "help": self.help,
            "request": self.submitRequest,
            "api_key": self.getApiKey
        }

        '''
        "get": {
            "daily": {
                "full": self.dailyFullQuery,
                "compact": self.dailyCompactQuery,
                "help": self.dailyHelp
            }
        }'''
        Source.__init__(self, global_settings, parent_handler)

        self.local_settings = AlphaVantageSettings(
            self.global_settings,
            self.plugins_dir_slug(),
            "alphavantage"
        )

        '''with Session as session:
            url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&state=active&apikey={self.local_settings.api_key}'
            download = session.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            self.active_listed: List[str] ='''

        # print(f"Key: {self.local_settings.api_key}")

    def start(self) -> None:
        pass

    def submitRequest(self, function: str, **function_args) -> Result[Union[Dict, DataFrame], str]:

        match function:
            case "price":  # eg: source alphavantage request price symbol=AAPL required_points=100 interval=daily
                if all(("symbol" in function_args,
                        "required_points" in function_args,
                        "interval" in function_args,
                        )):
                    match self.validateSymbol(function_args["symbol"]):
                        case Ok(symbol):
                            return self.getPriceData(symbol=symbol)
                        case Err(e):
                            return Err(e)
            case "sector_performance":

                sp = SectorPerformances(key=self.api_key)

                sp.get_sector()

                return Err("Unimplemented")

            case _:
                return Err(f"Function <{function}> not recognised...")

    def validateSymbol(self, symbol: str) -> Result[str, str]:
        with Session() as session:
            url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={self.api_key}"
            response = session.get(url)
            match response.status_code:
                case 200:
                    symbol_search = loads(response.content)["bestMatches"]
                    symbol_search = [x["1. symbol"] for x in symbol_search]

                    if not symbol in symbol_search:
                        # todo: may fail on empty dictionary
                        return Err(f"Symbol <{symbol}> failed validation. Maybe try {[x for x in symbol_search]}")

                    return Ok(symbol)
                case _:
                    # todo
                    return Err(f"Symbol <{symbol}> failed validation: {response.status_code}")

    def getPriceData(self, symbol: str = "", required_points: int = 100, interval: str = "daily") -> Result[Union[Dict, DataFrame], str]:

        ts = TimeSeries(key=self.api_key,
                        output_format=self.local_settings.output_format,
                        indexing_type=self.local_settings.indexing_type)

        if required_points > 100:
            outputsize = "full"
        else:
            outputsize = "compact"
        try:
            match interval:
                case "daily":
                    res = ts.get_daily(symbol,
                                       outputsize=outputsize)
                    return Ok(res)
                case "weekly":
                    return Ok(ts.get_weekly())
        except ValueError as e:
            # todo: verbose response
            return Err("Request failed")

    def getApiKey(self) -> str:
        return self.api_key

    def help(self, args: str) -> str:
        return "todo"

    @staticmethod
    def description():
        return 'A source module that retrieves data from the alphavantage api.'

    @staticmethod
    def dailyHelp() -> str:
        return "Gets historical time series data.\n\
            Compact retrieves the last 100 data points.\n\
            Full retrieves all historical data."

    def exit(self) -> None:
        # todo
        ...

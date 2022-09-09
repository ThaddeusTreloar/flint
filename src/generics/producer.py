

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List
from pathlib import Path

from result import Result


class DataFormats(Enum):

    DataFrame = "dataframe"
    JSon = "json"


@dataclass
class AvailableData:
    pass


@dataclass
class FinancialTimeSeriesData(AvailableData):

    historical: bool
    intraday: bool
    intraday_delay_min: int
    open: bool
    high: bool
    low: bool
    close: bool
    volume: bool


@dataclass
class FinanancialSectorData(AvailableData):

    health_care: bool
    financials: bool
    materials: bool
    consumer_discretionary: bool
    energy: bool
    information_technology: bool
    industrials: bool
    real_estate: bool
    utilities: bool
    consumer_staples: bool
    communicaiton_services: bool


class Producer:

    @property
    @abstractmethod
    def available_data(self) -> AvailableData:
        pass

    @property
    def instruments(self) -> Dict[str, str]:
        '''
        Dict of financial instrument containers eg: NASDAQ, ASX, etc...
        Each containes all instruments available in that container.
        '''
        ...

    @property
    @abstractmethod
    def formats(self) -> List[str]:
        '''
        list of available datatypes.
        Should always include pandas.DataFrame
        '''
        ...

    @property
    def instrument_data_path(self) -> Path:
        '''
        This variable stores the location of the non-volatile copy of
        Producer.instruments.
        This stored copy will saved api calls and save time
        '''
        ...

    def UpdateInstruments(self) -> Result[None, str]:
        '''
        This function will update the available exchanges and tickers.
        Should update both Producer.instruments as well as the non-volatile
        copy stored at Producer.instrument_data_path
        '''
        ...

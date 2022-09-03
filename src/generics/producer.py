

from abc import abstractmethod
from enum import Enum
from typing import Any, List


class DataFormats(Enum):

    DataFrame = 0


class Producer:

    @property
    @abstractmethod
    def Formats(self) -> List[DataFormats]:
        ...

    def __init__(self) -> None:
        pass

    @abstractmethod
    def request_data(self, ) -> Any:
        ...

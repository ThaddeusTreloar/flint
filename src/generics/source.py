from generics import Generic
from abc import abstractmethod
from typing import Tuple, List, Any
from util import unimplemented


class Source(Generic):
    '''
    Generic parent module for pulling in source data
    Must implement:
        @property daemoniseThread (Whether the thread is dependant on the main thread)
        @property description (description of what the module does)
        @property local_command_set (Command set for this modules)
        method help (help dialogue for this module)
        method submit (entry point to start a query)
    '''

    @property
    @abstractmethod
    def threadable(self) -> bool:
        pass

    @staticmethod
    def plugins_dir_slug() -> str:
        return "source"

    def __init__(self, global_settings: Any, parent_handler: Any) -> None:
        super().__init__(global_settings, parent_handler)


class ApiSource(Source):

    '''
    Generic parent module for classes that contact a remote API
    Must implement:
        @property API key
        @property API url
        method buildQuery (builds a query for the api)
        method sendRequest (takes a query and sends the query to api)
    Parent module provides:
        method submit (
            Will submit a query with *args by sendRequest( buildQuery( *args ) )
        )
    '''

    @property
    @abstractmethod
    def api_key(self) -> str:
        pass

    @property
    @abstractmethod
    def api_url(self) -> str:
        pass

    @property
    def daemoniseThread(self) -> bool:
        False

    def __init__(self, global_settings: Any, parent_handler: Any) -> None:
        super().__init__(global_settings, parent_handler)

    def submit(self, *args) -> Any:  # todo: update all of below when completed
        self.buildAndSend(*args)

    @abstractmethod
    def buildQuery(self, *args) -> str:
        ...

    @abstractmethod
    def sendRequest(self, query: str, *args) -> str:
        ...

    def buildAndSend(self, *args) -> str:
        return self.sendRequest(self.buildQuery(*args))

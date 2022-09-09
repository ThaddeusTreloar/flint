from abstract import Settings
from generics import Generic
from abc import abstractmethod
from typing import Tuple, List, Any, Dict
from generics.actor import Actor
from generics.producer import Producer
from util import unimplemented
from pathlib import Path
from requests import Request


class Source(Generic, Producer, Actor):
    '''
    Generic parent module for pulling in source data
    Must implement:
        @property daemoniseThread (Whether the thread is dependant on the main thread)
        @property description (description of what the module does)
        @property local_command_set (Command set for this modules)
        method help (help dialogue for this module)
        method submit (entry point to start a query)
    '''

    @staticmethod
    def plugins_dir_slug() -> str:
        return "source"

    def __init__(self, global_settings: Any, parent_handler: Any) -> None:
        super().__init__(global_settings, parent_handler)


class ApiSourceSettings(Settings):

    @property
    def config_namespace(self) -> str:
        return "api_source"

    def __init__(self, config_path: Path) -> None:
        self.api_key: str = ""

        super().__init__(config_path)

    def interperateSetting(self, key, value) -> Tuple[str, Any]:
        match key:
            case _:
                return key, value


class ApiSource:

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
        @property daemoniseThread is set to False by default
    '''

    @property
    @abstractmethod
    def api_key(self) -> str:
        ...


class PackageSource:

    @property
    @abstractmethod
    def function_params(self) -> Dict[str, Dict[str, str]]:
        ...

    @abstractmethod
    def submitRequest(self) -> Any:
        ...


class UrlSource:

    @property
    @abstractmethod
    def api_url(self) -> str:
        ...

    def submitRequest(self, query_template: str, *args) -> Any:
        return self.sendRequest(self.buildQuery(query_template, *args))

    @abstractmethod
    def buildQuery(self, *args) -> str:
        ...

    @abstractmethod
    def sendRequest(self, query: str, *args) -> Any:
        ...

    # todo: may be needed
    def matchStatusCode(self, code: int) -> Any:
        ...


class FileSource:
    pass

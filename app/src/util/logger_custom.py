from asyncio.log import logger
from abc import ABC
from typing import Any
import datetime
#import dateutil.tz
import json
import logging
import inspect



root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

logging.basicConfig(format='%(message)s', level=logging.INFO)

class Logger(ABC):
    @staticmethod
    def info(method: str, message: str, data: Any = {}, self=None):
        logging.info(_get_dict(self=self, method=method, level="INFO", message=message, data=data))

    @staticmethod
    def error(message, self=None, data=None, method: str = None):
        logging.error(_get_dict(self=self, message=message, level="ERROR", data=data, method=method))

    @staticmethod
    def warning(message, self=None, data=None, method=None):
        logging.warning(_get_dict(self=self, message=message, level="WARN", data=data, method=method))

    @staticmethod
    def critical(message, self=None, data=None, method=None):
        logging.critical(_get_dict(self=self, message=message, level="CRITICAL", data=data, method=method))

    """
    inspect.stack => https://stackoverflow.com/questions/17065086/how-to-get-the-caller-class-name-inside-a-function-of-another-class-in-python
    methodName(inspect.stack()[1].frame.f_code.co_name, inspect.stack()[1][0].frame.f_code.co_name, inspect.stack()[1][3])
    className(inspect.stack()[1][0].f_locals["self"].__class__.__name__) 
    """
    @staticmethod
    def getMethodCurrent() -> str:
        className = inspect.currentframe().f_back.f_locals["self"].__class__.__name__
        methodName = inspect.currentframe().f_back.f_code.co_name
        return f'{className}.{methodName}'
        
    @staticmethod
    def getClassMethodCurrent() -> str:
        className = inspect.currentframe().f_back.f_locals["self"].__class__.__name__
        methodName = inspect.currentframe().f_back.f_code.co_name
        return f'{className}.{methodName}'

def _get_dict(self, method: str, level: str, message: str, data={}):
    # timeZone = dateutil.tz.gettz('America/Sao_Paulo')
    dictionaryLog = {
        # "timestamp": datetime.datetime.now(tz=timeZone).strftime("%Y-%m-%dT%H:%M:%S"),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "level": level,
        "application": "soat-fiap",
        "classMethod": method,
        "mensagem": message,
        "data": data 
    }
    dictionaryLog = {key: dictionaryLog[key] for key in dictionaryLog.keys() if dictionaryLog[key]}
    return json.dumps(dictionaryLog)

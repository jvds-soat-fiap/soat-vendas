from typing import Any, List, Generic, TypeVar
from abc import abstractmethod, ABC

# tipagem para model
T = TypeVar("T")

# tipagem para primary key
K = TypeVar("K")


class Database(Generic[T, K],ABC):
    @abstractmethod
    def insert(self, model: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: K, modelType: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, model: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def findById(self, id: K, modelType: T) -> T:
        raise NotImplementedError

    # def _getTypeModel(self, type: T) -> str:        
    #     raise NotImplementedError

    @abstractmethod
    def _getSession(self):
        raise NotImplementedError


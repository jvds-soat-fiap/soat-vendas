from typing import Any, List, Generic, TypeVar
from abc import abstractmethod, ABC

T = TypeVar("T")
K = TypeVar("K")


class Repository(Generic[T, K],ABC):
    @abstractmethod
    def save(self, entity: T) -> T:
        raise NotImplemented

    @abstractmethod
    def update(self, entity: T) -> T:
        raise NotImplemented

    @abstractmethod
    def delete(self, entity: T) -> bool:
        raise NotImplemented
    
    @abstractmethod
    def findById(self, id: K) -> T:
        raise NotImplemented        
    
    @abstractmethod
    def findByAll(self) -> List[T]:
        raise NotImplemented

    @abstractmethod
    def findByFilter(self, filter: Any) -> List[T]:
        raise NotImplemented

    @abstractmethod
    def _getSession(self):
        raise NotImplemented        

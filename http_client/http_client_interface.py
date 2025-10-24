from abc import ABC, abstractmethod

class HTTPClientInterface(ABC):
    @abstractmethod
    def get(self, endpoint):
        pass
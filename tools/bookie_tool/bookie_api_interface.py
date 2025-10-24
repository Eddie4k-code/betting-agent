from abc import ABC, abstractmethod

# Capabilites our agent expects from any bookie related API provider
class BookieAPIInterface(ABC):
    @abstractmethod
    def get_sports():
        pass

    def get_odds():
        pass

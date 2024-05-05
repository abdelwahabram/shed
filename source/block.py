from abc import ABC, abstractmethod

class Block(ABC):
    def __init__(self):
        pass
    

    @abstractmethod
    def create(self):
        pass


    @abstractmethod
    def read(self):
        pass
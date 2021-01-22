
# Author: Kirill Leontyev (DC)

from abc import ABC, abstractmethod



class Coder(ABC):
    
    @abstractmethod
    def encode(self, symb):
        pass

    @abstractmethod
    def decode(self, code):
        pass

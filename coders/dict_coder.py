
# Author: Kirill Leontyev (DC)

from coders.coder_interface import Coder



class Dict_coder(Coder):

    def __init__(self, assoc_list: list):
        self.__drive_dec = {}
        self.__drive_enc = {}
        for k, v in assoc_list:
            try:
                self.__drive_dec[int(v)] = k
                self.__drive_enc[k] = int(v)
            except TypeError:
                raise TypeError("Ошибка в списке кодов символов")
    
    def encode(self, symb: str):
        return self.__drive_enc[symb]
    
    def decode(self, code: int):
        return self.__drive_dec[code]

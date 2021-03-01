from .istr_reader import IStrReader


class StrReader(IStrReader):
    """
    StrReader is string buffer for reading string data.
    """
    __data: str                  # string buffer
    __pos: int                   # current position in string buffer

    def __init__(self, data = ""):
        super().__init__()
        self.set_data(data)

    def reset(self)-> None:
        """
        Reset buffer to init state
        :return: None
        """
        self.__pos = 0

    def set_data(self, data: str)-> None:
        """
        Set new string in buffer
        :param data: string of data
        :return: None
        """
        self.__data = data
        self.reset()              # reset buffer to init state

    def read(self, count = 1)-> str:
        """
        Read specified number of chars from string buffer
        :param count: number of read chars from string buffer
        :return: string of read chars
        :raise: ValueError
        """
        if count < 1:
            raise ValueError("count must be greater 0!!!")
        ans = self.__data[self.__pos: self.__pos + count]
        self.__pos += len(ans)                              # update position in buffer
        return ans

    def has_data(self)-> bool:
        """
        Has yet data in string buffer?
        :return: bool
        """
        return self.__pos < len(self.__data)
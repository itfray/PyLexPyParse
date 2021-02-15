import abc


class IStrReader(abc.ABC):
    """
    IStrReader is string buffer for reading string data.
    """
    @abc.abstractmethod
    def reset(self)-> None:
        """
        Reset buffer to init state
        :return: None
        """
        return

    @abc.abstractmethod
    def read(self, count: int)-> str:
        """
        Read specified number of chars from string buffer
        :param count: number of read chars from string buffer
        :return: string of read chars
        """
        return ""

    @abc.abstractmethod
    def has_data(self)-> bool:
        """
        Has yet data in string buffer?
        :return: True or False
        """
        return False


class StrReader(IStrReader):
    __buf: str                              # string buffer
    __pos: int                              # current position in string buffer

    def __init__(self, data = ""):
        super().__init__()
        self.set_data(data)

    def reset(self):
        self.__pos = 0

    def set_data(self, data: str):
        self.__buf = data
        self.reset()

    def read(self, count = 1):
        if count < 1:
            raise ValueError("count must be greter 0!!!")
        ans = self.__buf[self.__pos: self.__pos + count]
        self.__pos += len(ans)
        return ans

    def has_data(self):
        return self.__pos < len(self.__buf)

class FileStrReader(StrReader):
    __filename: str
    __file: IO

    def __init__(self, filename = ""):
        super().__init__()

    def set_filename(self, filename: str):
        self.__filename = filename
        self.__close()

    def __close(self):
        if not self.__file.closed:
            self.__file.close()

    def __open(self):
        self.__file = open(self.__filename, 'r')


if __name__ == "__main__":
    pass
import abc
import os
import time


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
    __data: str                              # string buffer
    __pos: int                               # current position in string buffer

    def __init__(self, data = ""):
        super().__init__()
        self.set_data(data)

    def reset(self):
        self.__pos = 0

    def set_data(self, data: str):
        self.__data = data
        self.reset()

    def read(self, count = 1):
        if count < 1:
            raise ValueError("count must be greater 0!!!")
        ans = self.__data[self.__pos: self.__pos + count]
        self.__pos += len(ans)
        return ans

    def has_data(self):
        return self.__pos < len(self.__data)


class FileStrReader(IStrReader):
    DEFAULT_BUFFERING = -1
    DEFAULT_ENCODING = 'utf-8'
    __file = None
    __file_size: int

    def __init__(self, filename="", **kwargs):
        super().__init__()
        if len(filename) > 0:
            self.open(filename, **kwargs)

    def close(self):
        if not self.__file is None:
            self.__file.close()
        self.__file = None

    def open(self, filename: str, **kwargs):
        try:
            buffering = kwargs.get("buffering", self.DEFAULT_BUFFERING)
            encoding = kwargs.get("encoding", self.DEFAULT_ENCODING)
            self.__file = open(filename, 'r', buffering, encoding)
            self.__file_size = os.stat(filename).st_size
        except Exception as err:
            self.close()
            raise err

    def reset(self) -> None:
        if not self.__file is None:
            self.__file.seek(0)

    def read(self, count: int) -> str:
        if self.__file is None:
            raise OSError("Can not read data from file!!! Opened file is not found!!!")
        if count < 1:
            raise ValueError("count must be greater 0!!!")
        return self.__file.read(count)

    def has_data(self):
        return False if self.__file is None else self.__file.tell() < self.__file_size

    def filename(self)-> str:
        return "" if self.__file is None else self.__file.name

    def __del__(self):
        self.close()


if __name__ == "__main__":
    data = "Hello\nMy\nWorld!!!"
    filename = "test_str_file.txt"

    t0 = time.time()
    reader = FileStrReader(filename=filename, buffering=-1)
    while reader.has_data():
        print(reader.read(38), end="")

    print()
    print()
    print(time.time() - t0, "sec")
    print()

    reader = StrReader(data)
    while reader.has_data():
        print(reader.read(1), end="")
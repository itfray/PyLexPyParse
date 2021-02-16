import abc
from typing import IO
import os


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

    # @abc.abstractmethod
    # def readline(self)-> str:
    #     pass
    #
    # @abc.abstractmethod
    # def readlines(self):
    #     pass


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
            raise ValueError("count must be greater 0!!!")
        ans = self.__buf[self.__pos: self.__pos + count]
        self.__pos += len(ans)
        return ans

    def has_data(self):
        return self.__pos < len(self.__buf)


class FileStrReader(IStrReader):
    DEF_BUF_SIZE = 256
    __buf: str
    __buf_size: int
    __pos: int
    __file = None
    __file_size: int

    def __init__(self, **kwargs):
        super().__init__()
        filename = kwargs.get("filename", None)
        buf_size = kwargs.get("buf_size", self.DEF_BUF_SIZE)
        if filename:
            self.open(filename)
        self.set_buf_size(buf_size)

    def set_buf_size(self, size: int):
        if size <= 0:
            raise ValueError("Uncorrect buf size!!!")
        self.__buf_size = size

    def close(self):
        if not self.__file is None:
            self.__file.close()
        self.__file = None
        self.reset()

    def open(self, filename: str):
        try:
            self.reset()
            self.__file = open(filename, mode='r', encoding='utf-8')
            self.__file_size = os.stat(filename).st_size
        except Exception as err:
            self.close()
            raise err

    def reset(self) -> None:
        self.__buf = ""
        self.__pos = 0
        if not self.__file is None:
            self.__file.seek(0)

    def read(self, count: int) -> str:
        if self.__file is None:
            raise FileNotFoundError("Can not read data from file!!! Opened file is not found!!!")
        if count < 1:
            raise ValueError("count must be greater 0!!!")
        eof = False
        size_data = count if count > self.__buf_size else self.__buf_size
        new_pos = self.__pos + count
        if new_pos > len(self.__buf):
            data = self.__file.read(size_data)
            self.__buf = data if self.__pos >= len(self.__buf) else\
                         self.__buf[self.__pos: len(self.__buf)] + data
            self.__pos = 0
            new_pos = count
            eof = len(data) < size_data and new_pos >= len(self.__buf)
        ans = self.__buf[self.__pos: new_pos]
        if eof:
            self.__buf = ""
        else:
            self.__pos += len(ans)
        return ans

    def has_data(self):
        if self.__file is None:
            return False
        return self.__file.tell() < self.__file_size or len(self.__buf) > 0


    def filename(self)-> str:
        if self.__file is None:
            return ""
        return self.__file.name

    def __del__(self):
        self.close()



if __name__ == "__main__":
    filename = "test_str_file.txt"
    reader = FileStrReader(filename=filename)
    while reader.has_data():
        print(reader.read(10), end="")
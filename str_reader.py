import abc
from typing import IO


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
    __filename: str
    __file = None

    def __init__(self, filename, buf_size = DEF_BUF_SIZE):
        super().__init__()
        self.set_file(filename)
        self.set_buf_size(buf_size)

    def set_file(self, filename: str):
        self.__filename = filename
        self.__close()
        self.__open()

    def set_buf_size(self, size: int):
        if size <= 0:
            raise ValueError("Uncorrect buf size!!!")
        self.__buf_size = size

    def __close(self):
        if not self.__file is None:
            self.__file.close()
        self.__file = None

    def __open(self):
        try:
            self.__file = open(self.__filename, mode='r', encoding='utf-8')
        except Exception as err:
            raise err
        finally:
            self.__close()

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
        size_data = count if count > self.__buf_size else self.__buf_size
        new_pos = self.__pos + count
        if new_pos > len(self.__buf):
            self.__buf = self.__buf[self.pos: len(self.__buf)] + self.__file.read(size_data)
            self.__pos = 0
            new_pos = count
        ans = self.__buf[self.__pos: new_pos]
        self.__pos += len(ans)
        return ans

    def has_data(self):
        if self.__file is None:
            return False
        self.__file.flush()


    def __del__(self):
        self.__close()



if __name__ == "__main__":
    data = "Hello!!!"
    reader = StrReader(data)
    for i in range(len(data)):
        print(f"{i}: {reader.read()}")
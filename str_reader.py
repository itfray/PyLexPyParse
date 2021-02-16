import abc
import os
import time


class IStrReader(abc.ABC):
    """
    IStrReader is interface of string buffer for reading string data.
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


class FileStrReader(IStrReader):
    """
    FileStrReader is string buffer for reading string data from file.
    """
    DEFAULT_BUFFERING = -1                           # size buffer for reading from file
    DEFAULT_ENCODING = 'utf-8'                       # what encoding for reading from file
    __file = None                                    # handler of file
    __file_size: int                                 # size of file (number of bytes)

    def __init__(self, filename="", **kwargs):
        super().__init__()
        if len(filename) > 0:
            self.open(filename, **kwargs)

    def close(self)-> None:
        """
        Close file
        :return: None
        """
        if not self.__file is None:
            self.__file.close()
        self.__file = None

    def open(self, filename: str, **kwargs)-> None:
        """
        Open file
        :param filename: path to file
        :param kwargs:
            :param buffering: size buffer for reading from file
            :param encoding: what encoding for reading from file
        :return: None
        """
        try:
            buffering = kwargs.get("buffering", self.DEFAULT_BUFFERING)
            encoding = kwargs.get("encoding", self.DEFAULT_ENCODING)
            self.__file = open(filename, 'r', buffering, encoding)
            self.__file_size = os.stat(filename).st_size
        except Exception as err:
            self.close()
            raise err

    def reset(self) -> None:
        """
        Reset string buffer and position in file to init state.
        :return: None
        """
        if not self.__file is None:
            self.__file.seek(0)                                 # set pointer in file to start of file

    def read(self, count = 1) -> str:
        """
        Read specified number of chars from string buffer readed from file
        :param count: number of read chars from string buffer
        :return: string of read chars
        """
        if self.__file is None:
            raise OSError("Can not read data from file!!! Opened file is not found!!!")
        if count < 1:
            raise ValueError("count must be greater 0!!!")
        return self.__file.read(count)

    def has_data(self):
        """
        Has yet data in file?
        :return: True or False
        """
        return False if self.__file is None else self.__file.tell() < self.__file_size

    def filename(self)-> str:
        """
        :return: string filename
        """
        return "" if self.__file is None else self.__file.name

    def __del__(self):
        self.close()


# if __name__ == "__main__":
#     data = ""
#     filename = "test_str_file.txt"
#
#     reader = FileStrReader(filename=filename, buffering=768)
#     while reader.has_data():
#         readed = reader.read(38)
#         print(readed, end="")
#         data += readed
#
#     print('\n')
#
#     reader = StrReader(data)
#     while reader.has_data():
#         print(reader.read(38), end="")
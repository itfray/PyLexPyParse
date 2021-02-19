from .istr_reader import IStrReader


class FileStrReader(IStrReader):
    """
    FileStrReader is string buffer for reading string data from file.
    """
    DEFAULT_BUFFERING = -1                           # size buffer for reading from file
    DEFAULT_ENCODING = 'utf-8'                       # what encoding for reading from file
    __file = None                                    # handler of file

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

    def filename(self)-> str:
        """
        :return: string filename
        """
        return "" if self.__file is None else self.__file.name

    def __del__(self):
        self.close()
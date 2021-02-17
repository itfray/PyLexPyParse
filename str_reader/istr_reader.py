import abc

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

    @abc.abstractmethod
    def read(self, count: int)-> str:
        """
        Read specified number of chars from string buffer
        :param count: number of read chars from string buffer
        :return: string of read chars
        """

    @abc.abstractmethod
    def has_data(self)-> bool:
        """
        Has yet data in string buffer?
        :return: True or False
        """
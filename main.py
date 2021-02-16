from str_reader import IStrReader
from str_reader.str_reader import StrReader
from str_reader.file_reader import FileStrReader


reader = StrReader('Hello my batya!!!')
while reader.has_data():
    print(reader.read(1), end="")
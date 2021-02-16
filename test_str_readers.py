import unittest
from str_reader import StrReader, FileStrReader


class TestStrReaderCase(unittest.TestCase):
    def test_init(self):
        reader = StrReader()
        self.assertEqual(reader._StrReader__buf, "", "buf init error!!!")
        self.assertEqual(reader._StrReader__pos, 0, "pos init error!!!")
        strdata = "data"
        reader = StrReader(strdata)
        self.assertEqual(reader._StrReader__buf, strdata, "buf init error!!!")
        self.assertEqual(reader._StrReader__pos, 0, "pos init error!!!")

    def test_set_data(self):
        strdata = "data"
        reader = StrReader()
        reader.set_data(strdata)
        self.assertEqual(reader._StrReader__buf, strdata, "buf error!!!")

    def test_read(self):
        strdata = "data"
        reader = StrReader(strdata)
        self.assertEqual(strdata[0], reader.read(), "read() error!!!")
        self.assertEqual(reader._StrReader__pos, 1, "pos error!!!")
        self.assertEqual(strdata[1:len(strdata)], reader.read(len(strdata) - 1), "read() error!!!")
        reader.reset()
        self.assertEqual(reader._StrReader__pos, 0, "pos error!!!")
        try:
            reader.read(-1)
            self.assert_(False, "count must be greter 0!!!")
        except ValueError:
            pass
        try:
            reader.read(0)
            self.assert_(False, "count must be greter 0!!!")
        except ValueError:
            pass
        self.assertEqual(strdata, reader.read(len(strdata)), "read() error!!!")
        reader.reset()
        self.assertEqual(strdata[0], reader.read(1), "read() error!!!")
        self.assertEqual(strdata[1:len(strdata)], reader.read(len(strdata)), "read() error!!!")
        reader.reset()
        self.assertEqual(strdata[:5000], reader.read(5000), "read() error!!!")
        self.assertEqual(strdata[len(strdata):5000], reader.read(5000), "read() error!!!")
        reader.reset()
        reader.read(5000)
        reader.read(5000)
        self.assertEqual(reader._StrReader__pos, 4, "pos error!!!")

    def test_has_data(self):
        strdata = "data"
        reader = StrReader(strdata)
        reader.read(5000)
        self.assertEqual(reader._StrReader__pos, 4, "pos error!!!")
        self.assertEqual(reader.has_data(), False, "has_data() error!!!")
        reader.reset()
        reader.read(1)
        self.assertEqual(reader._StrReader__pos, 1, "pos error!!!")
        self.assertEqual(reader.has_data(), True, "has_data() error!!!")
        reader.read(len(strdata) - 2)
        self.assertEqual(reader._StrReader__pos, len(strdata) - 1, "pos error!!!")
        self.assertEqual(reader.has_data(), True, "has_data() error!!!")
        reader.read(1)
        self.assertEqual(reader._StrReader__pos, len(strdata), "pos error!!!")
        self.assertEqual(reader.has_data(), False, "has_data() error!!!")


class TestFileStrReaderCase(unittest.TestCase):
    def test_init(self):
        filename = "test_str_file.txt"
        try:
            reader = FileStrReader("")
            self.assert_(False, "Must be raised FileNotFoundError!!! No such file or directory: ''!!!")
        except FileNotFoundError as err:
            pass

        reader = FileStrReader(filename)
        self.assertEqual(reader.DEF_BUF_SIZE, reader._FileStrReader__buf_size, "buf_size error!!!")
        self.assertEqual(reader._FileStrReader__file is None, False, "file open error!!!")

        reader = FileStrReader(filename, 200)
        self.assertEqual(200, reader._FileStrReader__buf_size, "buf_size error!!!")

        try:
            reader = FileStrReader(filename, -2)
            self.assert_(False, "Must be raised ValueError!!! buf_size must be greater 0!!!")
        except ValueError as err:
            pass

    def test_set_file(self):
        filename = "test_str_file.txt"
        reader = FileStrReader(filename)
        try:
            reader.set_file('')
            self.assert_(False, "Must be raised FileNotFoundError!!! No such file or directory: ''!!!")
        except FileNotFoundError as err:
            pass
        self.assertEqual(reader._FileStrReader__file is None, True, "file close error!!!")
        self.assertEqual(reader.filename(), "", "file close error!!!")
        reader.set_file(filename)
        self.assertEqual(not reader._FileStrReader__file is None, True, "file open error!!!")
        self.assertEqual(reader.filename(), filename, "file open error!!!")


if __name__ == '__main__':
    unittest.main()

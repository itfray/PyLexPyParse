import unittest
from str_reader import StrReader


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



if __name__ == '__main__':
    unittest.main()

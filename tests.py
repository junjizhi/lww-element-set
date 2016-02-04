"""unit tests for the lww_set 
   Each test case correponds to a data row of the table in README.md. 
"""

import unittest
from lww import LWW_set

class Test_LWW_Set(unittest.TestCase):
    def setUP(self):
        pass

    def test1(self):
        lww = LWW_set()
        lww.add(1,1)
        self.assertTrue(lww.exist(1))
        lww.add(1,0)
        self.assertTrue(lww.exist(1))
        expected_arr = [1,]
        self.assertEqual(lww.get(), expected_arr)

    def test2(self):
        lww = LWW_set()
        lww.add(1,1)
        self.assertTrue(lww.exist(1))
        lww.add(1,1)
        self.assertTrue(lww.exist(1))
        expected_arr = [1,]
        self.assertEqual(lww.get(), expected_arr)

    def test3(self):
        lww = LWW_set()
        lww.add(1,1)
        self.assertTrue(lww.exist(1))
        lww.add(1,2)
        self.assertTrue(lww.exist(1))
        expected_arr = [1,]
        self.assertEqual(lww.get(), expected_arr)

    def test4(self):
        lww = LWW_set()
        lww.remove(1,1)
        self.assertFalse(lww.exist(1))
        lww.add(1,0)
        self.assertFalse(lww.exist(1))
        expected_arr = []
        self.assertEqual(lww.get(), expected_arr)

    def test5(self):
        lww = LWW_set()
        lww.remove(1,1)
        self.assertFalse(lww.exist(1))
        lww.add(1,1)
        self.assertTrue(lww.exist(1))
        expected_arr = [1,]
        self.assertEqual(lww.get(), expected_arr)

    def test6(self):
        lww = LWW_set()
        lww.remove(1,1)
        self.assertFalse(lww.exist(1))
        lww.add(1,2)
        self.assertTrue(lww.exist(1))
        expected_arr = [1,]
        self.assertEqual(lww.get(), expected_arr)

    def test7(self):
        lww = LWW_set()
        lww.remove(1,1)
        self.assertFalse(lww.exist(1))
        lww.remove(1,0)
        self.assertFalse(lww.exist(1))
        expected_arr = []
        self.assertEqual(lww.get(), expected_arr)

    def test8(self):
        lww = LWW_set()
        lww.remove(1,1)
        self.assertFalse(lww.exist(1))
        lww.remove(1,1)
        self.assertFalse(lww.exist(1))
        expected_arr = []
        self.assertEqual(lww.get(), expected_arr)

    def test8(self):
        lww = LWW_set()
        lww.remove(1,1)
        self.assertFalse(lww.exist(1))
        lww.remove(1,2)
        self.assertFalse(lww.exist(1))
        expected_arr = []
        self.assertEqual(lww.get(), expected_arr)

    def test9(self):
        lww = LWW_set()
        lww.remove(1,1)
        self.assertFalse(lww.exist(1))
        lww.remove(1,0)
        self.assertFalse(lww.exist(1))
        expected_arr = []
        self.assertEqual(lww.get(), expected_arr)

    def test10(self):
        lww = LWW_set()
        lww.add(1,1)
        self.assertTrue(lww.exist(1))
        lww.remove(1,0)
        self.assertTrue(lww.exist(1))
        expected_arr = [1,]
        self.assertEqual(lww.get(), expected_arr)

    def test11(self):
        lww = LWW_set()
        lww.add(1,1)
        self.assertTrue(lww.exist(1))
        lww.remove(1,1)
        self.assertTrue(lww.exist(1))
        expected_arr = [1,]
        self.assertEqual(lww.get(), expected_arr)

    def test12(self):
        lww = LWW_set()
        lww.add(1,1)
        self.assertTrue(lww.exist(1))
        lww.remove(1,2)
        self.assertFalse(lww.exist(1))
        expected_arr = []
        self.assertEqual(lww.get(), expected_arr)

        
if __name__ == '__main__':
    unittest.main()


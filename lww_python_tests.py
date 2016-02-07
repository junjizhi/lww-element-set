"""unit tests for the lww_set"""

import unittest
from lww_python import LWW_python as LWW_set
import threading

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

    def test_string_add_remove(self):
        lww = LWW_set()
        a = "s1"
        b = "s22"
        lww.add(a,1)
        self.assertTrue(lww.exist(a))
        self.assertFalse(lww.exist(b))
        lww.add(b,1)
        lww.remove(a, 2)
        self.assertTrue(lww.exist(b))
        self.assertFalse(lww.exist(a))
        expected_arr = [b,]
        self.assertEqual(lww.get(), expected_arr)

    def test_multi_threaded(self):
        """Uses mutiple add/remove threads to test an lww-set object."""

        lww = LWW_set()
        base = [1,2,3,4]       
        element = 2
        nTests = 100
        for i in range(nTests):
            threads = []
            # For every test round, we increase the timestamp
            timestamps = base * (i+1) 
            

            # remove timestamp3 is always largest. add timestamp is always second
            remove_timestamp1 = timestamps[0]
            remove_timestamp2 = timestamps[1]
            add_timestamp = timestamps[2]
            remove_timestamp3 = timestamps[3]

            addThread = AddThread(lww, element, add_timestamp)
            removeThread1 = RemoveThread(lww, element, remove_timestamp1)
            removeThread2 = RemoveThread(lww, element, remove_timestamp2)
            removeThread3 = RemoveThread(lww, element, remove_timestamp3)

            threads.append(removeThread1)
            threads.append(removeThread2)            
            threads.append(removeThread3)
            threads.append(addThread)

            for t in threads:
                t.start()

            for t in threads:
                t.join()

            # Since only removeThread1 has the higher than the add thread,
            # eventually the element will be removed. 
            # If there is any race condition, i.e., one old remove thread
            # overwrites a new one, then the below assertion may fail. 
            self.assertFalse(lww.exist(element))


class AddThread (threading.Thread):
    def __init__(self, lww_set, element, timestamp):
        threading.Thread.__init__(self)
        self.lww_set = lww_set
        self.timestamp = timestamp
        self.element = element
    def run(self):
        self.lww_set.add(self.element, self.timestamp)

class RemoveThread (threading.Thread):
    def __init__(self, lww_set, element, timestamp):
        threading.Thread.__init__(self)
        self.lww_set = lww_set
        self.timestamp = timestamp
        self.element = element
    def run(self):
        self.lww_set.remove(self.element, self.timestamp)

        
if __name__ == '__main__':
    unittest.main()


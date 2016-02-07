from threading import *
from lww_interface import LWW_set

class LWW_python(LWW_set):
    """A Last-Writer-Win element set with Python dict. 

    See base class LWW_set for detals. 
    """
    def __init__(self):
        self.add_set = {}       
        self.remove_set = {}
        self.add_lock = RLock()
        self.remove_lock = RLock()

    def add(self, element, timestamp):
        """Add an element to lww_set, or update the existing element timestamp
        
        See base class LWW_set for detals. 
        """

        if not isinstance (timestamp, (int, long)):
            raise ValueError("timestamp must be an integer or long!")

        return_flag = True
        self.add_lock.acquire()
        # since the operation is on python dictionarily, there should
        # not be any exceptions at anytime, but to be safe, we use
        # try/except here
        try:                    
            self.__test_and_add(self.add_set, element, timestamp)
        except:
            return_flag = False
        finally:
            self.add_lock.release()  # make sure to release the lock in any situation

        return return_flag

    def __test_and_add(self, target_set, element, timestamp):
        """A non-atomic test and add function helper 

        The wrapper function that inserts the element if not
        exist. Otherwise, update the timestamp if the passed
        timestamp is newer(or larger) than the existing element's
        timestamp. 

        Note that this function is non-atomic. Invoking of this
        function is supposed protected by a lock. Otherwise data race
        could happen.

        Keyword arguments:
        target_set -- either add_set or remove_set
        element -- an object that has a unique identifier
        timestamp -- a non-negaive number (int or long)

        """
        if element in target_set:
            current_timestamp = target_set[element]
            if current_timestamp < timestamp:
                target_set[element] = timestamp
        else:
            target_set[element] = timestamp

    def remove(self, element, timestamp):
        """Remove an element from lww_set 

        See base class LWW_set for detals. 
        """
        if not isinstance (timestamp, (int, long)):
            raise ValueError("timestamp must be an integer or long!")

        return_flag = True
        self.remove_lock.acquire()
        # since the operation is on python dictionarily, there should
        # not be any exceptions at anytime, but to be safe, we use
        # try/except here
        try:
            self.__test_and_add(self.remove_set, element, timestamp)
        except:
            return_flag = False
        finally:
            self.remove_lock.release()  # make sure to release the lock in any situation
        return return_flag

    def exist(self, element):
        """Check if the element exists in lww-set 

        See base class LWW_set for detals. 
        """
        try:
            if element not in self.add_set:  # Checking the dict is atomic and thread-safe
                return False
            elif element not in self.remove_set:
                return True
            elif self.add_set[element] >= self.remove_set[element]:
                return True
            else:
                return False        
        except:
            raise RuntimeError("An internal error occurs when accessing lww-set. A retry may solve the problem. ")
    
    def get(self):
        """Returns an array of all existing elements in lww-set 

        See base class LWW_set for detals.
        """
        result = []
        for element in self.add_set:
            if self.exist(element):
                result.append(element)
        return result

from threading import *

class LWW_set:
    """A Last-Writer-Win element set.  

    This set stores only one instance of each element in the set, and
    associates it with a timestamp,(lww_set element, timestamp). The
    design of such set is implemented with two separate sets: add_set
    and remove_set.

    For a lww-set: 1) An element is in the set if its most-recent
    operation was an add, or when add or remove operation have the
    same timestamp(i.e., we bias add). 2) An element is not in the set
    if its most-recent operation was a remove, or there exists no such
    element in either add or remove set.

    Keyword attributes: 
    add_set -- a separate set of add operations recorded.
    remove_set -- a separate set of remove operations recorded
    """
    def __init__(self):
        self.add_set = {}       # built-in dictionaries are thread-safe. 
        self.remove_set = {}
        self.add_lock = Lock()
        self.remove_lock = Lock()

    def add(self, element, timestamp):
        """Add an element to lww_set 

        When accessing concurrently with other processes/threads, the
        timestamp of an element may be overwritten by another's newer
        timestamp.  Therefore, there is no guarantee that this method
        succeeds, and the return value is always none.

        Keyword arguments: 
        element -- an object that has a unique identifier
        timestamp -- a non-negaive number (int or long)

        Keyword returns:
        None

        Keyword raise:
        -ValueError: bad timestamp argument
        """
        if not isinstance (timestamp, (int, long)):
            raise ValueError("timestamp must be an integer or long!")

        self.add_lock.acquire()
        self.test_and_add(self.add_set, element, timestamp)
        self.add_lock.release()

    def test_and_add(self, target_set, element, timestamp):
        if element in target_set:
            current_timestamp = target_set[element]
            if current_timestamp < timestamp:
                target_set[element] = timestamp
        else:
            target_set[element] = timestamp

    def remove(self, element, timestamp):
        """Remove an element from lww_set 

        When accessing concurrently with other processes/threads, the
        timestamp of an element may be overwritten by another's newer
        timestamp.  Therefore, there is no guarantee that this method
        succeeds, and the return value is always none.

        Keyword arguments: 
        element -- an object that has a unique identifier
        timestamp -- a non-negaive number (int or long)

        Keyword returns:
        None

        Keyword raise:
        -ValueError: bad timestamp argument
        """
        if not isinstance (timestamp, (int, long)):
            raise ValueError("timestamp must be an integer or long!")

        self.remove_lock.acquire()
        self.test_and_add(self.remove_set, element, timestamp)
        self.remove_lock.release()

    def exist(self, element):
        """Check if the element exists in lww-set 

        The method is read-only. When other processes/threads are
        calling add() or remove() concurrently, it is possible that
        this method does not return the most recent result. However,
        the result will be eventually correct when all other
        operations actually complete.

        Keyword arguments: 
        element -- an object that has a unique identifier

        Keyword returns:
        -True: The element exists in lww-set
        -False: The element does not exists in lww-set
        """

        if element not in self.add_set:  # Checking the dict is atomic and thread-safe
            return False
        elif element not in self.remove_set:
            return True
        elif self.add_set[element] >= self.remove_set[element]:
            return True
        else:
            return False        
    
    def get(self):
        """Returns an array of all existing elements in lww-set 

        Similar to exist(), when this method is invoked concurrently
        with add() or remove() operations, it is possible that it does
        not return the most recent result. However, the result will be
        eventually correct when other operations actually complete.
                
        Keyword returns:
        an array of all elements

        """
        result = []
        for element in self.add_set:
            if self.exist(element):
                result.append(element)
        return result

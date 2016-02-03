
class LWW_set:
    """A Last-Writer-Win element set.
    This set stores only one instance of each element in the set, and associates it with a timestamp. The design of such set is implemented with two separate sets: add_set and remove_set. 
    For a lww-set:
    -An element is in the set if its most-recent operation was an add, or when add or remove operation have the same timestamp(i.e., we bias add) 
    -An element is not in the set if its most-recent operation was a remove, or there exists no such element in either add or remove set. 

    Attributes:
    -add_set: a separate set of add operations recorded. Each entry is a tuple of (lww_set element, timestamp).
    -remove_set: a separate set of remove operations recorded. Each entry is a tuple of (lww_set element, timestamp).
    """
    def __init__(self):
        pass

    def add(self, element, timestamp):
        """Add an element to lww_set
        When accessing concurrently with other processes/threads, the timestamp of an element may be overwritten by another's newer timestamp. Therefore, there is no guarantee that this method succeeds, and the return value is always none. 

        Args:
        -element: an object that has a unique identifier which is used to differentiate from other elements
        -timestamp: a non-negaive number (int or long) that associates with each element. The larger the timestamp, the more recent the element is. 
        
        Returns:
        None

        Raise:
        -RuntimeError: An internal error has occured. 
        
        """
        pass

    def remove(self, element, timestamp):
        """Remove an element to lww_set
        When accessing concurrently with other processes/threads, the timestamp of an element may be overwritten by another's newer timestamp. Therefore, there is no guarantee that this method succeeds, and the return value is always none. 

        Args:
        -element: an object that has a unique identifier which is used to differentiate from other elements
        -timestamp: a non-negaive number (int or long) that associates with each element. The larger the timestamp, the more recent the element is. 
        
        Returns:
        None

        Raise:
        -RuntimeError: An internal error has occured
        
        """
        pass
    
    def exist(self, element):
        """Check if the element exists in lww-set

        Args:
        -element: an object that has a unique identifier which is used to differentiate from other elements

        Returns:
        -True: The element exists in lww-set
        -False: The element does not exists in lww-set 

        Raise:
        -RuntimeError: An internal error has occured
        """
        pass
    
    def get(self):
        """Returns an array of all existing elements in lww-set
        Args:
        None
        
        Returns:
        -an array of all (element, timestamp) tuples
        
        Raise:
        -RuntimeError: An internal error has occured
        """
        pass

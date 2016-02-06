"""An LWW_set interface"""

class LWW_set:
    """A Last-Writer-Win element set.  

    This set stores only one instance of each element, and associates
    each element with a timestamp, i.e., (lww_set element,
    timestamp). 
    """
    def __init__(self):
        pass

    @property
    def add(self, element, timestamp):
        """Add an element to lww_set, or update the existing element timestamp

        If the operation has the most recent timestamp, the operation
        will eventually succeed. Otherwise, when other processes or
        threads are invoking add() or remove() operations concurrently
        with this method, the timestamp of an element may be
        overwritten by another newer timestamp.  Therefore, there is
        no guarantee that this method succeeds.  The return value is
        always none and does not indicate the success of this
        operation.

        Keyword arguments: 
        element -- an object that has a unique identifier
        timestamp -- a non-negaive number (int or long)

        Keyword returns:
        None

        Keyword raise:
        -ValueError: bad timestamp argument
        """
        raise NotImplementedError("Subclasses should implement this!")

    @property
    def remove(self, element, timestamp):
        """Remove an element from lww_set 

        If the operation has the most recent timestamp, the operation
        will eventually succeed. Otherwise, when other processes or
        threads are invoking add() or remove() operations concurrently
        with this method, the timestamp of an element may be
        overwritten by another newer timestamp.  Therefore, there is
        no guarantee that this method succeeds.  The return value is
        always none and does not indicate the success of this
        operation.

        Keyword arguments: 
        element -- an object that has a unique identifier
        timestamp -- a non-negaive number (int or long)

        Keyword returns:
        None

        Keyword raise:
        -ValueError: bad timestamp argument
        """
        raise NotImplementedError("Subclasses should implement this!")        

    @property
    def exist(self, element):
        """Check if the element exists in lww-set 

        For an lww-set: 1) An element is in the set if its most-recent
        operation was an add, or when add or remove operation have the
        same timestamp(i.e., we bias add). 2) An element is not in the
        set if its most-recent operation was a remove, or there exists
        no such element in either add or remove set.

        The method is read-only. When other processes/threads are
        calling add() or remove() concurrently, it is possible that
        this method does not return the most recent result. However,
        the result will be eventually up-to-date when all other
        operations actually complete.

        Keyword arguments: 
        element -- an object that has a unique identifier

        Keyword returns:
        -True: The element exists in lww-set
        -False: The element does not exists in lww-set
        """
        raise NotImplementedError("Subclasses should implement this!")
    
    @property
    def get(self):
        """Returns an array of all existing elements in lww-set 

        Similar to exist(), when this method is invoked concurrently
        with add() or remove() operations, it is possible that it does
        not return the most recent result. However, the result will be
        eventually up-to-date when other operations actually complete.
                
        Keyword returns:
        an array of all elements
        """
        raise NotImplementedError("Subclasses should implement this!")

from threading import *
from lww_interface import LWW_set

class LWW_redis(LWW_set):
    """A Last-Writer-Win element set based on redis ZSET. 

    lww-set stores the add/remove operations in a remote 
    redis server. 

    Keyword attributes:
    redis -- an opened connection with a redis server

    """
    def __init__(self, redis):
        self.redis = redis
        self.add_lock = RLock()
        self.remove_lock = RLock()

    def add(self, element, timestamp):
        """Add an element to lww_set, or update the existing element timestamp

        """
        if not isinstance (timestamp, (int, long)):
            raise ValueError("timestamp must be an integer or long!")

        timestamp = float(timestamp)

        self.add_lock.acquire()
        self.__test_and_add("lww_add_set", element, timestamp)
        self.add_lock.release()

    def __test_and_add(self, target_set, element, timestamp):

        existing_timestamp = self.redis.zscore(target_set, element)
        if existing_timestamp != None:
            if existing_timestamp < timestamp:
                self.redis.zadd(target_set, timestamp, element)
        else:
            self.redis.zadd(target_set, timestamp, element)

    def remove(self, element, timestamp):
        """Remove an element from lww_set 

        """
        if not isinstance (timestamp, (int, long)):
            raise ValueError("timestamp must be an integer or long!")

        timestamp = float(timestamp)

        self.remove_lock.acquire()
        self.__test_and_add("lww_remove_set", element, timestamp)
        self.remove_lock.release()        

    def exist(self, element):
        """Check if the element exists in lww-set 

        """
        add_timestamp = self.redis.zscore("lww_add_set", element)
        remove_timestamp = self.redis.zscore("lww_remove_set", element) 

        if add_timestamp == None:
            return False
        elif remove_timestamp == None:
            return True
        elif add_timestamp >= remove_timestamp:
            return True
        else:
            return False        
    
    def get(self):
        """Returns an array of all existing elements in lww-set 

        """
        result = []
        all_add_elements = self.redis.zrange("lww_add_set", 0, -1)
        for element in all_add_elements:
            if self.exist(element):
                result.append(element)
        return result

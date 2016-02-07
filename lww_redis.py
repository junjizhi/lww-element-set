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
        return_flag = True
        self.add_lock.acquire()
        try:
            self.__test_and_add("lww_add_set", element, timestamp)
        except:
            return_flag = False
        finally: 
            self.add_lock.release()
        
        return return_flag

    def __test_and_add(self, target_set, element, timestamp):
        """A supposedly private function to lww_redis. 

        A wrapper function to do test and add. 

        Keyword raises:
        redis.exceptions.ResponseError -- A response error that
        probably indicates that the element has been assigned to the
        wrong type of set and the underlying redis set may be corrupted and need
        to be repaired. 
        """
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
        return_flag = True
        self.remove_lock.acquire()
        try:
            self.__test_and_add("lww_remove_set", element, timestamp)
        except:
            return_flag = False
        finally: 
            self.remove_lock.release()
        
        return return_flag

    def exist(self, element):
        """Check if the element exists in lww-set 

        """
        try:
            add_timestamp = self.redis.zscore("lww_add_set", element)
            remove_timestamp = self.redis.zscore("lww_remove_set", element) 
        except:
            raise RuntimeError("An internal error occurs, e.g., disconnection from network. A retry may solve the problem. ")

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

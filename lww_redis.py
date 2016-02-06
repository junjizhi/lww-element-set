

class LWW_set:
    """A Last-Writer-Win element set based on redis ZSET. 

    lww-set stores the add/remove operations in a remote 
    redis server. 

    Keyword attributes:
    redis -- an opened connection with a redis server

    """
    def __init__(self, redis):
        self.redis = redis

    def add(self, element, timestamp):
        """Add an element to lww_set, or update the existing element timestamp

        """
        if not isinstance (timestamp, (int, long)):
            raise ValueError("timestamp must be an integer or long!")

        self.redis.zadd("lww_add_set", element, timestamp)

    def remove(self, element, timestamp):
        """Remove an element from lww_set 

        """
        if not isinstance (timestamp, (int, long)):
            raise ValueError("timestamp must be an integer or long!")

        self.redis.zadd("lww_remove_set", element, timestamp)        

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
        all_add_elements = self.zrange("lww_add_set", 0, -1)
        for element in all_add_elements:
            if self.exist(element):
                result.append(element)
        return result

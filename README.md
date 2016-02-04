# lww-element-set
An Python implementation of Last-Writer-Wins Element Set. 
## Design
lww-set consists of two separate sets: add_set and remove_set. Each set records entries of (element, timestamp). When inserting an element to add_set or remove_set, create a new entry if the element does not exist. Otherwise, update the corresponding entry's timestamp if input is more recent (i.e., the passed timestamp is larger).
### Operations
The lww-set provides the following operations:
- add(element, timestamp): Attempt to add an element associated with its  timestamp in the set.
- remove(element, timestamp): Attempt to remove an element associated with its  timestamp in the set.
- exist(element): check if the element exists. The criteria is whether the element's most recent operation was an add.  
- get(): return a list of existing elements in lww-set

In order to satisfy the CRDT properties, i.e., Associativity, Commutativity and Idempotence, lww-set defines the following combinations of operations and their resulting states. 

Original state    Operation    Resulting state    Lww-set State changed    Note
A(a,1) R()    add(a,0)    A(a,1) R()    N    add out-of-date element because more recent add exists
A(a,1) R()    add(a,1)    A(a,1) R()    N    add success
A(a,1) R()    add(a,2)    A(a,2) R()    Y    add success
A() R(a,1)    add(a,0)    A(a,0) R(a,1)    Y    add out-of-date element because more recent remove exists
A() R(a,1)    add(a,1)    A(a,1) R(a,1)    Y    add success (we bias add)
A() R(a,1)    add(a,2)    A(a,2) R(a,1)    Y    add success
A() R(a,1)    remove(a,0)    A() R(a,1)    N    remove operation out of date because more recent remove exists
A() R(a,1)    remove(a,1)    A() R(a,1)    N    remove operation out of date because more recent remove exists
A() R(a,1)    remove(a,2)    A() R(a,2)    Y    remove success
A(a,1) R()    remove(a,0)    A(a,1) R(a,0)    Y    remove operation out of date because more recent add exists
A(a,1) R()    remove(a,1)    A(a,1) R(a,1)    Y    remove operation out of date because more recent add exists(we bias add)
A(a,1) R()    remove(a,2)    A(a,1) R(a,2)    Y    remove success

Note: The above table is different from the one in [Roshi](https://github.com/soundcloud/roshi) which does instant gargage collection when inserting a new element. This makes sure lww-set meets strictly the **Commutativity** property, i.e., a+b = b+a, the order of applying operations does not matter. However, because there is no garbage collection, there can be redundant copies of elements in both add_set and remove_sets, which wastes space. 

### Return values of add/remove operations
What value should lww-set remove operation return? It can result in a weird semantic. For example, when add set and remove set are both empty, i.e., A() R(), we perform Remove(a,1) operation on the lww-set. From an external view, we are deleting a non-existing element in lww-set, so it should return False in this semantic. But what actually happens is remove set will record an R operation and the internal result is changed to: A() R(a,1). So it indeed **changes** the state of lww-set and it should return True.

If the return value is based on the usual set add/remove semantic, then it may confuses users because some other processes calling the same method concurrently may have overwritten the element (with a more recent timestamp). 

If the return value is based on whether lww-set internal state has been changed, then we probably should we enumerate all return values for all possible scenarios(the table above). However, exposing the internal states of lww-set violates the encapsulation. 

The solution here is **add/remove methods always return None**. The caller of these methods does not know whether the operation succeeds or not based on the return value. The way to get a timely update is via calling get() or exist() method. 

## Synchronization Assumptions
lww-set is implemented with Python dictionaries. Since Python's GIL guarantees that only one thread runs at a time, dictionary operations, for example, D[x] = y, are [atomic and thread-safe](http://effbot.org/pyfaq/what-kinds-of-global-value-mutation-are-thread-safe.htm). 
## Redis extension
Besides the usual Python implementation, we also implement a version of lww-set based on Redis ZSET data structure. 

The expected usage scenario is like this: Each Redis replica (including the master and slaves) maintains a copy of this lww-set structure. Each (element, timestamp) update is sent through network to each replica. **The assumption is that the update requests may be delayed but will eventually arrive at each replica.** 

However, there could be a short period when the lww-set in each replica have different states, which causes inconsistency. But since requests eventually arrive, and the arrival order does not matter, eventually all replicas' lww-set will converge and be consistency. And there is no need to explicitly resolve conflicts. 
# Name: Robin Shindelman
# OSU Email: shindelr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/9/2023
# Description: This is an implementation of a hash map using open addressing
# collision resolution. The probing method is quadratic. This program requires
# the use of the file a6_include.py as the underlying structure of the hash
# table uses a dynamic array.


from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Add a new element to the hash map. Uses open addressing collision
        resolution with quadratic probing: Quadratic probing:
        hash_index = ( i_initial + j^2) % m (where, j = 1, 2, 3, …)
        i_initial is the first value returned by the hash function.
        j is a counter.
        m is the hash's capacity.
        key: The key to be inserted into the hash table.
        value: The corresponding value that the key refers to.
        returns: None
        """
        # First, handle load case:
        if self.table_load() > .5:
            self.resize_table(self._capacity * 2)

        initial_i = self._hash_function(key) % self._capacity
        hash_i = initial_i  # To start
        # If initial index is empty or has tombstone, just put 'er there.
        if self._buckets[hash_i] is None or \
                self._buckets[hash_i].is_tombstone is True:
            self._buckets[hash_i] = HashEntry(key, value)
            self._size += 1
            return

        # Handle duplicates.
        if self._buckets[hash_i].key == key:
            self._buckets[hash_i] = HashEntry(key, value)
            return

        # Otherwise, begin probing:
        j = 1
        while self._buckets[hash_i] is not None:
            # Duplicate check while probing
            if self._buckets[hash_i].key == key:
                self._buckets[hash_i] = HashEntry(key, value)
                return
            # Recalculate hash_index and probe:
            hash_i = (initial_i + j ** 2) % self._capacity  # Quadratic probe
            if self._buckets[hash_i] is None \
                    or self._buckets[hash_i].is_tombstone is True:
                self._buckets[hash_i] = HashEntry(key, value)
                self._size += 1
                return
            else:  # Continue forward.
                j += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the hash table to a new prime number. Rehashes
        all existing entries based on the new capacity.
        new_capacity: The new prime number to set capacity to. Must be > 1.
        returns: None
        """
        if new_capacity < self._size:
            return None

        if not self._is_prime(new_capacity):  # Check new cap for primeness.
            new_capacity = self._next_prime(new_capacity)

        # New, doubled or more table
        hash_table = HashMap(new_capacity, self._hash_function)

        # Rehash all hash links to new table.
        for i in range(self._capacity):
            if self._buckets[i] is not None and \
                    self._buckets[i].is_tombstone is False:
                hash_table.put(self._buckets[i].key, self._buckets[i].value)
        # Update data members
        self._buckets = hash_table._buckets
        self._capacity = hash_table._capacity
        self._size = hash_table._size

    def table_load(self) -> float:
        """
        Calculate the load factor on the given hash table. This is the number
        of elements in the table divided by the number of buckets available.
        """
        return self._size / self._buckets.length()  # Number of elems / buckets

    def empty_buckets(self) -> int:
        """
        Find the total number of empty buckets present in the hash table.
        returns: Int representing sum of all empty buckets
        """
        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Get the value associated with the argued key.
        key: The key desired.
        returns: HashEntry obj.value if key exists, None otherwise.
        """
        initial_i = self._hash_function(key) % self._capacity
        hash_i = initial_i
        j = 1
        # Check first index first, of course
        if self._buckets[initial_i] is not None and \
                self._buckets[initial_i].key == key and \
                self._buckets[initial_i].is_tombstone is False:
            return self._buckets[initial_i].value

        # Start probing
        while self._buckets[hash_i] is not None:
            hash_i = (initial_i + j ** 2) % self._capacity  # Quadratic probe
            if self._buckets[hash_i] is not None and \
                    self._buckets[hash_i].key == key and \
                    self._buckets[hash_i].is_tombstone is False:
                # Must make sure the tombstone is not True, that key would be ded.
                return self._buckets[hash_i].value
            else:
                j += 1
        return None  # Must've hit the end.

    def contains_key(self, key: str) -> bool:
        """
        Find out whether the argued key exists within this hash table.
        key: A key to a node in one of the chains (possibly)
        returns: True for success, False otherwise
        """
        if self.get(key) is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Remove the requested key and its value from the bucket it resides in.
        key: The key to be searched for and turned into a tombstone zombie.
        return: None
        """
        initial_i = self._hash_function(key) % self._capacity
        hash_i = initial_i
        j = 1
        # Check first index first, of course
        if self._buckets[initial_i] is not None and \
                self._buckets[initial_i].key == key and \
                self._buckets[initial_i].is_tombstone is False:
            self._buckets[initial_i].is_tombstone = True
            self._size -= 1
            return

        # Start probing
        while self._buckets[hash_i] is not None:
            hash_i = (initial_i + j ** 2) % self._capacity  # Quadratic probe
            if self._buckets[hash_i] is not None and \
                    self._buckets[hash_i].key == key and \
                    self._buckets[hash_i].is_tombstone is False:
                # Must make sure the tombstone is not True, that key would be ded.
                self._buckets[hash_i].is_tombstone = True
                self._size -= 1
                return
            else:
                j += 1
        return None  # Must've hit the end.

    def get_keys_and_values(self) -> DynamicArray:
        """
        Create an array populated by tuples of all the key:value pairs stored
        in the hash table.
        returns: DA
        """
        key_val_array = DynamicArray()
        for i in range(self._capacity):
            if self._buckets[i] is not None and \
                    self._buckets[i].is_tombstone is False:
                key_val_tup = self._buckets[i].key, self._buckets[i].value
                key_val_array.append(key_val_tup)
        return key_val_array

    def clear(self) -> None:
        """
        Empty the whole hash map. Will reduce size to zero but will not affect
        the capacity of the map.
        return: None
        """
        hash_map = HashMap(self._capacity, self._hash_function)
        self._buckets = hash_map._buckets
        self._capacity = hash_map._capacity
        self._size = hash_map._size
        self._hash_function = hash_map._hash_function

    def __iter__(self):
        """
        Create an iterator to traverse across the hash map.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Retrieve the next element in the hash map.
        """
        while self._index < self._capacity:
            if self._buckets[self._index] is not None and\
                    self._buckets[self._index].is_tombstone is False:
                item = self._buckets[self._index]
                self._index += 1
                return item
            else:
                self._index += 1
        raise StopIteration

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
                  m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
                  m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'),
          m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'),
          m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(),
              round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())
    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

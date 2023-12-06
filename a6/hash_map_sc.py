# Name: Robin Shindelman
# OSU Email: shindelr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/07/2023
# Description: This is an implementation of a Separate Chaining Hash Table.
# SC Hash Tables use a linked list to keep track of elements that are deemed
# the "same" by a given hash function. The hash function's result corresponds
# to a particular indice in the hash table, if two elements can be put in the
# same index, the hash table starts a linked list and attaches all elements
# that fit there as nodes.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int = 11, function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Add an element to the hash table. First, the element's spot in the
        hash table is computed using a hash function, then, the element is
        inserted into the associated chain.
        key: The identifiable piece of a linked list node
        value: The information stored at that key.
        returns: None
        """
        # Check load factor:
        if self.table_load() >= 1:
            # Resize based on the current capacity to the next prime number.
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)  # Hash table key
        index = hash % self._capacity
        chain = self._buckets[index]  # Chain @ DA index

        if self.contains_key(key):  # Handle duplicate
            for elem in chain:
                if elem.key == key:
                    elem.value = value
            return

        chain.insert(key, value)  # Add new node at that chain
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the hash table to a new prime number. Rehashes
        all existing entries based on the new capacity.
        new_capacity: The new prime number to set capacity to. Must be > 1.
        returns: None
        """
        if new_capacity < 1:
            return None

        if not self._is_prime(new_capacity):  # Check new cap for primeness.
            new_capacity = self._next_prime(new_capacity)

        # Downsizing branch
        # TODO: Get this darn thing to work
        if new_capacity <= self._size:
            new_capacity = 0
            while new_capacity <= self._size:
                new_capacity = self._next_prime(new_capacity*2)

        hash_table = HashMap(new_capacity)  # New, doubled or more table
        hash_table._hash_function = self._hash_function
        for i in range(self._capacity):
            if self._buckets[i].length() != 0:
                for elem in self._buckets[i]:
                    hash_table.put(elem.key, elem.value)

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
        empty_buckets = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                empty_buckets += 1
        return empty_buckets

    def get(self, key: str):
        """
        Get the value associated with the argued key.
        key: The key desired.
        returns: node.value if key exists, None otherwise.
        """
        hash = self._hash_function(key)  # Hash table key
        index = hash % self._capacity
        chain = self._buckets[index]  # Chain @ DA index
        if chain.length() is None:
            return None
        for elem in chain:  # Iterate over chain itself.
            if elem.key == key:
                return elem.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Find out whether the argued key exists within this hash table.
        key: A key to a node in one of the chains (possibly)
        returns: True for success, False otherwise
        """
        hash = self._hash_function(key)  # Hash table key
        index = hash % self._capacity
        chain = self._buckets[index]  # Chain @ DA index
        if chain.length() is None:
            return False
        for elem in chain:  # Still have to iterate over the chain itself.
            if key == elem.key:
                return True
        return False  # Otherwise, key not in chain

    def remove(self, key: str) -> None:
        """
        Remove the requested key and its value from the bucket it resides in.
        key: The key to be searched and destroyyed
        return: None
        """
        if not self.contains_key(key):
            return

        hash = self._hash_function(key)  # Hash table key
        index = hash % self._capacity
        chain = self._buckets[index]  # Chain @ DA index
        for elem in chain:
            if elem.key == key:
                chain.remove(key)
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Create an array populated by tuples of all the key:value pairs stored
        in the hash table.
        returns: DA
        """
        key_val_array = DynamicArray()
        for i in range(self._capacity):  # Must check all buckets?
            if self._buckets[i].length() != 0:  # If bucket not empty
                for elem in self._buckets[i]:  # Iterate through chain
                    key_val = elem.key, elem.value
                    key_val_array.append(key_val)
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


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Find the mode(s) of the argued dynamic array. If there is more than one
    mode, each mode value will be reported as well as the frequency with which
    they all appear.
    da: A DA object with one or more values.
    returns: Tuple([mode values,...,], frequency)
    """
    map = HashMap()
    max = 1  # Keep track of max occurrence

    # Generate a hash map where the key is the element and the value is the
    # number of times that the element has appeared in da.
    for i in range(da.length()):  # Iterate through da to generate hash map.
        if map.contains_key(da[i]):
            count = map.get(da[i])
            # This hash doesn't like dupes, so update count by 1.
            map.put(da[i], count + 1)
            if count + 1 >= max:  # Find new maximum as you go.
                max = count + 1
        else:
            map.put(da[i], 1)

    # With key:val pairs, if the val is equal to max, then it is one of the
    # modes. Append it to mode_arr.
    count_arr = map.get_keys_and_values()
    mode_arr = DynamicArray()
    for i in range(count_arr.length()):
        if count_arr[i][1] == max:
            mode_arr.append(count_arr[i][0])

    return mode_arr, max

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    """
    print("--------- Self Testing ---------------")

    print("--------- End Self Testing ------------")

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2),
                  m.get_size(), m.get_capacity())
        

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2),
                  m.get_size(), m.get_capacity())
    """
    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    m.resize_table(2)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)



        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    """
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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
    """



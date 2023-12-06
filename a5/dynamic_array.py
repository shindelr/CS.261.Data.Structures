# Name: Robin Shindelman
# OSU Email: shindelr@oregonstate.ed
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 10/30/2023
# Description: This file contains an implementation of a dynamic array. The
# code is built using a static array as the underlying data storage array, so
# the import of StaticArray.py is necessary for its functioning. DynamicArray
# will have a lot of the same functionality as other dynamic arrays you
# may find out in the world, such as Python's list. I.e., slice, append,
# remove, merge.


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------
    # -----------------------Robin's Little Helpers -------------------------
    def resize_checker(self) -> None:
        """
        Checks if the array size is equal to the capacity. If so, it calls
        resize(). Currently only implemented for append() and insert.
        """
        if self._size == self._capacity:
            self.resize(self._capacity*2)

    def insert_index_checker(self, index: int) -> None:
        """
        Check for a valid index. Currently only implemented for insert.
        Good for [0,N]
        index: The requested index.
        """
        # Handle the invalid index request
        if index < 0 or index >= self._size + 1:
            raise DynamicArrayException

    def remove_index_checker(self, index: int) -> None:
        """
        Check for a valid index. Implemented for remove, slice.
        Good for [0, N-1]
        index: Requested index
        """
        if index < 0 or index > self._size - 1:
            raise DynamicArrayException

    # -----------------------Assigned Methods---------------------------------
    def resize(self, new_capacity: int) -> None:
        """
        Resize the *capacity* of the dynamic array. If the desired new capacity
        is less than or equal to the current *size* of the array, no work will
        be done. Internal.
        new_capacity: A positive integer greater than self._size
        returns: None
        """
        # Base Cases
        if new_capacity <= 0:
            return None
        if new_capacity < self._size:
            return None

        resized_arr = StaticArray(new_capacity)
        # Copy over all the data to the new array.
        for i in range(self._size):
            resized_arr[i] = self._data[i]
        # Update ._data and ._capacity to match the new array.
        self._data = resized_arr
        self._capacity = resized_arr.length()

    def append(self, value: object) -> None:
        """
        Add a new value to the end of the array. If the array is at capacity,
        this method will automatically resize() the array to accommodate the
        new value(s).
        value: Item being appended.
        returns: None
        """
        self.resize_checker()  # Resize necessary for this operation?

        index = 0
        while value is not None:
            if self._data[index] is None:  # Add val to first empty spot.
                self._data[index] = value
                value = None  # Flip the loop condition to False.
                self._size += 1
            index += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Add a new value to the array at the given index. If the array is at
        capacity, this method will resize().
        index: Place in array to insert, must be a valid, positive integer.
        value: Item being added.
        returns: None
        """
        # Handle the invalid index request
        self.insert_index_checker(index)
        self.resize_checker()  # Resize? iff index is valid

        # If the desired index is the end, just call append and exit
        if index == self._size:
            self.append(value)
            return

        # Shift all the values to the right by one.
        for i in range(self._capacity-1, index-1, -1):
            if self._data[i] is not None:
                self._data[i+1] = self._data[i]
            # Reach the appropriate index at the bottom of the loop.
            if i == index:
                self._data[i] = value
                self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        Remove whatever value currently resides at the requested index. Shift
        all values to fill the hole, remaining contiguous.
        index: Valid indices are positive and within the array size.
        """
        # Handle the invalid index request
        self.remove_index_checker(index)

        # Handle resize: capacity must be 10 or greater & 4 times the size.
        if self._capacity > self._size * 4 and self._capacity > 10:
            if self._size * 2 > 10:
                # Resize to double the _size if it'll be greater than 10.
                self.resize(self._size*2)
            else:
                self.resize(10)

        # Removal
        for i in range(index, self._size):
            # Splice out the value being removed
            if i == index:
                # Edge case
                if i+1 >= self._capacity:
                    self._data[i] = None
                else:
                    self._data[i] = self._data[i+1]
                self._size -= 1
            # End the loop by tagging on a None.
            elif i == self._size:
                self._data[i] = None
            # Otherwise, shift everything over one.
            else:
                self._data[i] = self._data[i + 1]

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Create a new dynamic array holding only the elements between the
        specified indices.
        start_index: First value in the new array.
        size: The number of elements to be included in the new array.
        returns: A new DyanamicArray containing only the elements specified.
        """
        # Handle invalid indices
        self.remove_index_checker(start_index)
        if size < 0 or (size + start_index) > self._size:
            raise DynamicArrayException
        # Initialize new empty Dyno array
        slice_arr = DynamicArray()

        # Append all the desired values.
        for i in range(start_index, size+start_index):
            slice_arr.append(self._data[i])
        return slice_arr

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Append all the items in the given array onto the end of the current
        array.
        second_da: Dynamic array.
        returns: None.
        """
        for i in range(second_da.length()):
            self.append(second_da[i])

    def map(self, map_func) -> "DynamicArray":
        """
        Compute a new array of equal length to the current array. All values
        are passed through a function which may or may not change them, such
        as y=x^2, where all old values are 'x' and the new values are 'y'.
        map_func: Callable function to pass values through.
        returns: New Dynamo array containing computed values.
        """
        # Initialize return array.
        map_arr = DynamicArray()

        # Pass every element in self._data through the map function,
        # Then append those values onto the return array.
        for i in range(self._size):
            mapped_val = map_func(self._data[i])
            map_arr.append(mapped_val)
        return map_arr

    def filter(self, filter_func) -> "DynamicArray":
        """
        Create a new array populated only by values that passed the "filter
        test" with a True bool.
        filter_func: Callable function which returns a boolean.
        returns: New DyanmicArray containing filtered values.
        """
        # Initialize return array.
        filter_array = DynamicArray()

        # Call the given filter function to 'filter' out unwanted data values.
        for i in range(self._size):
            bool = filter_func(self._data[i])
            if bool is True:
                filter_array.append(self._data[i])

        return filter_array

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Pass all values in the current array through the reduce function.
        reduce_func: A callable function that will result in an integer.
        initializer: Default to None, if set, becomes the first value used
                    in the reduce_func.
        returns: Array reduced to a single item.
        """
        # Base cases for empty array. If initializer is present, return that.
        if self._size == 0 and initializer is None:
            return None
        elif self._size == 0:
            return initializer

        reduce_var = None
        if initializer is None:
            if self._size == 1:
                return self._data[0]
            for i in range(self._size-1):
                if reduce_var is None:
                    # First step, use the first value in array.
                    reduce_var = reduce_func(self._data[i], self._data[i+1])
                else:
                    # Every other step, use reduce_var.
                    reduce_var = reduce_func(reduce_var, self._data[i+1])
            return reduce_var

        for i in range(self._size):
            if reduce_var is None:
                # First step, use the initializer
                reduce_var = reduce_func(initializer, self._data[i])
            else:
                # Every other step use reduce var.
                reduce_var = reduce_func(reduce_var, self._data[i])
        return reduce_var

    def pop(self):
        """
        Remove and return the last value in the DA.
        returns: The value stored in the last index
        """
        return self._data[self.length()-1]

# -------------------------- End DynamicArray --------------------------------
def mode_counter(arr):
    """
    Count how often the mode(s) occur in the given array. Used to give the
    function find_mode() a count to compare its values to.
    arr: Dynamic or Static array to be counted.
    Returns: elem_count, the number of times the mode occurred.
    """
    arr_size = arr.length()
    # First two the same?
    if arr[0] == arr[1]:
        curr_elem, elem_count = arr[0], 2
        next_elem, next_elem_count = 0, 0
    else:
        curr_elem, elem_count = arr[0], 1
        next_elem, next_elem_count = arr[1], 1

    index = 1
    while index != arr_size - 1:
        third_elem = arr[index + 1]
        if third_elem == curr_elem:
            elem_count += 1
        if third_elem == next_elem:
            next_elem_count += 1

        # If next is not next-next, reset the next counter.
        if elem_count >= next_elem_count and third_elem != next_elem:
            next_elem, next_elem_count = third_elem, 1
        # Otherwise don't reset next_counter, just move it forward.
        elif elem_count >= next_elem_count:
            next_elem = third_elem
        # Or do the swap if next_counter is greater.
        else:
            curr_elem, elem_count = next_elem, next_elem_count
            next_elem, next_elem_count = third_elem, 1
        index += 1
    return elem_count


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Find the most oft occurring elements in the array.
    arr: A dynamic array in sorted order.
    returns: tuple(array:most occurring items, int of how many occurrences)
    """
    mode_array = DynamicArray()
    # Base case of array length one.
    if arr.length() == 1:
        return arr, 1
    # Call mode counter, how many times does the mode occur?
    elem_count = mode_counter(arr)

    current = 1
    for i in range(arr.length()):
        # Handle reaching the end of the list.
        if i + 1 == arr.length():
            if current >= elem_count:
                mode_array.append(arr[i])
        # Handle the edge of the value's territory in arr
        elif arr[i] != arr[i+1]:
            if current >= elem_count:
                mode_array.append(arr[i])
                current = 1
            # Reset the count if current is not >= to elem_count
            else:
                current = 1
        # Tabulate occurrences of individual values
        else:
            current += 1

    return mode_array, elem_count


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 'apple'])
    assert da.pop() == 'apple'



    """
    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    # DYN_ARR Size/Cap: 8/32 [10, 11, 12, 13, 14, 15, 16, 1024] Remove index 0
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16, 1024])
    da._capacity = 32
    da.remove_at_index(0)

    # DYN_ARR Size/Cap: 4/4 [xPSMNfy, \k\O, qCYYL, \DnODS] Remove index 3
    da = DynamicArray(['xPSMNfy', '\k\O', 'qCYYL', '\DnODS'])
    da.remove_at_index(3)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print(da.slice(2, 3))


    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
    """
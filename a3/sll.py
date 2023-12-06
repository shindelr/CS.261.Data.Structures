# Name: Robin Shindelman
# OSU Email: shindelr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 11/6/2023
# Description: This program implements a singly linked list data structure.
# The SLL is a linear structure based where values are stored in individual
# 'nodes', each node forms a link in the SLL chain, pointing to the next node.


from SLNode import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initialize new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        Insert a new node at the front of the SLL, just behind the front
        sentinel.
        value: Node object being passed.
        returns: None
        """
        new_node = SLNode(value)
        if self._head.next is not None:
            temp = self._head.next  # Don't break the chain, save the next val.
            new_node.next = temp
            self._head.next = new_node
        else:
            self._head.next = SLNode(value)

    def insert_back(self, value: object) -> None:
        """
        Attach a new node to the end of the SLL.
        value: A node object.
        returns: None
        """
        node = self._head
        last_node = None
        # Iterate through the SLL until the new node finds a spot.
        while last_node is None:
            if node.next is None:
                last_node = SLNode(value)  # Could refactor this section.
                node.next = last_node
            else:
                node = node.next  # Go next until we hit the end.

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Place a new node at the desired spot. Node immediately after front
        sentinel node represents index 0. Valid indices are [0, N].
        index: Integer between [0, N]
        value: Node object
        returns: None
        """
        # Index validation
        if self.length() < index or index < 0:
            raise SLLException

        # Base case of insert @ front.
        node = self._head.next
        if index == 0:
            self.insert_front(value)

        n = 0  # n represents the number of values in the SLL
        while n != index:
            if n == index-1:
                new_node = SLNode(value)  # Don't break the chain
                temp = node.next
                node.next = new_node
                new_node.next = temp
                n += 1
            else:
                node = node.next  # Increment forward.
                n += 1

    def remove_at_index(self, index: int) -> None:
        """
        Remove the value at a given index. 0 indicates the first index and the
        value immediately after the front sentinel. Valid indices [0, N-1]
        index: Positive integer.
        returns: None
        """
        # Index validation
        if self.length()-1 < index or index < 0:
            raise SLLException
        # If index at beginning of SLL reassign head next field.
        if index == 0:
            self._head.next = self._head.next.next
            return

        n = 1
        curr = self._head.next.next
        prev = self._head.next
        while n != index:
            # Traverse two pointers
            prev = curr
            curr = curr.next
            n += 1
        # Reassign prev next to equal the value past current.
        prev.next = curr.next

    def remove(self, value: object) -> bool:
        """
        Remove the first instance of the passed value from the SLL.
        value: Node object
        returns: True if obj removed, False otherwise.
        """
        n = 0
        curr = self._head
        prev = curr
        while n <= self.length():
            if curr.value == value:
                prev.next = curr.next
                # Splice out the unwanted value
                return True
            else:
                # Continuing incrementing forward
                prev = curr
                curr = curr.next
                n += 1
        return False

    def count(self, value: object) -> int:
        """
        Count the number of elements in the SLL that match the argued value.
        value: Node object
        returns: Integer representing the number of instances of a value.
        """
        node = self._head.next
        counter = 0
        while node is not None:
            if node.value == value:
                counter += 1
            node = node.next
        return counter

    def find(self, value: object) -> bool:
        """
        Determine if the given value exists in the SLL.
        value: Node object
        returns: True if value is in SLL, False otherwise
        """
        node = self._head.next
        while node is not None:
            if node.value == value:
                return True
            node = node.next
        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        Create a new linked list only containing the nodes between the starting
        index and however many indices forward are indicated by the size arg.
        start_index: The beginning index of the slice
        size: How many indices will be included in the slice
        returns: New linked list
        """
        # Index validation & size validation too
        if self.length() < size or start_index < 0 or size <0:
            raise SLLException
        if start_index + size > self.length():
            raise SLLException
        if start_index == self.length():
            raise SLLException

        # Initialize new linked list
        slice_list = LinkedList()

        # Set the node of the original list to the correct index.
        og_node = self._head
        slice_node = slice_list._head
        n = 0
        while n < start_index:
            og_node = og_node.next
            n += 1
        # Copy over all the values between start_index and size.
        n = 0
        while n < size:
            slice_node.next = SLNode(og_node.next.value)
            slice_node = slice_node.next
            og_node = og_node.next
            n += 1

        return slice_list

if __name__ == "__main__":

    print("\n# insert_front example 1")
    test_case = ["A", "B", "C"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_front(case)
        print(lst)


    print("\n# insert_back example 1")
    test_case = ["C", "B", "A"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_back(case)
        print(lst)

    print("\n# insert_at_index example 1")
    lst = LinkedList()
    test_cases = [(-1, "E"), (0, "A"), (0, "B"), (1, "C"), (3, "D"), (5, "F")]
    for index, value in test_cases:
        print("Inserted", value, "at index", index, ": ", end="")
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove_at_index example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6])
    print(f"Initial LinkedList : {lst}")
    for index in [0, 2, 0, 2, 2, -2]:
        print("Removed at index", index, ": ", end="")
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [7, 3, 3, 3, 3]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# remove example 2")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [1, 2, 3, 1, 2, 3, 3, 2, 1]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# count example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print("\n# find example 1")
    lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Claus"])
    print(lst)
    print(lst.find("Waldo"))
    print(lst.find("Superman"))
    print(lst.find("Santa Claus"))

    print("\n# slice example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print("Source:", lst)
    print("Start: 1 Size: 3 :", ll_slice)
    ll_slice.remove_at_index(0)
    print("Removed at index 0 :", ll_slice)

    print("\n# slice example 2")
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("Source:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Start:", index, "Size:", size, end="")
        try:
            print(" :", lst.slice(index, size))
        except:
            print(" : exception occurred.")

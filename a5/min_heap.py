# Name: Robin Shindelman
# OSU Email: shindelr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 5
# Due Date: 11/29/2023
# Description: This is an implementation of a minimum heap data structure.
# The min-heap stores the smallest value of an array as its root value. Then,
# there are subsequently larger values stored in the order that a complete
# binary tree would take. Note: There is heapsort() stored in this little
# module, heapsort() is a subquadratic sort function!


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)

    def index_validation(self, index):
        """
        Check for appropriate index input. Cannot be larger or smaller than
        the length of the underlying dynamic array. Raises an exception if
        invalid.
        index: Index to be evaluated
        """
        if index > self._heap.length() -1 or index < 0:
            raise MinHeapException
        else:
            return True

    def parent(self, index):
        """
        Calculate the index of the parent node to the argument node.
        index: Refers to the index of the child.
        returns: The index of the argued node's parent.
        """
        #self.index_validation(index)
        return (index - 1) // 2

    def left(self, index):
        """
        Calculate the index of a parent node's left child.
        index: Refers to the index of the current node.
        returns: The index of the left child.
        """
        #self.index_validation(index)
        return (2 * index) + 1

    def right(self, index):
        """
        Calculate the index of a parent node's right child.
        index: Refers to the index of the current node.
        returns: The index of the right child.
        """
        #self.index_validation(index)
        return (2 * index) + 2

    def add(self, node: object) -> None:
        """
        Add an item to the heap. Adds it to the first open space, then
        percolates upwards until the heap configuration is correct.
        node: Object to be added to the heap.
        returns: None
        """
        # Empty heap
        if self._heap.length() == 0:
            self._heap.append(node)
            return

        last_added = self._heap.length() - 1  # Actual index
        first_open = self._heap.length()  # Actual Index

        # Add value to First Available spot
        self._heap.insert_at_index(first_open, node)
        # Update pointers
        last_added = first_open  # Switch last added to the index where the last element was added
        first_open = self._heap.length()  # Index

        # Initialize percolation pointers
        parent_index = self.parent(last_added)  # Index of last_added parent
        node_index = last_added

        # Percolations:
        while parent_index >= 0:  # While we're in a valid index
            parent_val = self._heap[parent_index]
            if node < parent_val and node_index > parent_index:  # If the new val is greater, swap them.
                self._heap[parent_index] = node  # Put new val at parent spot
                self._heap[node_index] = parent_val  # Put parent at val old spot
                node_index = parent_index  # Update Node index pointer
                parent_index = self.parent(node_index)  # Update parent index
            else:
                return  # Base case? If you make it here, then the if statement above was false and percolations should end.

    def is_empty(self) -> bool:
        """
        Check if the heap is empty or not.
        returns: True if empty, False otherwise
        """
        # Convoluted I know, but I thought i'd experiment a bit
        error = 0
        try:
            self._heap[0]
        except:
            DynamicArrayException
            error = 1  # Any advice on how to do this better?
            # My idea is that I'm setting an 'error flag'.

        if error == 1:  # Error flag set
            return True  # Is empty!
        return False  # Error flag clear, there must be a list

    def get_min(self) -> object:
        """
        Reveal the minimum value of the min heap. This corresponds to the 0th
        index in the array.
        returns: Lowest value
        """
        self.index_validation(0)
        return self._heap[0]

    def remove_min(self) -> object:
        """
        Remove the minimum value from the minheap.
        When percolating downwards, the swaps favor the left child.
        returns: Minimum value
        """
        if self._heap.is_empty():
            raise MinHeapException

        min_val = self._heap[0]  # To return later
        if self._heap.length() == 1:  # If there is only one val in the heap.
            self._heap.remove_at_index(0)
            return min_val

        # Replace the first elem with the last, since we're removing the first
        self._heap[0] = self._heap[self._heap.length()-1]
        self._heap.remove_at_index(self._heap.length()-1)

        # Initialize percolation variables
        node_val = self._heap[0]  # New root
        node_index = 0
        left_c_i = self.left(node_index)  # Index of root's left child
        right_c_i = self.right(node_index)  # Index of root's right child

        while left_c_i < self._heap.length() or \
                right_c_i < self._heap.length():  # As long as there is child cont.

            # Find min child, if two childs compare. If one, just take the one that exists.
            if left_c_i < self._heap.length() and \
                    right_c_i < self._heap.length():
                min_c = min(self._heap[left_c_i], self._heap[right_c_i])
            else:
                if left_c_i < self._heap.length(): min_c = self._heap[left_c_i]
                elif right_c_i < self._heap.length(): min_c = self._heap[right_c_i]

            # Switch code, redundant, could refactor.
            if node_val > min_c:  # If replacement larger, swap with min
                if self._heap[left_c_i] == min_c:  # If left child
                    self._heap[node_index] = self._heap[left_c_i]
                    self._heap[left_c_i] = node_val
                    node_index = left_c_i
                    left_c_i = self.left(node_index)  # Index of root's left child
                    right_c_i = self.right(node_index)  # Index of root's right child
                elif self._heap[right_c_i] == min_c:  # If right child
                    self._heap[node_index] = self._heap[right_c_i]
                    self._heap[right_c_i] = node_val
                    node_index = right_c_i
                    left_c_i = self.left(node_index)  # Index of root's left child
                    right_c_i = self.right(node_index)  # Index of root's right child
            else:
                return min_val
        return min_val

    def build_heap(self, da: DynamicArray) -> None:
        """
        Create a valid min heap from any given dynamic array. Takes each item,
        adds it, and percolates it. Overrides any existing minheap stored in
        the variable.
        da: The dynamic array object containing values to be added to the heap.
        returns: None
        """
        # Empty list out to make room for new heap
        if self._heap.is_empty() is False:
            self.clear()
        if da.is_empty():  # If DA is empty, return None
            return None

        for elem in range(da.length()):  # Copy over all new elems into heap
            self._heap.append(da[elem])
        if self._heap.length() == 1:  # Heap of one: Just return the heap
            return

        leaf_index = self.parent(self._heap.length()-1)  # Parent of largest index
        node_index = leaf_index

        left_c_i = self.left(node_index)  # Index of root's left child
        right_c_i = self.right(node_index)  # Index of root's right child

        while leaf_index >= 0:  # One loop keeps track of making sure we percolate, one keeps track of the list indice
            while left_c_i < self._heap.length() or \
                    right_c_i < self._heap.length():
                node_val = self._heap[node_index]
                # Find min child, if two childs compare. If one, just take the one that exists.
                if left_c_i < self._heap.length() and \
                        right_c_i < self._heap.length():
                    min_c = min(self._heap[left_c_i], self._heap[right_c_i])
                else:
                    if left_c_i < self._heap.length():
                        min_c = self._heap[left_c_i]
                    elif right_c_i < self._heap.length():
                        min_c = self._heap[right_c_i]

                # Switch code
                if node_val > min_c:  # If replacement larger, swap with min
                    if self._heap[left_c_i] == min_c:  # If left child
                        self._heap[node_index] = self._heap[left_c_i]
                        self._heap[left_c_i] = node_val
                        node_index = left_c_i
                        left_c_i = self.left(node_index)  # Index left child
                        right_c_i = self.right(node_index)  # Index right child
                    elif self._heap[right_c_i] == min_c:  # If right child
                        self._heap[node_index] = self._heap[right_c_i]
                        self._heap[right_c_i] = node_val
                        node_index = right_c_i
                        left_c_i = self.left(node_index)  # Index left child
                        right_c_i = self.right(node_index)  # Index right child
                else:
                    break  # Break because percolations are over.
            # If not, leaf is good, go to next leaf!
            leaf_index = leaf_index - 1  # Move index forwards
            node_index = leaf_index  # Make sure to override old node index
            left_c_i = self.left(leaf_index)  # Index left child
            right_c_i = self.right(leaf_index)  # Index right child
        return

    def size(self) -> int:
        """
        Return the number of items stored in the heap.
        returns: Int representing number of elements in the heap.
        """
        if self._heap.is_empty():
            return 0
        return self._heap.length()

    def clear(self) -> None:
        """
        Clear the heap. Permanently deletes all data in the heap!
        returns: None
        """
        if self._heap.is_empty():
            return None
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    Take an unsorted array and sort it using heap functions. This function is
    O(nlogn) which is special! It's not often you run into sub-quadratic sort
    functions. Note: This function will sort the array in place and only into
    non-ascending order.
    da: An unsorted dynamic array
    returns: None
    """
    # Base case 1 & 2:
    if da.length() == 1:
        return
    if da.length() == 2:
        l_max = max(da[0], da[1])
        if da[0] != l_max:  # If second num is max, swap the two elems.
            da[0], da[1] = da[1], da[0]

    da = heapsort_helper(da)  # Heapify da

    # Base case 3:  (helps to have been heapified)
    if da.length() == 3:
        da[0], da[2] = da[2], da[0]  # Swap min and last
        l_max = max(da[0], da[1])
        if da[0] != l_max:  # If middle num is max, swap the front two elems.
            da[0], da[1] = da[1], da[0]
        return

    # K keeps track of the boundary between heap and sorted array
    k = da.length() - 1  # K counter starts at the last index

    # Keep track of k moving towards front of heap
    while k > 1:
        # Initialize/update all pointers
        k_val = da[k]  # Reset k_val to last val in heap.
        node_val = da[0]  # Reset node_val to min
        node_index = 0  # Reset node_index to 0
        temp = k_val
        da[k] = da[node_index]  # Swap min and kth value.
        da[node_index] = temp
        k_val = node_val
        node_val = temp
        k -= 1  # Decrement k towards front of heap
        left_c_i = left(node_index)  # Index of root's left child
        right_c_i = right(node_index)  # Index of root's right child

        # Percolate the new root value to a good position
        while (left_c_i < k or right_c_i < k):
            # Find min child, if two childs compare.
            if left_c_i < k and right_c_i <= k:
                min_c = min(da[left_c_i], da[right_c_i])
            else: # If one, just take the one
                if left_c_i < k:
                    min_c = da[left_c_i]
                elif right_c_i < k:
                    min_c = da[right_c_i]

            # Switch code, redundant, could refactor.
            if node_val > min_c:  # If replacement larger, swap with min
                if da[left_c_i] == min_c:  # If left child
                    da[node_index] = da[left_c_i]
                    da[left_c_i] = node_val
                    node_index = left_c_i
                    left_c_i = left(node_index)  # Index of  new left child
                    right_c_i = right(node_index)  # Index of new right child
                elif da[right_c_i] == min_c:  # If right child
                    da[node_index] = da[right_c_i]
                    da[right_c_i] = node_val
                    node_index = right_c_i
                    left_c_i = left(node_index)  # Index of new left child
                    right_c_i = right(node_index)  # Index of new right child
            else:
                break  # Go to decrement k section.

    # Final check, since k indexing is a little funny:
    max_l = max(da[0], da[1])
    if da[0] != max_l:  # If the front value is not the maximum.
        da[0], da[1] = da[1], da[0]
    return

#-------------------------- Heapsort Helpers ------------------------------#
def heapsort_helper(da):
    """
    Build a minheap but dyanmo array style.
    da: a valid DynamicArray object.
    returns: da in minheap arrangement
    """
    leaf_index = parent(da.length() - 1)  # Parent of largest index
    node_index = leaf_index

    left_c_i = left(node_index)  # Index of root's left child
    right_c_i = right(node_index)  # Index of root's right child

    while leaf_index >= 0:  # One loop keeps track of making sure we percolate, one keeps track of the list indice
        while left_c_i < da.length() or \
                right_c_i < da.length():
            node_val = da[node_index]
            # Find min child, if two childs compare. If one, just take the one that exists.
            if left_c_i < da.length() and \
                    right_c_i < da.length():
                min_c = min(da[left_c_i], da[right_c_i])
            else:
                if left_c_i < da.length():
                    min_c = da[left_c_i]
                elif right_c_i < da.length():
                    min_c = da[right_c_i]

            # Switch code
            if node_val > min_c:  # If replacement larger, swap with min
                if da[left_c_i] == min_c:  # If left child
                    da[node_index] = da[left_c_i]
                    da[left_c_i] = node_val
                    node_index = left_c_i
                    left_c_i = left(node_index)  # Index left child
                    right_c_i = right(node_index)  # Index right child
                elif da[right_c_i] == min_c:  # If right child
                    da[node_index] = da[right_c_i]
                    da[right_c_i] = node_val
                    node_index = right_c_i
                    left_c_i = left(node_index)  # Index left child
                    right_c_i = right(node_index)  # Index right child
            else:
                break  # Break because percolations are over.
        # If not, leaf is good, go to next leaf!
        leaf_index = leaf_index - 1  # Move index forwards
        node_index = leaf_index  # Make sure to override old node index
        left_c_i = left(leaf_index)  # Index left child
        right_c_i = right(leaf_index)  # Index right child
    return da


def parent(index):
    """
    Calculate the index of the parent node to the argument node.
    index: Refers to the index of the child.
    returns: The index of the argued node's parent.
    """
    return (index - 1) // 2


def left(index):
    """
    Calculate the index of a parent node's left child.
    index: Refers to the index of the current node.
    returns: The index of the left child.
    """
    return (2 * index) + 1


def right(index):
    """
    Calculate the index of a parent node's right child.
    index: Refers to the index of the current node.
    returns: The index of the right child.
    """
    return (2 * index) + 2
# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':
    print(" --------- Self Testing ------------")
    h = MinHeap([-56811, -21342, -24704, 72807, 68212, 91641, 7412])
    h.add(-41756)
    print(h)

    print(" --------- End Self Section ------------")

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())
    
    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    da = heapsort_helper(da)
    print(h)
    print(da)

    print("\n Self Test build_heap()")
    print("--------------------------")
    da = DynamicArray([6919, 81194, -75478, -17255, -35467])
    h = MinHeap([-50278, -48819])
    print(f'Start heap: {h}')
    h.build_heap(da)
    da = heapsort_helper(da)
    print(f'heapsort_helper: {da}')
    print(f'End heap: {h}')
    print(f'Expected heap: [-75478, -35467, 6919, -17255, 81194]')

    print('\n')
    da = DynamicArray([
        -80331, -94505, 43618, -22221, -95367, -63524, -1495, 27123, 13477,
        24404
        ])
    h = MinHeap([-45209, 9272])
    print(f'Start heap: {h}')
    h.build_heap(da)
    da = heapsort_helper(da)
    print(f'heapsort_helper: {da}')
    print(f'End heap: {h}')
    print(f'Expected heap: [-95367, -94505, -63524, -22221, -80331, 43618, -1495, 27123, 13477, 24404]')

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nGS - Self testing")
    print("------------------------")
    da = DynamicArray([23292, 99767, 15832, -72550, -36913])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
    print(f'Expected: DYN_ARR Size/Cap: 5/8 [99767, 23292, 15832, -36913, -72550]')

    print("\nGS - Self testing")
    print("------------------------")
    da = DynamicArray([3, 1, 2])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
    print(f'Expected: DYN_ARR Size/Cap: 5/8 [3, 2, 1]')

    print("\nGS - Self testing")
    print("------------------------")
    da = DynamicArray([30862, 32814, 40875, 85864, -71729, 7347, -84074, 40152, -76294])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
    print(f'Expected: DYN_ARR Size/Cap: n/n [85864, 40875, 40152, 32814, 30862, 7347, -71729, -76294, -84074]')

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)



# Scratch Code for the mid term!

def dynArrayAddAt(self, index, value):
    """
    Add a new value to the array at the given index. If the array is at
    capacity, this method will also resize the array.
    """
    # Handle if the array is empty somehow
    if self.size == 0:
        raise DynamicArrayException
    # Handle the invalid index request
    if index < 0 or index >= self.size + 1:
        raise DynamicArrayException

    # Handle the possibility of a resize.
    if self.size == self.capacity:
        new_capacity = self.size * 2
        # New array, copy items over.
        resized_arr = DynamicArray(new_capacity)
        for i in range(self.size):
            resized_arr[i] = self.data[i]
        self.data = resized_arr
        self.capacity = resized_arr.size

    if index == self.size:
        self.append(value)
        return
    # Create a space for the data by shifting everything over one.
    for i in range(self.capacity - 1, index - 1, -1):
        if self.data[i] is not None:
            self.data[i + 1] = self.data[i]
        # At the end of the loop, you'll have found the insertion point.
        if i == index:
            self.data[i] = value
            self.size += 1

def remove_at_index(self, index: int) -> None:
    """
    Remove a node from the given index.
    """
    # Index valid?
    if self.length() - 1 < index or index < 0:
        raise SLLException
    # Remove first item?
    if index == 0:
        self._head.next = self._head.next.next
    # Find node to remove
    node = self._head.next.next
    prev = self._head.next
    i = 1
    while i != self.length():
        if i == index:
            prev.next = node.next
            i += 1
        else:
            prev = node
            node = node.next







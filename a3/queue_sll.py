# Name: Robin Shindelman
# OSU Email: shindelr@oregonstate.ed
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 11/6/2023
# Description: This is an implementation of a queue ADT (first in first out)
# with a Singly Linked List data structure.


from SLNode import SLNode


class QueueException(Exception):
    """
    Custom exception to be used by Queue class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Queue:
    def __init__(self):
        """
        Initialize new queue with head and tail nodes
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = None
        self._tail = None

    def __str__(self):
        """
        Return content of queue in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'QUEUE ['
        if not self.is_empty():
            node = self._head
            out = out + str(node.value)
            node = node.next
            while node:
                out = out + ' -> ' + str(node.value)
                node = node.next
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the queue is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._head is None

    def size(self) -> int:
        """
        Return number of elements currently in the queue
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        node = self._head
        length = 0
        while node:
            length += 1
            node = node.next
        return length

    # -----------------------------------------------------------------------

    def enqueue(self, value: object) -> None:
        """
        Add a node to the back of the queue.
        value: SLNode object's value
        Returns: None
        """
        # Initial case empty list, set up head and attach it to tail.
        if self._head is None:
            self._head, self._head.next = SLNode(value), self._tail
            return

        # If tail hasn't been assigned, create a new tail node.
        if self._head.next is None:
            self._tail = SLNode(value)
            # Attach head to tail
            self._head.next = self._tail
            return

        # The new node will be the tail.
        new_node = self._tail
        new_node.next = SLNode(value)
        # Reassign tail node to be the new node.
        self._tail = new_node.next

    def dequeue(self) -> object:
        """
        Remove the node at the front of the queue.
        Returns: SLNode object that was just removed.
        """
        # Empty list handling
        if self.is_empty():
            raise QueueException

        # Save value to be returned
        return_val = self._head.value
        # Remove 1st link go to next.
        self._head = self._head.next
        return return_val

    def front(self) -> object:
        """
        Peek at the first value in the linked list. Does not remove the value.
        returns: SLNode Object's value
        """
        if self.is_empty():
            raise QueueException
        return self._head.value

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# enqueue example 1")
    q = Queue()
    print(q)
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
        print(q)
    print(q)

    print("\n# dequeue example 1")
    q = Queue()
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)
    for i in range(6):
        try:
            print(q.dequeue())
        except Exception as e:
            print("No elements in queue", type(e))

    print('\n#front example 1')
    q = Queue()
    print(q)
    for value in ['A', 'B', 'C', 'D']:
        try:
            print(q.front())
        except Exception as e:
            print("No elements in queue", type(e))
        q.enqueue(value)
    print(q)

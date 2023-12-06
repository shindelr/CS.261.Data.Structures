# Name: Robin Shindelman
# OSU Email: shindelr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 11/06/23
# Description: This is an implementation of a Stack ADT (first in, last out)
#  using a singly linked list as the underlying data structure.



from SLNode import SLNode


class StackException(Exception):
    """
    Custom exception to be used by Stack class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Stack:
    def __init__(self) -> None:
        """
        Initialize new stack with head node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = None

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'STACK ['
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
        Return True is the stack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._head is None

    def size(self) -> int:
        """
        Return number of elements currently in the stack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        node = self._head
        length = 0
        while node:
            length += 1
            node = node.next
        return length

    # -----------------------------------------------------------------------

    def push(self, value: object) -> None:
        """
        Place a new item on top of the stack.
        value: SLNode object to be pushed.
        """
        if self.is_empty():
            self._head = SLNode(value)
            return

        new_node = SLNode(value)
        new_node.next = self._head
        self._head = new_node

    def pop(self) -> object:
        """
        Remove the topmost node on the stack and return whatever value it
        was holding.
        Returns: SLNode object value
        """
        if self.is_empty():
            raise StackException

        node_val = self._head.value
        self._head = self._head.next
        return node_val

    def top(self) -> object:
        """
        'Peek' at the value of the first node sitting on the stack.
        Returns: SLNode object value
        """
        if self.is_empty():
            raise StackException

        return self._head.value

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# push example 1")
    s = Stack()
    print(s)
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    print(s)

    print("\n# pop example 1")
    s = Stack()
    try:
        print(s.pop())
    except Exception as e:
        print("Exception:", type(e))
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    for i in range(6):
        try:
            print(s.pop())
        except Exception as e:
            print("Exception:", type(e))

    print("\n# top example 1")
    s = Stack()
    try:
        s.top()
    except Exception as e:
        print("No elements in stack", type(e))
    s.push(10)
    s.push(20)
    print(s)
    print(s.top())
    print(s.top())
    print(s)
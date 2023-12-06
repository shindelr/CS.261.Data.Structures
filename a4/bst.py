# Name: Robin Shindelman
# OSU Email: shindelr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 11/20/2023
# Description: This is an implementation of the Binary Search Tree (BST) data
# structure. A BST is characterized by a series of nodes with 0 to 2 children.
# There is always a root, that is, a single node from which all others branch.
# In a BST, the branch to the left of any given node will contain a value less
# than that contained in the parent node, and the branch on the right will be
# greater.


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #
    def add(self, value: object) -> None:
        """
        Add a value to the tree. The value will be made into a node and linked
        to the rest of the tree in the appropriate location.
        value: A value to be attached to a BST node.
        returns: None
        """
        # Initialize new root
        if self._root is None:
            self._root = BSTNode(value)
            return

        node = self._root
        parent = node
        # We'll know we're at leaf if the next node is None.
        while node is not None:
            if value < node.value:  # Go left
                parent, node = node, node.left
            elif value >= node.value:  # Go right
                parent, node = node, node.right

        if value >= parent.value:
            parent.right = BSTNode(value)  # Insert right
        else:
            parent.left = BSTNode(value)  # Insert left

    def remove(self, value: object) -> bool:
        """
        Delete a node in the BST. Calls several different helper methods
        depending on whether the node to be removed has 0, 1, or 2 children.
        This method will preserve the structure of the BST, moving any
        necessary nodes in order to stay valid.
        value: The value to be removed.
        returns: True if successful, False otherwise.
        """
        # Is there a tree here?
        if self._root is None:
            return False

        # Navigate to desired node & determine removal case:
        remove_node = self._root
        parent = remove_node
        # Iterate till we find the desired value, updating parent and next.
        while remove_node.value != value:
            if value < remove_node.value:  # Go left
                parent, remove_node = remove_node, remove_node.left
            elif value >= remove_node.value:  # Go right
                parent, remove_node, = remove_node, remove_node.right
            if remove_node is None:
                return False  # Base case to exit the loop if val doesn't exist

        # Removal case calls:
        # No children
        if remove_node.right is None and remove_node.left is None:
            self._remove_no_subtrees(parent, remove_node)
        # 1 child
        elif remove_node.right is not None and remove_node.left is  None:
            self._remove_one_subtree(parent, remove_node)
        elif remove_node.right is None and remove_node.left is not None:
            self._remove_one_subtree(parent, remove_node)
        # 2 children
        else:
            self._remove_two_subtrees(parent, remove_node)
        return True

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Remove a node with no children. This node is just a leaf, so simply
        dereference the node.
        remove_parent: The parent node to the node to be removed.
        remove_node: The node containing the value to be removed.
        returns: True if successful, None otherwise.
        """
        # Handle root case
        if self._root == remove_node:
            self._root = None
        # Determine left or right:
        if remove_parent.right == remove_node:
            remove_parent.right = None
        else:
            remove_parent.left = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Remove a node one just one child. Simply assigns the child to be
        adopted by the remove_node's parent.
        remove_parent: Parent of the node being removed.
        remove_node: Node being excised, also parent of one child.
        returns: True if successful.
        """
        # Handle root case separately since it doesn't have a parent.
        if self._root == remove_node:
            if remove_node.right is not None:
                self._root = remove_node.right
                return
            else:
                self._root = remove_node.left
                return

        # Determine left or right for the parent:
        if remove_parent.right == remove_node:  # Right subtree process
            if remove_node.right is not None:
                remove_parent.right = remove_node.right
            else:
                remove_parent.right = remove_node.left
        # Left subtree process:
        else:
            if remove_node.right is not None:
                remove_parent.left = remove_node.right
            else:
                remove_parent.left = remove_node.left

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Dereference a node that has 2 children. Calls _inorder_successor() in
        order to properly remove the node without compromising the tree's
        structure.
        remove_parent: Parent of the node to be removed, adopts
                       the inorder successor.
        remove_node: Node to be removed, has two children.
        returns: True
        """
        # Get the successor and their parent.
        successor, succ_parent = self._inorder_successor(remove_node)
        # Immediately move the left subtree over to the successor
        successor.left = remove_node.left

        # Edge cases for making sure all the nodes go where they're supposed to
        # If successor is not on removal_node's immediate right:
        if successor != remove_node.right:
            succ_parent.left = successor.right  # Succ_parent adopts succ orphan
            successor.right = remove_node.right  # Swap successor with removal node.
            if self._root != remove_node:
                if remove_parent.left == remove_node:  # Left subtree
                    remove_parent.left = successor
                else:
                    remove_parent.right = successor  # Right subtree
            else:
                self._root = successor # If root, simply swap.

        else:  # Otherwise, just swap out remove_node for successor.
            if self._root != remove_node:  # Check for root case!
                if remove_parent.right == remove_node:
                    remove_parent.right = successor
                else:
                    remove_parent.left = successor
            else:
                self._root = successor

    def _inorder_successor(self, remove_node):
        """
        Find remove_node's inorder successor. This is the leftmost node on
        remove_node's right subtree.
        remove_parent: The parent of the node to be removed.
        remove_node: Node being removed.
        returns: remove_node's inorder successor and its parent
        """
        node = remove_node.right
        parent = remove_node
        while node.left is not None:
            parent = node
            node = node.left
        return node, parent

    def contains(self, value: object) -> bool:
        """
        Check the BST for the argued value.
        value: A value possibly contained by a BSTNode.
        returns: True for success, False otherwise
        """
        # Tree is empty?
        if self._root is None:
            return False

        node = self._root
        while node is not None:
            if node.value == value:
                return True
            # Traverse:
            else:
                if value > node.value:  # Go right
                    node = node.right
                else:
                    node = node.left  # Else go left.
        return False  # Failure to find value

    def inorder_traversal(self) -> Queue:
        """
        Traverse the BST and queue up all its associated values into inorder
        arrangement.
        returns: Queue object of BST node values if tree is not empty,
        otherwise, an empty queue.
        """
        # Empty tree?
        if self._root is None:
            return Queue()

        ordered_q = Queue()
        ordered_q = self.inorder_rec(self._root, ordered_q)
        return ordered_q

    def inorder_rec(self, node, queue):
        """Helper function for inorder_traversal."""
        while node is not None:
            self.inorder_rec(node.left, queue)  # Go left, far as possible 1st
            queue.enqueue(node.value)  # Far as you can go? Enqueue.
            self.inorder_rec(node.right, queue) # Go right on the way back out.
            return queue

    def find_min(self) -> object:
        """
        Find the smallest value in the BST.
        returns: Value stored in a BSTNode.
        """
        # Empty list?
        if self._root is None:
            return None
        queue = self.inorder_traversal()  # Get the inorder queue.
        return queue.dequeue()  # Smallest elem is at the front.

    def find_max(self) -> object:
        """
        Find the largest value in the BST. This method could be improved I bet.
        returns: Value stored in BSTNode
        """
        # Empty Tree?
        if self._root is None:
            return None

        queue = self.inorder_traversal()  # Get the inorder queue.
        while queue.is_empty() is False:
            max = queue.dequeue()  # Dequeue till the last elem. That's max.
        return max

    def is_empty(self) -> bool:
        """
        Check if the tree is empty or not.
        returns: True if empty, false otherwise.
        """
        if self._root is None:
            return True
        return False

    def make_empty(self) -> None:
        """
        Remove all the nodes from the tree.
        returns: None.
        """
        self._root = None

# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':
    tree = BST([64, 30, 10, 2, 17, 32, 75, 72,73, 77, 90])
    tree.remove(75)
    print(tree)

    tree = BST([50, 40, 60, 30, 70, 20, 80, 45])
    tree.remove(40)
    print(tree)

    tree = BST([-62, -93, 67, -27, 45, 46, 54, 57, -6, -7])
    tree.remove(-62)
    print(tree)
    tree.remove(67)
    print(tree)

    tree = BST([0, 2, 99, 38, -82, -80, -10, -70, 93, 63])
    tree.remove(0)
    print(tree)
    print('\n--------------------------------------------------------------\n')

    tree = BST([-93, -92, -91, 6, -51, 15, 81, -14, 29, -2])
    tree.remove(-93)
    print(tree)
    tree.remove(-91)
    print(tree)
    tree.remove(-51)
    print(tree)

    tree= BST([1, 2, -6, -6, 16, 17, 14, -3, -13, 19, -2, 8, -5, 3, -20, -12, -12,
         -8, -3, 18, 9, -13, -10, 18, 12, -7, -2, 13, -3, -14])
    print(tree)

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = ((1, 1, 1, 1),
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E')
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)
    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    print("-------------------------------")
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
        print(tree.is_valid_bst())

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
        print(tree.is_valid_bst())

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
        print(tree.is_valid_bst())

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())


    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
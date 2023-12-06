# Name: Robin Shindelman
# OSU Email: shindelr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 11/10/20
# Description: This is an implementation of an AVL tree. An AVL tree is a
# special type of BST where it always stays balanced. This balancing is defined
# as making sure that every subtree of the AVL tree stays within a difference
# in height of no more than 1.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Add a node to the AVL tree. Actively rebalances the the tree after
        each node is added. Acts like the normal BST add() until the end when
        it calls rebalance().
        value: Value to be turned into an AVLNode() and added to the tree.
        returns: None
        """
        # Base Cases:
        if self.contains(value):  # No duplicates allowed.
            return
        if self._root is None:  # If the tree is empty, make a new root.
            self._root = AVLNode(value)
            return

        # ----------------Normal Insertion Here ---------------------- #
        node = self._root
        parent = node
        # We'll know we're at leaf if the next node is None.
        while node is not None:
            if value < node.value:  # Go left
                parent, node = node, node.left
            elif value >= node.value:  # Go right
                parent, node = node, node.right

        if value >= parent.value:
            parent.right = AVLNode(value)  # Insert right
            node = parent.right  # Store node for restructure below
            node.parent = parent

        else:
            parent.left = AVLNode(value)  # Insert left
            node = parent.left  # Store node for restructure below
            node.parent = parent
        # ----------------Begin Restructure Here ---------------------- #
        parent = node.parent  # Iterate back upwards through the tree
        while parent is not None:
            self._update_height(parent)
            self._rebalance(parent)
            parent = parent.parent

    def remove(self, value: object) -> bool:
        """
        Remove an AVLNode from the AVL tree. This method keeps the AVL tree
        balanced. It's mostly the same as the OG BST method but also handles
        calling rebalance().
        value: The value of the AVLNode to be removed.
        returns: True if successful, False otherwise.
        """
        # ----------- OG BST REMOVE ---------------------#
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
        avl_parent = remove_node.parent
        avl_node = remove_node

        # No children
        if remove_node.right is None and remove_node.left is None:
            self._remove_no_subtrees(parent, remove_node)

        # 1 child
        elif remove_node.right is not None and remove_node.left is  None:  # Right subtree removal
            self._remove_one_subtree(parent, remove_node)
            if avl_node.right is not None:  # Trying to update parent pointers.
                avl_node.right.parent = avl_parent
            if avl_node.left is not None:
                avl_node.left.parent = avl_parent
        elif remove_node.right is None and remove_node.left is not None:  # Left subtree removal
            self._remove_one_subtree(parent, remove_node)
            if avl_node.right is not None:  # Trying to update parent pointers.
                avl_node.right.parent = avl_parent
            if avl_node.left is not None:
                avl_node.left.parent = avl_parent

        # 2 children
        else:
            avl_parent = self._remove_two_subtrees(parent, remove_node)
            if avl_parent is None:
                self._update_height(remove_node.parent)  # Accomodate root changes
                if remove_node.parent.right is not None:
                    self._update_height(remove_node.parent.right)
                    self._rebalance(remove_node.parent.right)
                if remove_node.parent.left is not None:
                    self._update_height(remove_node.parent.left)
                    self._rebalance(remove_node.parent.right)
                self._rebalance(remove_node.parent)

        # -------------- Start Balancing -----------------#
        if self._root is not None: self._update_height(self._root)  # Just in case?
        while avl_parent is not None:
            self._update_height(avl_parent)
            if avl_parent.left is not None:
                self._update_height(avl_parent.left)  # Update everyone if you can!!
            if avl_parent.right is not None:
                self._update_height(avl_parent.right)
            self._rebalance(avl_parent)
            avl_parent = avl_parent.parent
        return True

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        Override the original BST remove_two_subtrees() method. This override
        changes a variety of the branches to keep track of all the changing
        nodes' height and parents.
        remove_parent: The parent of the AVLNode being removed.
        remove_node: The node being removed.
        returns: AVLNode to be used by rebalance()
        """
        # Get the successor and their parent.
        successor, succ_parent = self._inorder_successor(remove_node)
        # Immediately move the left subtree over to the successor
        successor.left = remove_node.left

        # Edge cases for making sure all the nodes go where they're supposed to
        # If successor is not on removal_node's immediate right:
        if successor != remove_node.right:
            succ_parent.left = successor.right  # Succ_parent adopts succ orphan
            if successor.right is not None:
                successor.right.parent = succ_parent
            successor.right = remove_node.right  # Swap successor with removal node.
            successor.right.parent = successor  # To try to get the parent pointer
            if self._root != remove_node:
                if remove_parent.left == remove_node:  # Left subtree
                    remove_parent.left = successor
                    successor.parent = remove_parent
                    if successor.left is not None:
                        successor.left.parent = successor
                    if successor.right is not None:
                        successor.right.parent = successor
                    return successor.left
                else:
                    remove_parent.right = successor  # Right subtree
                    successor.parent = remove_parent
                    if successor.right is not None:
                        successor.right.parent = successor
                    if successor.left is not None:
                        successor.left.parent = successor
                    return successor.right  # For Rebalancing

            else:
                self._root = successor # If root, simply swap.
                self._root.parent = None  # Deref old root
                self._root.right.parent = self._root  # Fix both child's refs.
                self._root.left.parent = self._root
                #return self._root.right  # Return Inorder succ parent for rebalance() to use.
                return succ_parent

        else:  # Otherwise, just swap out remove_node for successor.
            if self._root != remove_node:  # Check for root case!
                if remove_parent.right == remove_node:
                    remove_parent.right = successor
                    successor.parent = remove_parent
                    if successor.left is not None:
                        successor.left.parent = successor
                    if successor.right is not None:
                        successor.right.parent = successor
                    return successor.right

                else:
                    remove_parent.left = successor
                    successor.parent = remove_parent
                    successor.left.parent = successor
                    if successor.left is not None:
                        successor.left.parent = successor
                    if successor.right is not None:
                        successor.right.parent = successor
                return successor.left

            else:
                self._root = successor
                self._root.parent = None  # Deref old root
                if self._root.right is not None:
                    self._root.right.parent = self._root  # Fix both child's refs.
                if self._root.left is not None:
                    self._root.left.parent = self._root

                if self._root.right is not None:
                    return self._root.right  # Return Inorder succ parent for rebalance() to use
                if self._root.left is not None:
                    return self._root.left  # Or if no .right, return .left

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Calculate the balance factor of any given subtree. -1, 0, or 1 are
        all acceptable BFs for the tree. A negative int represents left
        heaviness, a positive one right heaviness. 0 is perfection.
        node: AVLNode acting as the root of the subtree to be measured
        returns: Int describing balance factor.
        """
        bf = self._get_height(node.right) - self._get_height(node.left)
        return bf

    def _get_height(self, node: AVLNode) -> int:
        """
        Retrieve the height of a given subtree. A null node is considered
        to have a height of -1.
        node: AVLNode root of the subtree.
        returns: Int representing the height.
        """
        if node is None:
            return -1
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Rotate nodes to the left. This is a counterclockwise rotation around
        the argued node, N. C represents right child of N and rotates.
        node: node 'N' being rotated around.
        returns: AVLNode(new_sub_root) to be used by rebalance()
        """
        child = node.right  # Initialize "C"
        node.right = child.left  # Move the child's right grandkid to N.left.
        if node.right is not None:
            node.right.parent = node

        child.left = node  # Make the rotation of N downwards
        node.parent = child  # Make the rotation of C upwards.
        self._update_height(node)
        self._update_height(child)
        return child  # Becomes new_sub_root in rebalance()

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Rotate the nodes to the right. This is a clockwise rotation around
        the argued node, which can be represented by N. C represents the left
        child of N, which will be rotating since the subtree has an imbalance
        the left side.
        node: node 'N' being rotated around.
        returns: AVLNode(new_sub_root) to be used by rebalance()
        """
        # Set up the values so that we don't break the chain.
        child = node.left  # Initialize "C"
        node.left = child.right  # Move the child's right grandkid to N.left.
        if node.left is not None:
            node.left.parent = node

        child.right = node  # Make the rotation of N downwards
        node.parent = child  # Make the rotation of C upwards.
        self._update_height(node)
        self._update_height(child)
        return child  # Becomes new_sub_root in rebalance()

    def _update_height(self, node: AVLNode) -> None:
        """
        Update the height of a node that has experienced restructuring.
        node: AVLNode to be adjusted.
        returns: None.
        """
        node.height = max(self._get_height(node.left),
                          self._get_height(node.right)) + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        Rebalance the avl tree. Checks a node's balance factor. Performs the
        rotation necessary in order to put the tree back together.
        node: AVLNode acting as the root of the subtree to be balanced.
        returns: None
        """
        # Left heavy balancing, rotate right
        if self._balance_factor(node) < -1:
            if self._balance_factor(node.left) > 0:  # Check for dbl rotate
                node.left = self._rotate_left(node.left)  # Rotate the undertree
                node.left.parent = node  # Reassign parent
            og_node_parent = node.parent
            new_sub_root = self._rotate_right(node)  # Pass N, new root is C
            new_sub_root.parent = og_node_parent  # Finally, dereference old parent.
            if og_node_parent is None:  # AKA the root of the whole tree
                self._root = new_sub_root
            else:
                if new_sub_root.value < og_node_parent.value:  # Figure out which side the new_sub_root goes on.
                    og_node_parent.left = new_sub_root
                else:
                    og_node_parent.right = new_sub_root

        # Right heavy balancing, rotate left
        elif self._balance_factor(node) > 1:
            if self._balance_factor(node.right) < 0:  # Check for dbl rotate
                node.right = self._rotate_right(node.right)
                node.right.parent = node
            # This is all just opposite of above
            og_node_parent = node.parent
            new_sub_root = self._rotate_left(node)
            new_sub_root.parent = og_node_parent
            if og_node_parent is None:  # AKA the root of the whole tree
                self._root = new_sub_root
            else:
                if new_sub_root.value < og_node_parent.value:  # Figure out which side the new_sub_root goes on.
                    og_node_parent.left = new_sub_root
                else:
                    og_node_parent.right = new_sub_root

        # No balancing required!
        else:
            self._update_height(node)  # Check for height update needs.


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':
    print('//------Self Testing---------//')
    tree = [3, 2, 1]
    AVLtree = AVL(tree)
    print(AVLtree)
    #tree = [10, 7, 20, 15, 30, 3, 8, 2, 1]
    tree = [3, 1, 2]
    AVLtree = AVL(tree)
    print(AVLtree)

    tree = AVL([50, 40, 60, 30, 70, 20, 80, 45])
    print(f'Input: {tree}, delete: 30')
    tree.remove(30)
    print(f'Result: {tree}')
    print(f'Expected: AVL preorder [50, 40, 20, 45, 70, 60, 80]')

    tree = AVL([-28, 68, 45, -50, -99, -46, 18, 30, 61, -2])
    removals = [-28, 45]
    print(f'Input: {tree}, removing: {removals}')
    for val in removals:
        tree.remove(val)
        print(f'Removed {val}, Result: {tree}')
        assert tree.is_valid_avl()

    tree = AVL([26, 71, -87, -21, 45, -47, -72, -38, 94, 31])
    print(f'Input: {tree}, remove: 26')
    tree.remove(26)
    print(f'Result: {tree}')
    assert tree.is_valid_avl()

    tree = AVL([66, 3, 100, -54, -17, 15, 17, 47, -67, -65])
    print(f'Input: {tree}, remove: 66')
    tree.remove(66)
    print(f'Result: {tree}')
    assert tree.is_valid_avl()

    tree = AVL([-62, 100, -50, 79, 20, -75, 54, 87, -37, -34])
    removals = [-62, -50, 20, 54, -37]
    print(f'Input: {tree}, removing: {removals}')
    for val in removals:
        tree.remove(val)
        print(f'Removed {val}, Result: {tree}')
        assert tree.is_valid_avl()

    tree = AVL([-95, 4, -58, 11, 16, 84, -76, -42, 56, -4])
    removals = [-95, -58, 16, -76]
    print(f'Input: {tree}, removing: {removals}')
    for val in removals:
        tree.remove(val)
        print(f'Removed {val}, Result: {tree}')
        assert tree.is_valid_avl()

    tree = AVL([32, 34, 68, -17, 80, -76, 54, -74, 88, -2])
    removals = [32, 68, 80, 54]
    print(f'Input: {tree}, removing: {removals}')
    for val in removals:
        tree.remove(val)
        print(f'Removed {val}, Result: {tree}')
        assert tree.is_valid_avl()

    tree = AVL([77316, 72838, -94574, -31446, 98095, 11955, -96071, 68027, 15163, -579, -4928, -89532, 63434, 84948, -63660, 4956, 7909, 35322, -87941, 57084])
    removals = [77316, -94574, 98095, -96071, 15163, -4928, 63434, -63660, 7909]
    print(f'Input: {tree}, removing: {removals}')
    for val in removals:
        tree.remove(val)
        print(f'Removed {val}, Result: {tree}')
        assert tree.is_valid_avl()

    print('//--------------------------//\n')

    """
    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR  # Passed
        (1, 2, 3),  # RR  # Passed
        (3, 2, 1),  # LL  # Passed
    )
    for case in test_cases:
        print(f'Test Case: {case}')
        tree = AVL(case)
        print(f'{tree}\n')

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    
    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')
    """

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        assert tree.is_valid_avl()
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        assert tree.is_valid_avl()
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        assert tree.is_valid_avl()
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        assert tree.is_valid_avl()
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    """

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
    """

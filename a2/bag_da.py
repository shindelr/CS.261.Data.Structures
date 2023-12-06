# Name: Robin Shindelman
# OSU Email: shindelr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 10/30/2023
# Description: This is an implementation of the simple ADT known as Bag. In
# short, Bag acts just like a physical bag would. Things can be put it or taken
# out, the contents can be counted, and the whole thing can be dumped out.


from dynamic_array import *


class Bag:
    def __init__(self, start_bag=None):
        """
        Init new bag based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

        # populate bag with initial values (if provided)
        # before using this feature, implement add() method
        if start_bag is not None:
            for value in start_bag:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "BAG: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da.get_at_index(_))
                          for _ in range(self._da.length())])
        return out + ']'

    def size(self) -> int:
        """
        Return total number of items currently in the bag
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def add(self, value: object) -> None:
        """
        Add an item to the bag.
        value: A valid item, must be the same type as everything else
                already in the bag.
        Returns: None
        """
        self._da.append(value)

    def remove(self, value: object) -> bool:
        """
        Remove the first item matching the given value from the bag.
        value: An item in the bag.
        Returns: True if the item was removed, False otherwise.
        """
        # Iterate through the bag looking for the value.
        for i in range(self._da.length()):
            if self._da[i] == value:
                # Call remove, is this O(n)?
                self._da.remove_at_index(i)
                return True
        # If you get to the bottom, the item isn't there.
        return False

    def count(self, value: object) -> int:
        """
        Tabulate the number of items in the bag matching the given value.
        value: An item in the bag.
        Returns: Integer representing the number of occurrence.
        """
        count = 0
        # Count the number of times the item matches the val.
        for item in self._da:
            if item == value:
                count += 1
        return count

    def clear(self) -> None:
        """
        Dump the bag out into the trash! It'll be empty after this method is
        called.
        Returns: None
        """
        if self.size() == 0:
            return None
        self._da = self._da.slice(0, 0)

    def equal(self, second_bag: "Bag") -> bool:
        """
        Compare the contents of two bags to see if they are equal.
        second_bag: Another bag data structure to compare to the current bag.
        Returns: True if equal, False otherwise.
        """
        # Base case, the bags aren't the same size.
        if self.size() != second_bag.size():
            return False
        # Iterate through the second bag comparing the counts to each other.
        for value in second_bag:
            if self.count(value) != second_bag.count(value):
                return False
        return True

    def __iter__(self):
        """
        Create an iterator to traverse across through the Bag during a loop.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Retrieve the next item in the bag to pass to the iterator, then moves
        forward one item.
        """
        # Use an exception, we don't want the whole thing to crash for this.
        try:
            item = self._da[self._index]
        except DynamicArrayException:
            raise StopIteration

        # Advance the index.
        self._index += 1
        return item


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# add example 1")
    bag = Bag()
    print(bag)
    values = [10, 20, 30, 10, 20, 30]
    for value in values:
        bag.add(value)
    print(bag)

    print("\n# remove example 1")
    bag = Bag([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(bag)
    print(bag.remove(7), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)

    print("\n# count example 1")
    bag = Bag([1, 2, 3, 1, 2, 2])
    print(bag, bag.count(1), bag.count(2), bag.count(3), bag.count(4))

    print("\n# clear example 1")
    bag = Bag([1, 2, 3, 1, 2, 3])
    print(bag)
    bag.clear()
    print(bag)

    bag1 = Bag([55813, -2283, 32023, 84495, -65204, 58923,
                -33876, 28989, 12792, -79062])
    bag2 = Bag([58923, -65204, -2283, -33876, 12792, 55813,
                84495, 28989, 24885, 32023])

    assert bag1.equal(bag2) is False

    print("\n# equal example 1")
    bag1 = Bag([10, 20, 30, 40, 50, 60])
    bag2 = Bag([60, 50, 40, 30, 20, 10])
    bag3 = Bag([10, 20, 30, 40, 50])
    bag_empty = Bag()

    print(bag1, bag2, bag3, bag_empty, sep="\n")
    print(bag1.equal(bag2), bag2.equal(bag1))
    print(bag1.equal(bag3), bag3.equal(bag1))
    print(bag2.equal(bag3), bag3.equal(bag2))
    print(bag1.equal(bag_empty), bag_empty.equal(bag1))
    print(bag_empty.equal(bag_empty))
    print(bag1, bag2, bag3, bag_empty, sep="\n")

    bag1 = Bag([100, 200, 300, 200])
    bag2 = Bag([100, 200, 30, 100])
    print(bag1.equal(bag2))

    print("\n# __iter__(), __next__() example 1")
    bag = Bag([5, 4, -8, 7, 10])
    print(bag)
    for item in bag:
        print(item)

    print("\n# __iter__(), __next__() example 2")
    bag = Bag(["orange", "apple", "pizza", "ice cream"])
    print(bag)
    for item in bag:
        print(item)





# This great piece of script that tells you what an instance looks like while debugging. Put it at the bottom of
# a class!


def __repr__(self):
    """
    Allows the debugger to show an object's attributes rather than its
    address in memory.
    """
    return "{}({!r})".format(self.__class__.__name__, self.__dict__)

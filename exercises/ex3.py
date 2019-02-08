"""CSC148 Exercise 3: Stacks and a Chain of People

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains starter code for Exercise 3.
It is divided into two parts:
- Task 1, which contains two functions you should implement using only
  the public interface of Stacks (initializer, is_empty, push, pop)
- Task 2, which contains the definition of two new classes, Person and
  PeopleChain. You'll have to read their documentation carefully to understand
  how to use them.
"""
from typing import List, Optional
from stack import Stack


##############################################################################
# Task 1: More Stack Exercises
##############################################################################
def reverse(stack: Stack) -> None:
    """Reverse all the elements of <stack>.

    Do nothing if the stack is empty.

    >>> stack = Stack()
    >>> stack.push(1)
    >>> stack.push(2)
    >>> reverse(stack)
    >>> stack.pop()
    1
    >>> stack.pop()
    2
    """
    temp_stack1 = Stack()
    temp_stack2 = Stack()
    while not stack.is_empty():
        item = stack.pop()
        temp_stack1.push(item)

    while not temp_stack1.is_empty():
        item = temp_stack1.pop()
        temp_stack2.push(item)

    while not temp_stack2.is_empty():
        item = temp_stack2.pop()
        stack.push(item)


def merge_alternating(stack1: Stack, stack2: Stack) -> Stack:
    """Return a stack by merging two stacks in alternating order.

    Precondition: <stack1> and <stack2> have the same size.

    The new stack's top element is the top element of <stack1>,
    followed by the top element of <stack2>, followed by the next element
    of <stack1>, then <stack2>, etc.

    If <stack1> and <stack2> are both empty, the new stack should also be empty.

    <stack1> and <stack2> should be unchanged when the function ends.

    >>> s1 = Stack()
    >>> s2 = Stack()
    >>> s1.push('a')
    >>> s1.push('b')
    >>> s1.push('c')
    >>> s2.push(1)
    >>> s2.push(2)
    >>> s2.push(3)
    >>> merged = merge_alternating(s1, s2)
    >>> merged.pop()
    'c'
    >>> merged.pop()
    3
    >>> merged.pop()
    'b'
    >>> merged.pop()
    2
    >>> merged.pop()
    'a'
    >>> merged.pop()
    1
    >>> merged.is_empty()
    True
    >>> s1.is_empty()
    False
    >>> s2.is_empty()
    False
    """
    merged_stack = Stack()
    temp_stack1 = Stack()
    temp_stack2 = Stack()
    temp_stack3 = Stack()
    while not stack1.is_empty():
        item = stack1.pop()
        temp_stack1.push(item)
        temp_stack2.push(item)
        item1 = stack2.pop()
        temp_stack1.push(item1)
        temp_stack3.push(item1)

    while not temp_stack1.is_empty():
        item = temp_stack1.pop()
        merged_stack.push(item)

    while not temp_stack2.is_empty():
        item = temp_stack2.pop()
        stack1.push(item)

    while not temp_stack3.is_empty():
        item = temp_stack3.pop()
        stack2.push(item)

    return merged_stack


##############################################################################
# Task 2: A Chain of People
##############################################################################


class Person:
    """A person in a chain of people.

    === Attributes ===
    name: The name of this person.
    next: The next person in the chain, or None if this person is not holding
        onto anyone.
    """
    name: str
    next: Optional['Person']

    def __init__(self, name: str) -> None:
        """Initialize a person with the given name.

        The new person initially is not holding onto anyone.
        """
        self.name = name
        self.next = None  # Initially holding onto no one


class PeopleChain:
    """A chain of people.

    === Attributes ===
    leader: the first person in the chain, or None if the chain is empty.
    """
    leader: Optional['Person']

    def __init__(self, names: List[str]) -> None:
        """Initialize people linked together in the order provided in <names>.

        The leader of the chain is the first person in <names>.
        """
        if names == []:
            # No leader, representing an empty chain!
            self.leader = None
        else:
            # Initialize leader
            self.leader = Person(names[0])
            current_person = self.leader
            for name in names[1:]:
                # Set the link for the current person
                current_person.next = Person(name)
                # Update the current person
                # Note that current_person always refers to
                # the LAST person in the chain
                current_person = current_person.next

    def get_leader(self) -> str:
        """Return the name of the leader of the chain.

        Raise ShortChainError if chain has no leader.

        >>> chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
        >>> chain.get_leader()
        'Iron Man'

        """
        if self.leader.name is not None:
            return self.leader.name

    def get_second(self) -> str:
        """Return the name of the second person in the chain.

        That is, return the name of the person the leader is holding onto.
        Raise ShortChainError if chain has no second person.

        >>> chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
        >>> chain.get_second()
        'Janna'
        """
        if self.leader.name is not None:

            current = self.leader.next
            if current.name is not None:

                return current.name
            else:
                raise ShortChainError
        else:
            raise ShortChainError

    def get_third(self) -> str:
        """Return the name of the third person in the chain.

        Raise ShortChainError if chain has no third person.

        >>> chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
        >>> chain.get_third()
        'Kevan'
        """
        if self.leader.name is not None:
            current = self.leader.next
            if current.name is not None:
                third = current.next
                if third.name is not None:
                    return third.name
                else:
                    raise ShortChainError
            else:
                raise ShortChainError
        else:
            raise ShortChainError

    def get_nth(self, n: int) -> str:
        """Return the name of the n-th person in the chain.

        Precondition: n >= 1
        Raise ShortChainError if chain doesn't have n people.
        Indexing here starts at 1 (see doctest for an example).

        >>> chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
        >>> chain.get_nth(1)
        'Iron Man'
        >>> s = PeopleChain(['Iron Man', 'Janna', 'Kevan','hi', 'hello'])
        >>> s.get_nth(3)
        'Kevan'




        """
        # Remember: you must use a for or while loop in this function body!
        # If you use a for loop but don't need to use the loop variable,
        # use an underscore for the variable name:
        #
        # for _ in range(10):
        #     <code that doesn't use the index>

        """current = self.leader
        if n == 1:
            return self.leader.name
        count = 2

        while current.next is not None:
            if count == n:
                temp = current.next
                return temp.name
            elif count < n:
                temp = current.next
                current.next = temp.next
                count += 1
            elif count > n:
                raise ShortChainError
"""

        count = 2
        current = self.leader
        if n == 1:
            return self.leader.name
        while count <= n:
            temp = current.next
            if temp is None:

                raise ShortChainError
            elif temp is not None:
                if count == n:
                    return temp.name
                else:
                    current.next = temp.next
                    count += 1







class ShortChainError(Exception):
    """
    Raises an error
    """
    pass


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'typing', 'doctest', 'python_ta', 'stack'
        ]
    })

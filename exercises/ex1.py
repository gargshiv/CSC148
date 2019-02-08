"""CSC148 Exercise 1: Basic Object-Oriented Programming

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for Exercise 1.
It contains two classes that work together:
- SuperDuperManager, which manages all the cars in the system
- Car, a class which represents a single car in the system

Your task is to design and implement the Car class, and then modify the
SuperDuperManager methods so that they make proper use of the Car class.

You may not modify the public interface of any of the SuperDuperManager methods.
We have marked the parts of the code you should change with TODOs, which you
should remove once you've completed them.

Notes:
  1. We'll talk more about private attributes on Friday's class.
     For now, treat them the same as any other instance attribute.
  2. You'll notice we use a trailing underscore for the parameter name
     "id_" in a few places. It is used to avoid conflicts with Python
     keywords.Â Here we want to have a parameter named "id", but that is
     already the name of a built-in function.Â So we call it "id_" instead.
"""
from typing import Dict, Optional, Tuple


class SuperDuperManager:
    """A class that keeps track of all cars in the Super Duper system.
    """
    # === Private Attributes ===
    # _cars:
    #   A map of unique string identifiers to the corresponding Car.
    #   For example, _cars['car1'] would be a Car object corresponding to
    #   the id 'car1'.
    _cars: Dict[str, 'Car']

    def __init__(self) -> None:
        """Initialize a new SuperDuperManager.

        There are no cars in the system when first created.
        """
        self._cars = {}

    def add_car(self, id_: str, fuel: int) -> None:
        """Add a new car to the system.

        The new car is identified by the string <id_>, and has initial amount
        of fuel <fuel>.

        Do nothing if there is already a car with the given id.

        Precondition: fuel >= 0.
        """
        # Check to make sure the identifier isn't already used.
        if id_ not in self._cars:
            self._cars[id_] = Car(fuel)

    def move_car(self, id_: str, new_x: int, new_y: int) -> None:
        """Move the car with the given id.

        The car called <id_> should be moved to position (<new_x>, <new_y>).
        Do nothing if there is no car with the given id,
        or if the corresponding car does not have enough fuel.
        """
        if id_ in self._cars:
            curr = self._cars[id_]
            distance = abs(new_x - curr.x) + abs(new_y - curr.y)
            if curr.fuel - distance >= 0:
                curr.fuel -= distance
                curr.x = new_x
                curr.y = new_y

    def get_car_position(self, id_: str) -> Optional[Tuple[int, int]]:
        """Return the position of the car with the given id.
        Return a tuple of the (x, y) position of the car with id <id_>.
        Return None if there is no car with the given id.
        """
        if id_ in self._cars:
            curr = self._cars[id_]
            return (curr.x, curr.y)

    def get_car_fuel(self, id_: str) -> Optional[int]:
        """Return the amount of fuel of the car with the given id.

        Return None if there is no car with the given id.
        """
        if id_ in self._cars:
            return self._cars[id_].fuel

    def dispatch(self, x: int, y: int) -> None:
        """Move a car to the given location.

        Choose a car to move based on the following criteria:
        (1) Only consider cars that *can* move to the location.
            (Ignore ones that don't have enough fuel.)
        (2) After (1), choose the car that would move the *least* distance to
            get to the location.
        (3) If there is a tie in (2), pick the car whose id comes first
            alphabetically. Use < and/or > to compare the strings.
        (4) If no cars can move to the given location, do nothing.
        """

        # initial comparison variables for optimal car to dispatch
        closest_distance = None
        curr = None

        for (name, car) in self._cars.items():
            distance = abs(car.x - x) + abs(car.y - y)

            # if car has enough fuel, then check if its the closest car.
            if car.fuel - distance >= 0:
                if closest_distance is None or distance < closest_distance:
                    closest_distance = distance
                    curr = name
                elif distance == closest_distance:
                    # when two cars are the same distance away,
                    #<alpha_order> determines which id is alphabetcally first
                    curr = alpha_order(name, curr)

        if curr is not None:
            self.move_car(curr, x, y)

class Car:
    """A car in the Super system.

    === Public attributes ===
    x: the x-coordinate of this car's position
    y: the y-coordinate of this car's position
    fuel: the amount of fuel remaining this car has remaining

    === Representation invariants ===
    fuel >= 0
    """
    x: int
    y: int
    fuel: int
    def __init__(self, fuel: int) -> None:
        self.x = 0
        self.y = 0
        self.fuel = fuel

def alpha_order(s1: str, s2: str) -> str:
    """
    Compares two strings and retuns the string
    which comes alphabetically before the other.
    >>> alpha_order('bmw', 'alfa')
    alfa
    """
    if s1 < s2:
        return s1
    else:
        return s2

if __name__ == '__main__':
    # Run python_ta to ensure this module passes all checks for
    # code inconsistencies and forbidden Python features.
    # Useful for debugging!
    import python_ta
    python_ta.check_all()

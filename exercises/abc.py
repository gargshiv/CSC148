import unittest
import network_functions


class TestGetAverageFriendCount(unittest.TestCase):
    def test_get_average_empty(self):
        param = {}
        actual = network_functions.get_average_friend_count(param)
        expected = 0.0
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_get_average_one_person_one_friend(self):
        param = {'Jay Pritchett': ['Claire Dunphy']}
        actual = network_functions.get_average_friend_count(param)
        expected = 1.0
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_get_average_one_person_no_friend(self):
        param = {'First Last': []}
        actual = network_functions.get_average_friend_count(param)
        expected = 0.0
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_get_average_one_person_multiple_friend(self):
        param = {'Popular Dude': ['Jacob Chmura', 'Pior Szaran', \
                                  'Daniel Efinimnko', 'Will Wang']}
        actual = network_functions.get_average_friend_count(param)
        expected = 4.0
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_get_average_multiple_person_no_friend(self):
        param = {'Anti Social': [], 'No Friends': [], 'Needs Gainz': [], \
                 'Yuriy Bilynets': []}
        actual = network_functions.get_average_friend_count(param)
        expected = 0.0
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_get_average_multiple_person_one_friend(self):
        param = {'One Friend': ['Friendly Guy'], 'Mathew Beak': ['Total Guy'], \
                 'Last one': ['Also friendly']}
        actual = network_functions.get_average_friend_count(param)
        expected = 1.0
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_get_average_multiple_person_multiple_friend(self):
        param = {'Popular Dude': ['Jacob Chmura', 'Pior Szaran', \
                                  'Daniel Efinimnko', 'Will Wang'], \
                 'Justin bieber': ['Selena Gomez', 'Dead Mau5', 'Pior Szaran', \
                                   'White girl', 'Shivam G'],
                 'Faze Rain': ['Faze Adapt', \
                               'Lindsay Bul'],
                 'Person Name': ['Andrew toast', 'Liam Cheap', \
                                 'Diego Maro', 'C Ronaldo'], 'fIRST Last': [],
                 'My name': [], \
                 'John Peep': ['Amy Gin'], 'Woody Allen': [], 'Lone mans': []}
        actual = network_functions.get_average_friend_count(param)
        expected = 2.0
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_get_average_multiple_person_multiple_friend_constant(self):
        param = {'Popular Dude': ['Jacob Chmura', 'Pior Szaran', \
                                  'Daniel Efinimnko', 'Will Wang'], '\
                                  Justin bieber': ['Selena Gomez', 'Dead Mau5', \
                                                   'Pior Szaran', 'Shivam G'], \
                 'Faze Rain': ['Faze Adapt', \
                               'Lindsay Bul', \
                               'Little DudE', \
                               'Turtle Name'], \
                 'Person Name': ['Andrew toast', \
                                 'Liam Cheap', \
                                 'Diego Maro', \
                                 'C Ronaldo']}
        actual = network_functions.get_average_friend_count(param)
        expected = 4.0
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


if __name__ == '__main__':
    unittest.main(exit=False)


def get_average_friend_count(person_to_friends: Dict[str, List[str]]) -> float:
    """Return the average number of friends that people who appear as keys in
    the given "person to friends" dictionary have.

    >>> d = {'a': ['1', '2', '3', '4'], 'b': ['1', '2']}
    >>> get_average_friend_count(d)
    3.0

    >>> d = {'a': ['1', '2', '3', '4']}
    >>> get_average_friend_count(d)
    4.0

    """

    total_list = []
    for person in person_to_friends:
        num_friends = len(person_to_friends[person])
        total_list.append(num_friends)

    if total_list == []:
        return 0.0
    else:
        return sum(total_list) / len(total_list)


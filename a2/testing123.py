"""Testing 123
"""

raw_stations = [{'num': 1, 'num2': 2}, {'num': 2, 'num2': 4}, {'num': 3, 'num2': 6}]

print(raw_stations)
stations = {}

for dictionary in raw_stations:
    first = dictionary['num']

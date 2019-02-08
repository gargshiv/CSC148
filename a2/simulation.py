"""Assignment 1 - Simulation

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Simulation class, which is the main class for your
bike-share simulation.

At the bottom of the file, there is a sample_simulation function that you
can use to try running the simulation at any time.
"""
import csv
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple

from bikeshare import Ride, Station
from container import PriorityQueue
from visualizer import Visualizer

# Datetime format to parse the ride data
DATETIME_FORMAT = '%Y-%m-%d %H:%M'


class Simulation:
    """Runs the core of the simulation through time.

    === Attributes ===
    all_rides:
        A list of all the rides in this simulation.
        Note that not all rides might be used, depending on the timeframe
        when the simulation is run.
    all_stations:
        A dictionary containing all the stations in this simulation.
    visualizer:
        A helper class for visualizing the simulation.
    active_rides
        A list that contains the active rides that progess currently in the
        time of the simulation
    """
    all_stations: Dict[str, Station]
    all_rides: List[Ride]
    visualizer: Visualizer
    active_rides: List[Ride]
    event_priority: PriorityQueue['Event']

    def __init__(self, station_file: str, ride_file: str) -> None:
        """Initialize this simulation with the given configuration settings.
        """
        self.visualizer = Visualizer()
        self.all_stations = create_stations(station_file)
        self.all_rides = create_rides(ride_file, self.all_stations)
        self.active_rides = []
        self.event_priority = PriorityQueue()

    def run(self, start: datetime, end: datetime) -> None:
        """Run the simulation from <start> to <end>.
        """
        for ride in self.all_rides:
            if ride.start_time >= start:
                self.event_priority.add(RideStartEvent(self, ride.start_time,
                                                       ride))
        step = timedelta(minutes=1)  # Each iteration spans one minute of time

        while start <= end:
            self._update_active_rides_fast(start)
            #self._update_active_rides(start)
            if start < end:
                self._update_availability_and_unoccupied()
            self.visualizer.render_drawables(
                list(self.all_stations.values()) + self.active_rides, start)
            start += step
            # if start == end:
            #     self.active_rides = []

        # Leave this code at the very bottom of this method.
        # It will keep the visualization window open until you close
        # it by pressing the 'X'.

        while True:
            if self.visualizer.handle_window_events():
                return  # Stop the simulation

    def _update_availability_and_unoccupied(self):
        """
        updates the stations availability and unoccupied method per minute
        """
        for station in self.all_stations.values():
            station.low_availabilty()
            station.low_unoccupied()

    def _update_active_rides_fast(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   see Task 5 of the assignment handout
        """
        while not self.event_priority.is_empty():
            current_event = self.event_priority.remove()
            if current_event.ride.start_time >= time:
                self.event_priority.add(current_event)
                return
            #else:
             #   self.event_priority.add(current_event.process)

    def _update_active_rides(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   Loop through `self.all_rides` and compare each Ride's start and
            end times with <time>.

            If <time> is between the ride's start and end times (inclusive),
            then add the ride to self.active_rides if it isn't already in
            that list.

            Otherwise, remove the ride from self.active_rides if it is in
            that list.

        -   This means that if a ride started before the simulation's time
            period but ends during or after the simulation's time period,
            it should still be added to self.active_rides.
        """
        for current_ride in self.all_rides:
            ride_station_start = current_ride.start
            ride_station_end = current_ride.end

            s = current_ride.start_time
            e = current_ride.end_time
            if time == s and time < e:
                if ride_station_start.num_bikes > 0 and ride_station_start. \
                        unocc_spots != ride_station_start.capacity:
                    ride_station_start.num_bikes -= 1
                    ride_station_start.stats['starting rides'] += 1
                    ride_station_start.unocc_spots += 1
                    self.active_rides.append(current_ride)
            if time == e and current_ride in self.active_rides:
                if ride_station_end.num_bikes < ride_station_end.capacity and \
                                ride_station_end.unocc_spots > 0:
                    ride_station_end.stats['ending rides'] += 1
                    ride_station_end.num_bikes += 1
                    ride_station_end.unocc_spots -= 1
                    self.active_rides.remove(current_ride)
                else:
                    self.active_rides.remove(current_ride)

    def calculate_statistics(self) -> Dict[str, Tuple[str, float]]:
        """Return a dictionary containing statistics for this simulation.

        The returned dictionary has exactly four keys, corresponding
        to the four statistics tracked for each station:
          - 'max_start'
          - 'max_end'
          - 'max_time_low_availability'
          - 'max_time_low_unoccupied'

        The corresponding value of each key is a tuple of two elements,
        where the first element is the name (NOT id) of the station that has
        the maximum value of the quantity specified by that key,
        and the second element is the value of that quantity.

        For example, the value corresponding to key 'max_start' should be the
        name of the station with the most number of rides started at that
        station, and the number of rides that started at that station.
        """

        max_start = -1
        max_start_station_name = None
        max_end = -1
        max_end_station_name = None
        max_avail = -1
        max_avail_station_name = None
        max_unocc = -1
        max_unocc_station_name = None

        for station in self.all_stations.values():
            if station.stats['starting rides'] >= max_start:
                if station.stats['starting rides'] > max_start:
                    max_start = station.stats['starting rides']
                    max_start_station_name = station.name

                elif station.stats['starting rides'] == max_start:
                    if station.name < max_start_station_name:
                        max_start_station_name = station.name

            if station.stats['ending rides'] >= max_end:
                if station.stats['ending rides'] > max_end:
                    max_end = station.stats['ending rides']
                    max_end_station_name = station.name
                elif station.stats['ending rides'] == max_start:
                    if station.name < max_end_station_name:
                        max_end_station_name = station.name

            if station.stats['low availability'] >= max_avail:
                if station.stats['low availability'] > max_avail:
                    max_avail_station_name = station.name
                    max_avail = station.stats['low availability']
                elif station.stats['low availability'] == max_avail:
                    if station.name < max_avail_station_name:
                        max_avail_station_name = station.name

            if station.stats['low unoccupied'] >= max_unocc:
                if station.stats['low unoccupied'] > max_unocc:
                    max_unocc_station_name = station.name
                    max_unocc = station.stats['low unoccupied']
                elif station.stats['low unoccupied'] == max_unocc:
                    if station.name < max_unocc_station_name:
                        max_unocc_station_name = station.name

        return {
            'max_start': (max_start_station_name, max_start),
            'max_end': (max_end_station_name, max_end),
            'max_time_low_availability': (max_avail_station_name, max_avail),
            'max_time_low_unoccupied': (max_unocc_station_name, max_unocc)
        }


def create_stations(stations_file: str) -> Dict[str, 'Station']:
    """Return the stations described in the given JSON data file.

    Each key in the returned dictionary is a station id,
    and each value is the corresponding Station object.
    Note that you need to call Station(...) to create these objects!

    Precondition: stations_file matches the format specified in the
                  assignment handout.

    This function should be called *before* _read_rides because the
    rides CSV file refers to station ids.
    """
    # Read in raw data using the json library.
    with open(stations_file, encoding="utf-8") as file:
        raw_stations = json.load(file)

    stations = {}
    for s in raw_stations['stations']:
        station_id = s['n']
        station_name = s['s']
        station_lat = float(s['la'])
        station_long = float(s['lo'])
        num_of_bikes = int(s['da'])
        num_of_emptyspots = int(s['ba'])
        station_capacity = num_of_bikes + num_of_emptyspots
        stations[station_id] = Station((station_long, station_lat),
                                       station_capacity, num_of_bikes,
                                       station_name)

        # Extract the relevant fields from the raw station JSON.
        # s is a dictionary with the keys 'n', 's', 'la', 'lo', 'da', and 'ba'
        # as described in the assignment handout.
        # NOTE: all of the corresponding values are strings, and so you need
        # to convert some of them to numbers explicitly using int() or float().

    return stations


def create_rides(rides_file: str,
                 stations: Dict[str, 'Station']) -> List['Ride']:
    """Return the rides described in the given CSV file.

    Lookup the station ids contained in the rides file in <stations>
    to access the corresponding Station objects.

    Ignore any ride whose start or end station is not present in <stations>.

    Precondition: rides_file matches the format specified in the
                  assignment handout.
    """
    rides = []
    with open(rides_file) as file:
        for line in csv.reader(file):
            # line is a list of strings, following the format described
            # in the assignment handout.
            #
            # Convert between a string and a datetime object
            # using the function datetime.strptime and the DATETIME_FORMAT
            # constant we defined above. Example:
            # >>> datetime.strptime('2017-06-01 8:00', DATETIME_FORMAT)
            # datetime.datetime(2017, 6, 1, 8, 0)
            if line[1] in stations and line[3] in stations:
                start_time = datetime.strptime(line[0], DATETIME_FORMAT)
                end_time = datetime.strptime(line[2], DATETIME_FORMAT)
                start_station = line[1]
                end_station = line[3]

                rides.append(Ride(stations[start_station], stations[end_station]
                                  , (start_time, end_time)))

    return rides


class Event:
    """An event in the bike share simulation.

    Events are ordered by their timestamp.
    """
    simulation: 'Simulation'
    time: datetime

    def __init__(self, simulation: 'Simulation', time: datetime) -> None:
        """Initialize a new event."""
        self.simulation = simulation
        self.time = time

    def __lt__(self, other: 'Event') -> bool:
        """Return whether this event is less than <other>.
        Events are ordered by their timestamp.
        """
        return self.time < other.time

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.

        Return a list of new events spawned by this event.
        """
        raise NotImplementedError


class RideStartEvent(Event):
    """An event corresponding to the start of a ride."""
    ride: Ride

    def __init__(self, sim: 'Simulation', time: datetime, ride: Ride) -> None:
        """Initialize a new event."""
        Event.__init__(self, sim, time)
        self.ride = ride

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.
            Return a list of new events spawned by this event.
        """
        start_ride = []
        self.simulation.active_rides.append(self.ride)
        self.simulation.update_giving_station(self.ride, self.time)
        start_ride.append(RideEndEvent(self.simulation, self.ride.end_time,
                                       self.ride))
        return start_ride


class RideEndEvent(Event):
    """An event corresponding to the start of a ride."""
    ride: Ride

    def __init__(self, sim: 'Simulation', time: datetime, ride: Ride) -> None:
        Event.__init__(self, sim, time)
        self.ride = ride

    def process(self) -> None:
        """Process this event by updating the state of the simulation.
        Return a list of new events spawned by this event.
        """
        self.simulation.update_taking_station(self.ride, self.time)
        self.simulation.active_rides.remove(self.ride)


def sample_simulation() -> Dict[str, Tuple[str, float]]:
    """Run a sample simulation. For testing purposes only."""

    sim = Simulation('stations.json', 'sample_rides.csv')
    sim.run(datetime(2017, 6, 1, 8, 0, 0),
            datetime(2017, 6, 1, 9, 0, 0))
    return sim.calculate_statistics()


def update_giving_station(ride: Ride, time: datetime) -> None:
    """Decrease the num_bikes of a station if the ride is being
    added to the active rides list
       """
    if ride.start_time == time:
        if ride.start.num_bikes > 0:
            ride.start.num_bikes -= 1


def update_taking_station(ride: Ride, time: datetime) -> None:
    """Increase the num_bikes of a station if the ride is
    being added to the active rides list only if we haven't exceeded the
    station capacity yet."""

    if ride.end_time == time:
        if ride.end.capacity > ride.end.num_bikes:
            ride.end.num_bikes += 1


if __name__ == '__main__':
    # Uncomment these lines when you want to check your work using python_ta!
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['create_stations', 'create_rides'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'csv', 'datetime', 'json', 'bikeshare', 'container', 'visualizer'
        ]})
    print(sample_simulation())

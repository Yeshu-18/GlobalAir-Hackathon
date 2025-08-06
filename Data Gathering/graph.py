# graph.py

class Airport:
    """A class to represent an airport node with its attributes."""
    def __init__(self, iata, name, city, country, lat, lon):
        self.iata = iata
        self.name = name
        self.city = city
        self.country = country
        self.lat = lat
        self.lon = lon
    
    def __repr__(self):
        """String representation for debugging."""
        return f"Airport({self.iata} - {self.name})"

class Graph:
    """Represents the flight network using an adjacency list."""
    def __init__(self):
        self.adjacency_list = {}
        self.airports = {} # Maps IATA code to Airport object

    def add_node(self, airport):
        """Adds an airport node to the graph."""
        if airport.iata not in self.adjacency_list:
            self.adjacency_list[airport.iata] = []
            self.airports[airport.iata] = airport

    def add_edge(self, source_iata, dest_iata, weights):
        """Adds a directed edge with weights between two airports."""
        if source_iata in self.adjacency_list and dest_iata in self.adjacency_list:
            self.adjacency_list[source_iata].append((dest_iata, weights))

    def get_airport(self, iata):
        """Retrieves an Airport object by its IATA code."""
        return self.airports.get(iata)

    def __str__(self):
        """Returns a string summary of the graph."""
        num_routes = sum(len(v) for v in self.adjacency_list.values())
        return f"Flight Network Graph with {len(self.airports)} airports and {num_routes} routes."
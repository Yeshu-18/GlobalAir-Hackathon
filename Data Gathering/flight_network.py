# import csv
# import random
# from math import radians, sin, cos, sqrt, atan2
# from collections import Counter
# BUDGET_AIRLINES = {'FR', 'WN', '6E', 'U2', 'DY'} # Ryanair, Southwest, IndiGo, EasyJet, Norwegian
# DELAY_PRONE_AIRLINES = {'UA', 'AA', 'DL', 'B6'} # e.g., United, American, Delta, JetBlue


# def calculate_route_frequencies(routes_file):
#     """
#     Counts the occurrences of each route in the dataset.

#     Returns:
#         A Counter object mapping (source, dest) tuples to their frequency.
#     """
#     print("... Calculating route frequencies ...")
#     route_counts = Counter()
#     try:
#         with open(routes_file, 'r', encoding='utf-8') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 try:
#                     # Only count direct flights
#                     if row[7] == '0':
#                         route_counts[(row[2], row[4])] += 1
#                 except IndexError:
#                     continue
#     except FileNotFoundError:
#         print(f"Error: {routes_file} not found.")
#     print("✅ Frequencies calculated.")
#     return route_counts

# def calculate_haversine_distance(lat1, lon1, lat2, lon2):
#     """
#     Calculates the distance between two points on Earth using the Haversine formula.

#     Returns:
#         float: The distance in kilometers.
#     """
#     R = 6371.0  # Radius of Earth in kilometers

#     lat1_rad = radians(lat1)
#     lon1_rad = radians(lon1)
#     lat2_rad = radians(lat2)
#     lon2_rad = radians(lon2)

#     dlon = lon2_rad - lon1_rad
#     dlat = lat2_rad - lat1_rad

#     a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))

#     distance = R * c
#     return distance

# class Graph:
#     """
#     Represents a flight network graph using an adjacency list.

#     Time/Space Complexity:
#     - V: number of vertices (airports)
#     - E: number of edges (routes)
#     - Adjacency List Space: O(V + E)
#     """
#     def __init__(self):
#         """
#         Initializes the graph.
#         - adjacency_list: Maps an airport IATA to a list of its connections.
#         - airport_data: Maps an airport IATA to its detailed information.
#         """
#         self.adjacency_list = {}
#         self.airport_data = {}

#     def add_node(self, airport_id, name, city, country, iata, icao, lat, lon):
#         """
#         Adds an airport (node) to the graph.

#         Time Complexity: O(1) on average for dictionary insertion.
#         """
#         if iata not in self.adjacency_list:
#             self.adjacency_list[iata] = []
#             self.airport_data[iata] = {
#                 'id': airport_id,
#                 'name': name,
#                 'city': city,
#                 'country': country,
#                 'icao': icao,
#                 'latitude': lat,
#                 'longitude': lon
#             }

#     def add_edge(self, source_iata, dest_iata, weights):
#         """
#         Adds a directed flight route (edge) between two airports.

#         Time Complexity: O(1) on average for list append.
#         """
#         if source_iata in self.adjacency_list and dest_iata in self.adjacency_list:
#             self.adjacency_list[source_iata].append((dest_iata, weights))

#     def get_airport_details(self, iata):
#         """
#         Retrieves airport details by its IATA code.

#         Time Complexity: O(1) on average for dictionary lookup.
#         """
#         return self.airport_data.get(iata, None)

#     def __str__(self):
#         return f"Flight Network Graph with {len(self.adjacency_list)} airports and {sum(len(v) for v in self.adjacency_list.values())} routes."

# def build_flight_network(airports_file, routes_file):
#     """
#     Builds the flight network graph from OpenFlights data files.

#     Time Complexity: O(A + R), where A is airports and R is routes.
#     Space Complexity: O(A + R) to store the graph data.
#     """
#     flight_graph = Graph()
#     # --- New Pre-processing Step ---
#     route_frequencies = calculate_route_frequencies(routes_file)
#     # Define a threshold for a "frequent" route
#     frequent_route_threshold = 10 

#     # --- Step 1: Load Airports as Nodes ---
#     print("✈️  Loading airports...")
#     try:
#         with open(airports_file, 'r', encoding='utf-8') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 try:
#                     iata = row[4]
#                     if iata != '\\N' and len(iata) == 3:
#                         flight_graph.add_node(
#                             airport_id=row[0], name=row[1], city=row[2],
#                             country=row[3], iata=iata, icao=row[5],
#                             lat=float(row[6]), lon=float(row[7])
#                         )
#                 except (ValueError, IndexError):
#                     continue # Skip rows with malformed data
#     except FileNotFoundError:
#         print(f"Error: The file {airports_file} was not found.")
#         return None
#     print(f"✅ Loaded {len(flight_graph.adjacency_list)} airports.")

#     # --- Step 2: Load Routes with Advanced Cost Calculation ---
#     print("✈️  Loading routes...")
#     routes_loaded = 0
#     try:
#         with open(routes_file, 'r', encoding='utf-8') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 try:
#                     airline_code, source_iata, dest_iata, stops = row[1], row[2], row[4], row[7]

#                     if stops == '0':
#                         source_airport = flight_graph.get_airport_details(source_iata)
#                         dest_airport = flight_graph.get_airport_details(dest_iata)

#                         if source_airport and dest_airport:
#                             distance = calculate_haversine_distance(
#                                 source_airport['latitude'], source_airport['longitude'],
#                                 dest_airport['latitude'], dest_airport['longitude']
#                             )
                            
#                             # --- Advanced Cost Logic ---
#                             # 1. Start with a base cost
#                             base_cost = 50 + (distance * 0.12) # Slightly adjusted base rate

#                             # 2. Apply airline multiplier
#                             if airline_code in BUDGET_AIRLINES:
#                                 airline_multiplier = 0.8  # 20% discount for budget airlines
#                             else:
#                                 airline_multiplier = 1.15 # 15% surcharge for standard/legacy

#                             # 3. Apply frequency discount
#                             if route_frequencies.get((source_iata, dest_iata), 0) > frequent_route_threshold:
#                                 frequency_multiplier = 0.9 # 10% discount for frequent routes
#                             else:
#                                 frequency_multiplier = 1.0 # No discount

#                             # 4. Calculate final cost
#                             final_cost = base_cost * airline_multiplier * frequency_multiplier
                            
#                         # --- Intelligent Delay Simulation ---
#                         # 1. Check if the airline is in our delay-prone list
#                         if airline_code in DELAY_PRONE_AIRLINES:
#                             # Use a higher range for delay-prone airlines
#                             simulated_delay = random.randint(30, 120) # 30 to 120 minutes
#                         else:
#                             # Use a standard, lower range for other airlines
#                             simulated_delay = random.randint(5, 45) # 5 to 45 minutes

#                         # 2. Add all weights to the graph edge
#                         weights = {
#                             "distance": round(distance, 2),
#                             "cost": round(final_cost, 2),
#                             "delay": simulated_delay
#                         }
#                         flight_graph.add_edge(source_iata, dest_iata, weights)
#                         routes_loaded += 1

#                 except (ValueError, IndexError):
#                     continue
#     except FileNotFoundError:
#         print(f"Error: The file {routes_file} was not found.")
#         return None
#     print(f"✅ Loaded {routes_loaded} routes with advanced pricing.")
#     return flight_graph

# if __name__ == '__main__':
#     # Define the paths to your data files
#     AIRPORTS_FILE = 'airports.dat'
#     ROUTES_FILE = 'routes.dat'

#     # Build the graph
#     flight_network = build_flight_network(AIRPORTS_FILE, ROUTES_FILE)

#     if flight_network:
#         print("\n" + "="*40)
#         print(flight_network)
#         print("="*40 + "\n")

#         # --- Example Usage ---
#         # Let's inspect the flights from Chennai (MAA)
#         start_airport_iata = "MAA" 
#         print(f"🔍 Routes from {start_airport_iata} ({flight_network.get_airport_details(start_airport_iata)['name']}):")
        
#         if start_airport_iata in flight_network.adjacency_list:
#             connections = flight_network.adjacency_list[start_airport_iata]
#             if connections:
#                 for dest_iata, w in connections:
#                     dest_details = flight_network.get_airport_details(dest_iata)
#                     print(
#                         f"  -> To: {dest_iata} ({dest_details['name']})\n"
#                         f"     Weights: Distance: {w['distance']} km, "
#                         f"Est. Cost: ${w['cost']}, "
#                         f"Avg. Delay: {w['delay']} min"
#                     )
#             else:
#                 print(f"No outgoing routes found for {start_airport_iata}.")
#         else:
#             print(f"Airport {start_airport_iata} not found in the network.")






import csv
import random
from math import radians, sin, cos, sqrt, atan2
from collections import Counter

# --- Configuration ---
BUDGET_AIRLINES = {'FR', 'WN', '6E', 'U2', 'DY'} # Ryanair, Southwest, IndiGo, EasyJet, Norwegian
DELAY_PRONE_AIRLINES = {'UA', 'AA', 'DL', 'B6'} # e.g., United, American, Delta, JetBlue

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """Calculates distance between two points on Earth in kilometers."""
    R = 6371.0
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def calculate_route_frequencies(routes_file):
    """Pre-processes the routes file to count route frequencies."""
    print("... Calculating route frequencies ...")
    route_counts = Counter()
    try:
        with open(routes_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    if row[7] == '0':
                        route_counts[(row[2], row[4])] += 1
                except IndexError:
                    continue
    except FileNotFoundError:
        print(f"Error: {routes_file} not found.")
    print("✅ Frequencies calculated.")
    return route_counts

class Graph:
    """Represents the flight network using an adjacency list."""
    def __init__(self):
        self.adjacency_list = {}
        self.airport_data = {}

    def add_node(self, iata, name, city, country, lat, lon):
        if iata not in self.adjacency_list:
            self.adjacency_list[iata] = []
            self.airport_data[iata] = {'name': name, 'city': city, 'country': country, 'latitude': lat, 'longitude': lon}

    def add_edge(self, source_iata, dest_iata, weights):
        if source_iata in self.adjacency_list and dest_iata in self.adjacency_list:
            self.adjacency_list[source_iata].append((dest_iata, weights))

    def get_airport_details(self, iata):
        return self.airport_data.get(iata)

def build_flight_network(airports_file, routes_file):
    """Builds the flight network graph from source files."""
    flight_graph = Graph()
    route_frequencies = calculate_route_frequencies(routes_file)
    frequent_route_threshold = 10 

    print("✈️  Loading airports...")
    try:
        with open(airports_file, 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                try:
                    iata = row[4]
                    if iata != '\\N' and len(iata) == 3:
                        flight_graph.add_node(iata, row[1], row[2], row[3], float(row[6]), float(row[7]))
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        print(f"Error: {airports_file} not found."); return None
    print(f"✅ Loaded {len(flight_graph.adjacency_list)} airports.")

    print("✈️  Loading routes...")
    routes_loaded = 0
    try:
        with open(routes_file, 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                try:
                    airline_code, source_iata, dest_iata, stops = row[1], row[2], row[4], row[7]
                    if stops == '0':
                        source_airport = flight_graph.get_airport_details(source_iata)
                        dest_airport = flight_graph.get_airport_details(dest_iata)
                        if source_airport and dest_airport:
                            distance = calculate_haversine_distance(source_airport['latitude'], source_airport['longitude'], dest_airport['latitude'], dest_airport['longitude'])
                            
                            base_cost = 50 + (distance * 0.12)
                            airline_multiplier = 0.8 if airline_code in BUDGET_AIRLINES else 1.15
                            frequency_multiplier = 0.9 if route_frequencies.get((source_iata, dest_iata), 0) > frequent_route_threshold else 1.0
                            final_cost = base_cost * airline_multiplier * frequency_multiplier
                            
                            simulated_delay = random.randint(30, 120) if airline_code in DELAY_PRONE_AIRLINES else random.randint(0, 45)
                            
                            weights = {
                                "distance": round(distance, 2),
                                "cost": round(final_cost, 2),
                                "delay": simulated_delay
                            }
                            flight_graph.add_edge(source_iata, dest_iata, weights)
                            routes_loaded += 1
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        print(f"Error: {routes_file} was not found."); return None
    print(f"✅ Loaded {routes_loaded} routes.")
    return flight_graph

if __name__ == '__main__':
    flight_network = build_flight_network('airports.dat', 'routes.dat')
    if flight_network:
        # print(flight_network)
        print("\n🔍 Example: Flights from Chennai (MAA):")
        maa_flights = flight_network.adjacency_list.get("MAA", [])
        for dest, w in maa_flights[:]: # Show first 5 for brevity
            print(f"  -> To: {dest}, Weights: {w}")
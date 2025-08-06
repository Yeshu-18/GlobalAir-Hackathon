# data_loader.py

import csv
import random
from math import radians, sin, cos, sqrt, atan2
from collections import Counter
from graph import Graph, Airport
import config

def _calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """Calculates distance between two points on Earth in kilometers."""
    R = 6371.0
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def _calculate_route_frequencies():
    """Pre-processes the routes file to count route frequencies."""
    print("... Calculating route frequencies ...")
    route_counts = Counter()
    try:
        with open(config.ROUTES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    if row[7] == '0':
                        route_counts[(row[2], row[4])] += 1
                except IndexError:
                    continue
    except FileNotFoundError:
        print(f"Error: {config.ROUTES_FILE} not found.")
    print("✅ Frequencies calculated.")
    return route_counts

def build_flight_network():
    """Builds the flight network graph from source files using config settings."""
    flight_graph = Graph()
    route_frequencies = _calculate_route_frequencies()

    # Step 1: Load Airports
    print("✈️  Loading airports...")
    try:
        with open(config.AIRPORTS_FILE, 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                try:
                    iata, name, city, country = row[4], row[1], row[2], row[3]
                    lat, lon = float(row[6]), float(row[7])
                    if iata != '\\N' and len(iata) == 3:
                        flight_graph.add_node(Airport(iata, name, city, country, lat, lon))
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        print(f"Error: {config.AIRPORTS_FILE} not found."); return None
    print(f"✅ Loaded {len(flight_graph.airports)} airports.")

    # Step 2: Load Routes
    print("✈️  Loading routes...")
    routes_loaded = 0
    try:
        with open(config.ROUTES_FILE, 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                try:
                    airline_code, source_iata, dest_iata, stops = row[1], row[2], row[4], row[7]
                    if stops == '0':
                        source_airport = flight_graph.get_airport(source_iata)
                        dest_airport = flight_graph.get_airport(dest_iata)
                        if source_airport and dest_airport:
                            distance = _calculate_haversine_distance(source_airport.lat, source_airport.lon, dest_airport.lat, dest_airport.lon)
                            
                            base_cost = config.BASE_COST + (distance * config.COST_PER_KM)
                            airline_multiplier = config.BUDGET_AIRLINE_MULTIPLIER if airline_code in config.BUDGET_AIRLINES else config.STANDARD_AIRLINE_MULTIPLIER
                            frequency_multiplier = config.FREQUENCY_DISCOUNT_MULTIPLIER if route_frequencies.get((source_iata, dest_iata), 0) > config.FREQUENT_ROUTE_THRESHOLD else 1.0
                            final_cost = base_cost * airline_multiplier * frequency_multiplier
                            
                            delay_range = config.HIGH_DELAY_RANGE if airline_code in config.DELAY_PRONE_AIRLINES else config.LOW_DELAY_RANGE
                            simulated_delay = random.randint(*delay_range)
                            
                            weights = {"distance": round(distance, 2), "cost": round(final_cost, 2), "delay": simulated_delay}
                            flight_graph.add_edge(source_iata, dest_iata, weights)
                            routes_loaded += 1
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        print(f"Error: {config.ROUTES_FILE} was not found."); return None
    print(f"✅ Loaded {routes_loaded} routes.")
    return flight_graph
import sys


# Each node represents a location in the airport terminal.
# 'tags' will be used to match user interests.
# Using a dictionary for nodes allows for quick lookups by ID.
nodes = {
    0: {'name': 'Arrival Gate C25', 'type': 'gate', 'tags': {'gate'}},
    1: {'name': 'Departure Gate D12', 'type': 'gate', 'tags': {'gate'}},
    2: {'name': 'SATS Premier Lounge', 'type': 'lounge', 'tags': {'quiet', 'lounge', 'food'}},
    3: {'name': 'Starbucks', 'type': 'food', 'tags': {'coffee', 'food', 'quick'}},
    4: {'name': 'Gucci', 'type': 'shopping', 'tags': {'luxury', 'shopping'}},
    5: {'name': 'Terminal Skytrain Stop', 'type': 'transport', 'tags': {'transport'}},
    6: {'name': 'Food Court', 'type': 'food', 'tags': {'food', 'cheap', 'quick'}}
}

# Adjacency matrix representing direct travel times (in minutes) between nodes.
# We use a large number (infinity) for unconnected nodes.
INF = sys.maxsize
dist_matrix = [
    #      0(C25) 1(D12) 2(Lnge) 3(Star) 4(Gucci) 5(Train) 6(Food)
    [   0,    INF,     8,     5,    INF,      3,    INF], # 0: Gate C25
    [ INF,      0,   INF,   INF,      4,      2,    INF], # 1: Gate D12
    [   8,    INF,     0,     7,     15,    INF,      3], # 2: Lounge
    [   5,    INF,     7,     0,     12,      4,      2], # 3: Starbucks
    [ INF,      4,    15,    12,      0,      6,    INF], # 4: Gucci
    [   3,      2,   INF,     4,      6,      0,    INF], # 5: Skytrain
    [ INF,    INF,     3,     2,    INF,    INF,      0]  # 6: Food Court
]

# --------------------------------------------------------------------------
# Step 2: All-Pairs Shortest Path Calculation (Floyd-Warshall)
# --------------------------------------------------------------------------

def floyd_warshall(graph):
    """
    Calculates the shortest travel time between every pair of nodes.
    Returns a new matrix with these shortest times.
    """
    num_nodes = len(graph)
    # Create a copy to store the shortest path results to avoid modifying the original
    shortest_paths = [row[:] for row in graph]

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                # If the path from i to j through k is shorter than the current known path,
                # update the shortest path.
                if (shortest_paths[i][k] != INF and
                    shortest_paths[k][j] != INF and
                    shortest_paths[i][k] + shortest_paths[k][j] < shortest_paths[i][j]):
                    
                    shortest_paths[i][j] = shortest_paths[i][k] + shortest_paths[k][j]
    
    return shortest_paths

# --------------------------------------------------------------------------
# Step 3: Interest-Based Filtering
# --------------------------------------------------------------------------

def find_interesting_locations(nodes_data, user_interests):
    """
    Finds all locations that match the user's interests using set intersection.
    """
    matched_node_ids = []
    # Convert user interests to a set for efficient lookups (O(1) average time complexity)
    interest_set = set(user_interests)
    
    for node_id, data in nodes_data.items():
        # We don't consider gates as points of interest to visit
        if data['type'] == 'gate':
            continue
            
        # The intersection of two sets is non-empty if they share at least one element.
        if interest_set.intersection(data['tags']):
            matched_node_ids.append(node_id)
            
    return matched_node_ids

# --------------------------------------------------------------------------
# Step 4: Greedy Itinerary Builder
# --------------------------------------------------------------------------

def build_greedy_itinerary(
    arrival_gate_id,
    departure_gate_id,
    layover_time_mins,
    interesting_node_ids,
    shortest_paths_matrix,
    nodes_data,
    visit_duration=45, # Average time spent at one location (minutes)
    safety_buffer=40   # Time for security, boarding, etc. (minutes)
):
    """
    Constructs a layover itinerary using a greedy nearest-neighbor approach.
    """
    # The itinerary starts at the arrival gate.
    itinerary = [{'id': arrival_gate_id, 'travel_time': 0}]
    
    # Calculate the time actually available for activities.
    time_for_activities = layover_time_mins - safety_buffer
    
    current_location_id = arrival_gate_id
    unvisited_poi_ids = set(interesting_node_ids)

    while time_for_activities > 0 and unvisited_poi_ids:
        # Find the closest, unvisited, interesting location from the current spot.
        next_location_id = -1
        min_travel_time = INF
        
        for poi_id in unvisited_poi_ids:
            travel_time = shortest_paths_matrix[current_location_id][poi_id]
            if travel_time < min_travel_time:
                min_travel_time = travel_time
                next_location_id = poi_id

        # If no more reachable points of interest, break the loop.
        if next_location_id == -1:
            break

        # Check if we have enough time for this next step AND to get to the departure gate afterward.
        time_to_return_to_gate = shortest_paths_matrix[next_location_id][departure_gate_id]
        
        # Calculate total time needed for the potential next step in the journey.
        required_time = min_travel_time + visit_duration + time_to_return_to_gate
        
        if required_time <= time_for_activities:
            # If there is enough time, add the location to our itinerary.
            itinerary.append({'id': next_location_id, 'travel_time': min_travel_time})
            
            # Update our state: decrease available time, update current location, and mark POI as visited.
            time_for_activities -= (min_travel_time + visit_duration)
            current_location_id = next_location_id
            unvisited_poi_ids.remove(next_location_id)
        else:
            # Not enough time for any more stops, so we exit the loop.
            break
            
    # Always add the final leg of the journey to the departure gate.
    final_travel_time = shortest_paths_matrix[current_location_id][departure_gate_id]
    itinerary.append({'id': departure_gate_id, 'travel_time': final_travel_time})
    
    return itinerary

# --------------------------------------------------------------------------
# Step 5: Formatting and Main Execution
# --------------------------------------------------------------------------

def format_itinerary(itinerary, nodes_data, visit_duration, safety_buffer):
    """Prints the generated itinerary in a user-friendly format."""
    print("Personalized Layover Plan ")
    print("-" * 38)
    
    total_time_spent = 0
    
    # Print the starting point.
    start_node = nodes_data[itinerary[0]['id']]
    print(f"1. Arrive at: {start_node['name']}")
    
    # Iterate through the rest of the itinerary steps.
    for i, step in enumerate(itinerary[1:]):
        node_info = nodes_data[step['id']]
        travel_time = step.get('travel_time', 0)
        
        # Check if this step is a point of interest (not the final gate).
        is_poi = (i < len(itinerary) - 2)
        
        if is_poi:
            print(f"{i+2}. Walk to {node_info['name']} ({travel_time} mins).")
            print(f"   - Spend {visit_duration} mins here (type: {node_info['type']}).")
            total_time_spent += travel_time + visit_duration
        else: # This is the final step to the departure gate.
            print(f"{i+2}. Walk to {node_info['name']} ({travel_time} mins) for departure.")
            total_time_spent += travel_time

    print("-" * 38)
    print(f"Total activity and travel time: {total_time_spent} minutes.")
    print(f"Safety buffer for boarding: {safety_buffer} minutes.")
    print("Enjoy your layover!")


# This block ensures the code runs only when the script is executed directly.
if __name__ == "__main__":
    # --- SCENARIO DEFINITION ---
    layover_hours = 6
    passenger_interests = ['lounge', 'food', 'quick']
    arrival_gate_id = 0  # Corresponds to 'Arrival Gate C25' in our nodes dictionary
    departure_gate_id = 1 # Corresponds to 'Departure Gate D12'
    
    # --- EXECUTION LOGIC ---
    
    # 1. Convert layover to minutes.
    layover_minutes = layover_hours * 60

    # 2. Pre-compute all-pairs shortest paths using Floyd-Warshall.
    #    In a real application, this would be done once and cached.
    all_pairs_shortest_paths = floyd_warshall(dist_matrix)

    # 3. Find all locations that match the passenger's interests.
    interesting_places_ids = find_interesting_locations(nodes, passenger_interests)
    print(f"System: Found potential locations based on interests: {interesting_places_ids}\n")

    # 4. Build the greedy itinerary with the specified parameters.
    #    These parameters could be adjusted based on user input.
    visit_duration_per_stop = 45
    boarding_safety_buffer = 40
    
    final_itinerary = build_greedy_itinerary(
        arrival_gate_id=arrival_gate_id,
        departure_gate_id=departure_gate_id,
        layover_time_mins=layover_minutes,
        interesting_node_ids=interesting_places_ids,
        shortest_paths_matrix=all_pairs_shortest_paths,
        nodes_data=nodes,
        visit_duration=visit_duration_per_stop,
        safety_buffer=boarding_safety_buffer
    )
    
    # 5. Present the final plan to the user in a readable format.
    format_itinerary(final_itinerary, nodes, visit_duration_per_stop, boarding_safety_buffer)

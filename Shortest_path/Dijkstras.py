import heapq

adj = {
    'Chennai': {'Dubai': {'cost': 750, 'time': 4}, 'Singapore': {'cost': 400, 'time': 5}},
    'Dubai': {'New York': {'cost': 1200, 'time': 14}, 'London': {'cost': 800, 'time': 8}},
    'Singapore': {'Tokyo': {'cost': 500, 'time': 7}, 'San Francisco': {'cost': 1100, 'time': 16}},
    'London': {'New York': {'cost': 300, 'time': 8}},
    'New York': {'San Francisco': {'cost': 250, 'time': 6}},
    'Tokyo': {'San Francisco': {'cost': 600, 'time': 9}},
    'San Francisco': {}
}

# This helper function reads the 'predecessors' map to build the path
from collections import deque

def get_path(predecessors, start_node, end_node):
    # 1. Create a new path object inside the function.
    path = deque()
    current_node = end_node

    # 2. Loop until you trace back to the very beginning.
    while current_node is not None:
        path.appendleft(current_node)
        current_node = predecessors.get(current_node)

    # 3. Verify the path is valid and return it.
    if path and path[0] == start_node:
        return list(path)
    else:
        return None

def dijkstra(start, end, param):
    heap = []
    heapq.heappush(heap, (0, start))
        
    # Dictionary to store the minimum value to reach each node
    min_values = {node: float('inf') for node in adj}
    min_values[start] = 0
    
    # Dictionary to store the path (the "breadcrumbs")
    predecessors = {node: None for node in adj}
    
    while heap:
        curr_value, current_node = heapq.heappop(heap)
        
        # Optimization: if we've already found a better path, skip
        if curr_value > min_values[current_node]:
            continue

        # When we reach the end, we can stop and return the results
        if current_node == end:
            path = get_path(predecessors, start, end)
            return min_values[end], path

        for neighbor, weights in adj[current_node].items():
            new_value = curr_value + weights[param]
            if new_value < min_values[neighbor]:
                min_values[neighbor] = new_value
                # Add a breadcrumb pointing back to the current node
                predecessors[neighbor] = current_node
                heapq.heappush(heap, (new_value, neighbor))
                
    # This will be reached if the end node is unreachable
    return None, None

# --- Main Program ---
start_node = input("Enter the starting airport: ")
end_node = input("Enter the destination airport: ")
param = input("Enter the parameter to optimize (cost/time): ")

if start_node in adj and end_node in adj and param in ['cost', 'time']:
    value, path = dijkstra(start_node, end_node, param) 
    
    print("\n--- Results ---")
    if value is not None and path is not None:
        print(f"The minimum {param} from {start_node} to {end_node} is: {value}")
        print(f"Path: {' -> '.join(path)}")
    else:
        print(f"No path found from {start_node} to {end_node}.")
else:
    print("Invalid input. Please check airport names and parameter (cost/time).")
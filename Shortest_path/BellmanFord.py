def bellman_ford(graph, start_node):
    """
    Finds the shortest paths from a start node using the Bellman-Ford algorithm.

    Args:
        graph (dict): A graph where keys are nodes and values are dictionaries
                      of {neighbor: weight}.
        start_node (str): The starting node.

    Returns:
        A tuple (distances, predecessors). Returns (None, None) if a
        negative-weight cycle is detected.
    """
    num_vertices = len(graph)
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[start_node] = 0

    # 1. Relax all edges V-1 times
    for _ in range(num_vertices - 1):
        for u in graph:
            for v, weight in graph[u].items():
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u

    # 2. Check for negative-weight cycles
    for u in graph:
        for v, weight in graph[u].items():
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                print("Error: Graph contains a negative-weight cycle.")
                return None, None

    return distances, predecessors

def get_path(predecessors, start_node, end_node):
    """Constructs the path from the predecessors dictionary."""
    path = []
    current_node = end_node
    while current_node is not None:
        path.insert(0, current_node)
        current_node = predecessors.get(current_node)

    if path and path[0] == start_node:
        return path
    return None

# --- Example Usage ---
if __name__ == "__main__":
    # Graph with a penalty/rebate (negative weight)
    travel_graph_negative = {
        'Chennai': {'Dubai': 400},
        'Dubai': {'New York': 800},
        'New York': {'San Francisco': 300, 'London': -100},  # Rebate route
        'London': {'Dubai': 700},
        'San Francisco': {}
    }

    start_city = 'Chennai'
    end_city = 'San Francisco'

    print(f"--- Bellman-Ford Algorithm 📉 ---")
    distances, predecessors = bellman_ford(travel_graph_negative, start_city)

    if distances:
        path = get_path(predecessors, start_city, end_city)
        if path:
            print(f"Shortest cost from {start_city} to {end_city}: ${distances[end_city]}")
            print(f"Path: {' -> '.join(path)}")
        else:
            print(f"No path found from {start_city} to {end_city}.")

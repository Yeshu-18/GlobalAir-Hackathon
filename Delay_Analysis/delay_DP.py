import collections
from datetime import datetime

def generate_sample_data():
    """Generates a sample list of flight records for demonstration."""
    return [
        # A simple chain: JFK -> ORD -> SFO with accumulating delays
        {'origin': 'JFK', 'destination': 'ORD', 'date': '2024-01-10', 'delay_minutes': 30},
        {'origin': 'ORD', 'destination': 'SFO', 'date': '2024-01-10', 'delay_minutes': 60},
        {'origin': 'SFO', 'destination': 'HNL', 'date': '2024-01-10', 'delay_minutes': 90}, 
        {'origin': 'HNL', 'destination': 'SYD', 'date': '2024-01-11', 'delay_minutes': 50},

        # Another chain for January, starting from LAX
        {'origin': 'LAX', 'destination': 'DEN', 'date': '2024-01-20', 'delay_minutes': 20},
        {'origin': 'DEN', 'destination': 'ATL', 'date': '2024-01-20', 'delay_minutes': 40},

        # Some flights in July to show time-of-year analysis
        {'origin': 'JFK', 'destination': 'MIA', 'date': '2024-07-05', 'delay_minutes': 120}, 
        {'origin': 'ORD', 'destination': 'MIA', 'date': '2024-07-06', 'delay_minutes': 75},

        # A flight that doesn't lead to a long chain
        {'origin': 'ATL', 'destination': 'MCO', 'date': '2024-03-15', 'delay_minutes': 10},
    ]

# --- Part 1: Most Delay-Prone Airports by Time of Year ---

def analyze_airport_delays(flight_data):
    """
    Finds the most delay-prone airports by month by aggregating delay data.
    """
    # Cache to store: (airport, month) -> [total_delay, flight_count]
    delay_cache = collections.defaultdict(lambda: [0, 0])

    for flight in flight_data:
        if flight['delay_minutes'] > 0:
            airport = flight['origin']
            month = datetime.strptime(flight['date'], '%Y-%m-%d').month
            
            delay_cache[(airport, month)][0] += flight['delay_minutes']
            delay_cache[(airport, month)][1] += 1
            
    # Calculate average delays
    avg_delays = {
        key: total_delay / count
        for key, (total_delay, count) in delay_cache.items()
    }

    # Sort by average delay in descending order
    return sorted(avg_delays.items(), key=lambda item: item[1], reverse=True)

# --- Part 2: Longest Delay Chains (Dynamic Programming) ---

def find_longest_delay_chain(flight_data):
    """
    Main function to find the longest multi-hop delay chain using DP.
    """
    graph = collections.defaultdict(list)
    airports = set()
    for flight in flight_data:
        graph[flight['origin']].append((flight['destination'], flight['delay_minutes']))
        airports.add(flight['origin'])
        airports.add(flight['destination'])

    # Memoization cache: airport -> (max_delay, next_hop)
    memo = {}
    
    for airport in list(airports):
        if airport not in memo:
            _dfs_delay_chain(airport, graph, memo)

    if not memo:
        return 0, []

    # Find the starting point of the overall longest chain from the cache
    start_of_best_chain = max(memo, key=lambda airport: memo[airport][0])
    
    # Reconstruct the chain from the memoization cache
    path = []
    total_delay = memo[start_of_best_chain][0]
    current_node = start_of_best_chain
    while current_node is not None:
        path.append(current_node)
        current_node = memo[current_node][1] # Follow the breadcrumbs
        
    return total_delay, path

def _dfs_delay_chain(airport, graph, memo):
    """
    Recursive DFS helper with memoization to solve the subproblems.
    """
    if airport in memo:
        return memo[airport]

    max_delay = 0
    best_next_hop = None

    for destination, delay in graph.get(airport, []):
        downstream_delay, _ = _dfs_delay_chain(destination, graph, memo)
        current_total_delay = delay + downstream_delay
        
        if current_total_delay > max_delay:
            max_delay = current_total_delay
            best_next_hop = destination
            
    # Memoize the result before returning
    memo[airport] = (max_delay, best_next_hop)
    return max_delay, best_next_hop

# --- Main Execution ---
if __name__ == "__main__":
    flights = generate_sample_data()
    
    print("✈️  Historical Delay Analysis Results")
    print("="*40)
    
    # Run Part 1
    airport_delays = analyze_airport_delays(flights)
    print("\n Most Delay-Prone Airports (by Month):")
    print("(Airport, Month) -> Average Delay (minutes)")
    for (airport, month), avg_delay in airport_delays[:5]: # Print top 5
        print(f"({airport}, {month:02d}) ---------> {avg_delay:.0f} min")
        
    print("\n" + "="*40)

    # Run Part 2
    total_delay, path = find_longest_delay_chain(flights)
    print("\n🔗 Longest Delay Chain (Multi-hop):")
    print(f"Maximum Cumulative Delay: {total_delay} minutes")
    print(f"Path: {' -> '.join(path)}")

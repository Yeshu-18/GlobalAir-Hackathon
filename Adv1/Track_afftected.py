import random
from collections import deque

class BaggageTracker:
    """
    Manages baggage dependencies as a graph to track downstream effects of a lost bag.
    """

    def __init__(self):
        """
        Initializes the baggage tracker with an empty graph and passenger list.
        The graph is represented as an adjacency list (dictionary).
        """
        self.graph = {}
        self.passengers = {}

    def add_dependency(self, source_bag_id: str, dependent_bag_id: str):
        """
        Adds a directed edge from a source bag to a dependent bag.
        This signifies that the dependent bag's journey is affected by the source bag.

        Args:
            source_bag_id (str): The ID of the source bag.
            dependent_bag_id (str): The ID of the bag that depends on the source.
        """
        if not source_bag_id or not dependent_bag_id or source_bag_id == dependent_bag_id:
            print("Error: Please provide valid and distinct bag IDs.")
            return

        # Add nodes to the graph if they don't exist
        self.graph.setdefault(source_bag_id, []).append(dependent_bag_id)
        self.graph.setdefault(dependent_bag_id, [])

        # Assign a random passenger ID if the bag is new
        self.passengers.setdefault(source_bag_id, f"PAX-{random.randint(1000, 9999)}")
        self.passengers.setdefault(dependent_bag_id, f"PAX-{random.randint(1000, 9999)}")
        
        print(f"Added dependency: {source_bag_id} -> {dependent_bag_id}")

    def bfs(self, start_node: str) -> list:
        """
        Performs a Breadth-First Search (BFS) from a starting node.
        Explores the graph layer by layer.

        Args:
            start_node (str): The ID of the lost bag to start the traversal from.

        Returns:
            list: A list of all affected bag IDs, including the start node.
        """
        if start_node not in self.graph:
            return []
            
        queue = deque([start_node])
        visited = {start_node}
        result = [start_node]

        while queue:
            node = queue.popleft()
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    result.append(neighbor)
        return result

    def dfs(self, start_node: str) -> list:
        """
        Performs a Depth-First Search (DFS) from a starting node.
        Explores as far as possible along each branch before backtracking.

        Args:
            start_node (str): The ID of the lost bag to start the traversal from.

        Returns:
            list: A list of all affected bag IDs.
        """
        if start_node not in self.graph:
            return []

        visited = set()
        result = []
        
        def _dfs_util(node):
            visited.add(node)
            result.append(node)
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    _dfs_util(neighbor)

        _dfs_util(start_node)
        return result

    def detect_cycle(self) -> tuple:
        """
        Detects cycles in the graph using a modified DFS traversal.
        This is crucial for identifying impossible routing loops.

        Returns:
            tuple: A tuple containing a boolean (True if cycle detected) and the path of the cycle.
        """
        visited = set()
        recursion_stack = set()
        all_nodes = list(self.graph.keys())

        for node in all_nodes:
            if node not in visited:
                # The path is passed as a list to be mutable across recursive calls
                path, has_cycle = self._detect_cycle_util(node, visited, recursion_stack, [])
                if has_cycle:
                    # Trim the path to show only the cycle itself
                    cycle_start_index = path.index(path[-1])
                    return True, path[cycle_start_index:]
        return False, []

    def _detect_cycle_util(self, node, visited, recursion_stack, path):
        visited.add(node)
        recursion_stack.add(node)
        path.append(node)

        for neighbor in self.graph.get(node, []):
            if neighbor not in visited:
                # If a cycle is found in a deeper call, propagate the result up
                found_path, has_cycle = self._detect_cycle_util(neighbor, visited, recursion_stack, path)
                if has_cycle:
                    return found_path, True
            elif neighbor in recursion_stack:
                # Cycle detected
                path.append(neighbor)
                return path, True
        
        # Backtrack
        recursion_stack.remove(node)
        path.pop()
        return path, False

    def display_results(self, lost_bag: str, affected_bags: list):
        """Prints the tracking results in a user-friendly format."""
        print("\n--- Tracking Results ---")
        print(f"Lost Bag: {lost_bag} (Passenger: {self.passengers.get(lost_bag, 'N/A')})")
        print(f"Found {len(affected_bags) - 1} downstream dependencies.")
        print("\nAffected Passengers and Bags:")
        if not affected_bags:
            print("  No bags found.")
            return
        
        for bag_id in affected_bags:
            passenger_id = self.passengers.get(bag_id, "N/A")
            prefix = "  (Lost Bag)" if bag_id == lost_bag else "  (Affected)"
            print(f"{prefix:<12} Bag ID: {bag_id:<10} | Passenger: {passenger_id}")
        print("------------------------\n")


if __name__ == "__main__":
    # --- Simulation Setup ---
    tracker = BaggageTracker()

    # Scenario: A complex interline transfer
    # LHR -> JFK -> SFO -> HNL
    tracker.add_dependency("BAG-LHR-001", "BAG-JFK-002") # Interline transfer
    tracker.add_dependency("BAG-JFK-002", "BAG-SFO-003") # Another transfer
    tracker.add_dependency("BAG-SFO-003", "BAG-HNL-004") # Final leg

    # A separate passenger's journey
    tracker.add_dependency("BAG-CDG-111", "BAG-DXB-222")

    # A passenger with two bags on the same flight as BAG-JFK-002
    tracker.add_dependency("BAG-JFK-002", "BAG-JFK-005") # Shared container/flight
    tracker.add_dependency("BAG-JFK-005", "BAG-SFO-006") # This bag also transfers

    print("\nInitial Baggage Dependency Graph:")
    for source, dependents in tracker.graph.items():
        print(f"  {source} -> {dependents}")
    print("-" * 20)

    # --- Cycle Detection ---
    has_cycle, cycle_path = tracker.detect_cycle()
    if has_cycle:
        print(f"\n WARNING: Cycle Detected! Path: {' -> '.join(cycle_path)}")
    else:
        print("\n No cycles detected in the graph.")

    # --- Tracking Simulation ---
    LOST_BAG_ID = "BAG-JFK-002"

    # 1. Track with BFS
    print("\n--- Running Tracker with BFS ---")
    affected_with_bfs = tracker.bfs(LOST_BAG_ID)
    tracker.display_results(LOST_BAG_ID, affected_with_bfs)

    # 2. Track with DFS
    print("--- Running Tracker with DFS ---")
    affected_with_dfs = tracker.dfs(LOST_BAG_ID)
    tracker.display_results(LOST_BAG_ID, affected_with_dfs)
    
    # --- Example of adding a cycle for demonstration ---
    print("\n--- Adding a dependency that creates a cycle ---")
    tracker.add_dependency("BAG-HNL-004", "BAG-LHR-001") # This creates a loop
    has_cycle, cycle_path = tracker.detect_cycle()
    if has_cycle:
        print(f"\n WARNING: Cycle Detected! Path: {' -> '.join(cycle_path)}")


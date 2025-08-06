import heapq

# --- Data-holding class is unchanged ---
class Baggage:
    def __init__(self, baggage_id, destination, passenger_priority, security_risk_level):
        self.baggage_id = baggage_id
        self.destination = destination
        self.passenger_priority = passenger_priority
        self.security_risk_level = security_risk_level

    def __repr__(self):
        return (f"Baggage(ID: {self.baggage_id}, Dest: {self.destination}, "
                f"Priority: {self.passenger_priority}, Risk: {self.security_risk_level})")

# --- AVL Tree Implementation (Replaces BST) ---
class AVLNode:
    """A node in a self-balancing AVL Tree."""
    def __init__(self, baggage):
        self.key = baggage.baggage_id
        self.data = baggage
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    """A self-balancing AVL Tree to guarantee O(log n) performance."""

    def getHeight(self, node):
        return node.height if node else 0

    def getBalance(self, node):
        return self.getHeight(node.left) - self.getHeight(node.right) if node else 0

    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def insert(self, baggage):
        """Public method to insert a new baggage item."""
        if not hasattr(self, 'root'):
            self.root = None
        self.root = self._insert_recursive(self.root, baggage)

    def _insert_recursive(self, node, baggage):
        # 1. Standard BST insertion
        if not node:
            return AVLNode(baggage)
        elif baggage.baggage_id < node.key:
            node.left = self._insert_recursive(node.left, baggage)
        else:
            node.right = self._insert_recursive(node.right, baggage)

        # 2. Update height and get balance factor
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        balance = self.getBalance(node)

        # 3. Rebalance the tree if needed
        # Left Left Case
        if balance > 1 and baggage.baggage_id < node.left.key:
            return self.rightRotate(node)
        # Right Right Case
        if balance < -1 and baggage.baggage_id > node.right.key:
            return self.leftRotate(node)
        # Left Right Case
        if balance > 1 and baggage.baggage_id > node.left.key:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)
        # Right Left Case
        if balance < -1 and baggage.baggage_id < node.right.key:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)
        
        return node

    def search(self, baggage_id):
        return self._search_recursive(self.root, baggage_id)

    def _search_recursive(self, current_node, baggage_id):
        if not current_node or current_node.key == baggage_id:
            return current_node.data if current_node else None
        if baggage_id < current_node.key:
            return self._search_recursive(current_node.left, baggage_id)
        else:
            return self._search_recursive(current_node.right, baggage_id)

# --- Main System (integrates the new AVL Tree) ---
class BaggageFlowSystem:
    def __init__(self):
        # The ONLY change needed here is swapping the tree type
        self.baggage_catalog = AVLTree()
        self.priority_queue = []

    def add_baggage(self, baggage_id, destination, passenger_priority, security_risk_level):
        new_bag = Baggage(baggage_id, destination, passenger_priority, security_risk_level)
        self.baggage_catalog.insert(new_bag)
        print(f"Cataloged: {new_bag}")

        heapq.heappush(self.priority_queue, (-new_bag.passenger_priority, new_bag.security_risk_level, new_bag.baggage_id, new_bag))
        print(f"    -> Added to loading queue.")

    def load_next_bag(self):
        if not self.priority_queue:
            print("\n🛑 No more baggage to load.")
            return None
        _, _, _, next_bag = heapq.heappop(self.priority_queue)
        print(f"\nLoading next bag onto plane -> {next_bag}")
        return next_bag

# --- Example Usage ---
if __name__ == "__main__":
    system = BaggageFlowSystem()
    print("--- Adding Baggage to the System (Using AVL Tree) ---")
    
    # Adding baggage in sorted order to show the AVL tree's strength
    print("\nAdding bags with sequential IDs (worst-case for BST):")
    system.add_baggage(100, "JFK", 3, 1)
    system.add_baggage(200, "LHR", 1, 1)
    system.add_baggage(300, "SFO", 2, 1)
    system.add_baggage(400, "DXB", 1, 3)
    system.add_baggage(500, "NRT", 3, 2)

    print("\n--- Loading Baggage onto Plane ---")
    while len(system.priority_queue) > 0:
        system.load_next_bag()

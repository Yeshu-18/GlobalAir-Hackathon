import datetime

class BaggageNode:
    """
    Represents a single checkpoint scan for a piece of baggage.
    This acts as a node in our doubly linked list.
    """
    def __init__(self, baggage_id, checkpoint, metadata=None):
        self.baggage_id = baggage_id
        self.checkpoint = checkpoint
        self.timestamp = datetime.datetime.now()
        self.metadata = metadata if metadata is not None else {}
        self.prev = None  # Pointer to the previous BaggageNode
        self.next = None  # Pointer to the next BaggageNode

    def __repr__(self):
        """String representation for easy printing."""
        return (f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"ID: {self.baggage_id}, Checkpoint: {self.checkpoint}")

class BaggageTracker:
    """
    A system to track baggage using a hash table and doubly linked lists.
    """
    def __init__(self):
        """
        Initializes the tracker.
        The baggage_map is our hash table that maps a baggage_id
        to the *most recent* BaggageNode for that bag.
        """
        self.baggage_map = {} # Key: baggage_id, Value: latest BaggageNode

    def add_scan(self, baggage_id, checkpoint, metadata=None):
        # Ensure metadata is a dictionary
        new_metadata = metadata if metadata is not None else {}
        
        # If the bag already exists, merge its old metadata with the new
        if baggage_id in self.baggage_map:
            existing_metadata = self.baggage_map[baggage_id].metadata
            # Unpack both dictionaries into a new one
            final_metadata = {**existing_metadata, **new_metadata}
        else:
            final_metadata = new_metadata
            
        # Create the new node with the final, merged metadata
        new_node = BaggageNode(baggage_id, checkpoint, final_metadata)
        

        if baggage_id in self.baggage_map:
            # If the bag is already in the system, link the new node
            # to the existing chain.
            last_node = self.baggage_map[baggage_id]
            last_node.next = new_node
            new_node.prev = last_node
        
        # Update the map to point to the new node as the latest scan.
        self.baggage_map[baggage_id] = new_node

    def get_last_known_location(self, baggage_id):
        """
        Returns the last known location and metadata of a bag in O(1) time.
        
        Args:
            baggage_id (str): The unique ID of the bag.
            
        Returns:
            The last BaggageNode if found, otherwise None.
        """
        if baggage_id not in self.baggage_map:
            print(f"INFO: Bag {baggage_id} not found in the system.")
            return None
            
        return self.baggage_map.get(baggage_id)

    def trace_baggage_history(self, baggage_id):
        """
        Traces and returns the full history of a bag's journey.
        
        Args:
            baggage_id (str): The unique ID of the bag.
            
        Returns:
            A list of all BaggageNodes in chronological order.
        """
        if baggage_id not in self.baggage_map:
            print(f"INFO: Cannot trace bag {baggage_id}. Not found.")
            return []
        
        print(f"\n--- Tracing History for Bag {baggage_id} ---")
        
        # Start from the most recent node (the tail of the list)
        current_node = self.baggage_map.get(baggage_id)
        history = []
        
        # Traverse backwards using the 'prev' pointers to get the full history
        while current_node:
            history.append(current_node)
            current_node = current_node.prev
            
        # The history is now in reverse-chronological order, so we reverse it.
        return list(reversed(history))

    def delete_bag(self, baggage_id):
        """
        Deletes a bag and its entire history from the system. O(1) operation.
        The linked list nodes will be garbage collected by Python once the
        reference in the hash map is removed.
        
        Args:
            baggage_id (str): The unique ID of the bag to delete.
        """
        if baggage_id in self.baggage_map:
            del self.baggage_map[baggage_id]
            print(f"\nDELETE: Bag {baggage_id} and its history have been removed.")
        else:
            print(f"INFO: Cannot delete bag {baggage_id}. Not found.")

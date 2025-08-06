from baggage_tracker import BaggageTracker

if __name__ == "__main__":
    # 1. Initialize the baggage tracking system
    tracker = BaggageTracker()
    print("Baggage Tracking System Initialized.\n")

    # 2. Add scans for a few bags
    tracker.add_scan("BAG-UA-123", "Check-in", {"owner": "John Doe", "flight": "UA 45"})
    tracker.add_scan("BAG-DL-456", "Check-in", {"owner": "Jane Smith", "flight": "DL 88"})
    tracker.add_scan("BAG-UA-123", "Security", {"status": "Cleared"})
    tracker.add_scan("BAG-UA-123", "Gate A5", {"status": "Boarding"})
    tracker.add_scan("BAG-DL-456", "Security", {"status": "Cleared"})
    
    print("\n----------------------------------------\n")

    # 3. Get the last known location of a bag (O(1) operation)
    print("--- Getting Last Known Location ---")
    bag_id_to_find = "BAG-UA-123"
    last_location = tracker.get_last_known_location(bag_id_to_find)
    if last_location:
        print(f"Last location for {bag_id_to_find}: '{last_location.checkpoint}'")
        print(f"Metadata: {last_location.metadata}")

    print("\n----------------------------------------\n")

    # 4. Trace the full history of a bag
    history = tracker.trace_baggage_history("BAG-DL-456")
    for scan in history:
        print(scan)

    # 5. Delete a bag from the system (O(1) operation)
    tracker.delete_bag("BAG-DL-456")
    
    # 6. Try to find the deleted bag
    print("\n--- Verifying Deletion ---")
    deleted_bag_location = tracker.get_last_known_location("BAG-DL-456")
    if not deleted_bag_location:
        print("Verification successful. Bag BAG-DL-456 is no longer tracked.")
# main.py
from data_loader import build_flight_network

def main():
    """Main function to run the GlobalAir application."""
    print("--- ✈️  Starting GlobalAir Logistics System ---")
    
    flight_network = build_flight_network()

    if flight_network:
        print("\n" + "="*50)
        print(flight_network)
        print("="*50 + "\n")

        # --- Example Usage ---
        start_airport_iata = "MAA" 
        start_airport = flight_network.get_airport(start_airport_iata)
        
        if start_airport:
            print(f"🔍 Routes from {start_airport.iata} ({start_airport.name}):")
            connections = flight_network.adjacency_list.get(start_airport_iata, [])
            if connections:
                for dest_iata, w in connections[:5]: # Show first 5 for brevity
                    dest_airport = flight_network.get_airport(dest_iata)
                    print(
                        f"  -> To: {dest_airport.iata} ({dest_airport.name})\n"
                        f"     Weights: Distance: {w['distance']} km, "
                        f"Est. Cost: ${w['cost']}, "
                        f"Avg. Delay: {w['delay']} min"
                    )
            else:
                print(f"No outgoing routes found for {start_airport_iata}.")
        else:
            print(f"Airport {start_airport_iata} not found in the network.")

if __name__ == '__main__':
    main()
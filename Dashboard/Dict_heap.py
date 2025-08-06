import time
import os
import random
import heapq

def clear_screen():
    """Clears the terminal screen for Windows, macOS, and Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Runs the main dashboard application."""
    # --- Data Storage (Master Data) ---
    # In a real system, this data would be in a database or a shared cache.
    route_delays = {
        "SFO-JFK": 70, "LAX-ORD": 45, "ATL-MIA": 15,
        "DEN-DFW": 30, "JFK-LHR": 85, "ORD-SFO": 22,
        "MIA-JFK": 55, "DFW-LAX": 40,
    }

    baggage_jams = {
        "T2-Claim4": 3, "T1-Claim1": 5, "T4-Claim8": 2,
        "T3-Claim2": 8, "TInternational-A": 4,
    }

    flights_at_risk = {
        "UA456": 25, "DL123": 35, "AA789": 20,
        "BA286": 22, "LH491": 30, "EK202": 40,
    }

    print("Starting Airport Dashboard... (Press Ctrl+C to stop)")
    time.sleep(2)

    # --- Main Dashboard Loop ---
    while True:
        try:
            clear_screen()
            print("✈️  Airport System Monitoring Dashboard")
            print(f"   Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("===================================================")

            # --- 1. Top 5 Delay-Prone Routes ---
            # Use heapq.nlargest to efficiently find the top 5 routes by delay.
            # It's much faster than sorting the whole dictionary.
            top_routes = heapq.nlargest(5, route_delays.items(), key=lambda item: item[1])
            
            print("\n--- Top 5 Delay-Prone Routes ---")
            for i, (route, delay) in enumerate(top_routes, 1):
                print(f"{i}. Route: {route:<10} | Delay: {delay} mins")

            # --- 2. Top 5 Baggage Jams ---
            top_jams = heapq.nlargest(5, baggage_jams.items(), key=lambda item: item[1])
            
            print("\n--- Top 5 Baggage Jams ---")
            for i, (area, count) in enumerate(top_jams, 1):
                print(f"{i}. Area: {area:<15} | Jam Count: {count}")
            
            # --- 3. Top 5 Flights at Risk ---
            # Use heapq.nsmallest to find flights with the shortest connection times.
            top_risk_flights = heapq.nsmallest(5, flights_at_risk.items(), key=lambda item: item[1])

            print("\n--- Top 5 Flights at Risk (by Connection Time) ---")
            for i, (flight, conn_time) in enumerate(top_risk_flights, 1):
                print(f"{i}. Flight: {flight:<10} | Connection: {conn_time} mins")

            print("\n===================================================")
            print("Simulating new data... (System is live)")

            # --- Simulate new data arriving randomly ---
            random_route = random.choice(list(route_delays.keys()))
            route_delays[random_route] += random.randint(1, 10)
            
            random_jam_area = random.choice(list(baggage_jams.keys()))
            baggage_jams[random_jam_area] += 1

            # Sleep for 3 seconds before the next refresh
            time.sleep(3)

        except KeyboardInterrupt:
            print("\n\nDashboard stopped by user. Goodbye!")
            break

if __name__ == "__main__":
    main()

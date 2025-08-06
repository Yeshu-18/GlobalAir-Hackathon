# --- File Paths ---
AIRPORTS_FILE = 'airports.dat'
ROUTES_FILE = 'routes.dat'

# --- Airline Lists for Simulation ---
BUDGET_AIRLINES = {'FR', 'WN', '6E', 'U2', 'DY'} # Ryanair, Southwest, IndiGo, EasyJet, Norwegian
DELAY_PRONE_AIRLINES = {'UA', 'AA', 'DL', 'B6'} # United, American, Delta, JetBlue

# --- Cost Model Parameters ---
BASE_COST = 50.0
COST_PER_KM = 0.12
BUDGET_AIRLINE_MULTIPLIER = 0.8
STANDARD_AIRLINE_MULTIPLIER = 1.15
FREQUENCY_DISCOUNT_MULTIPLIER = 0.9
FREQUENT_ROUTE_THRESHOLD = 10

# --- Delay Model Parameters ---
HIGH_DELAY_RANGE = (30, 120)
LOW_DELAY_RANGE = (5, 45)

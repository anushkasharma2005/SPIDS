"""
Configuration Template for Inflation Simulation
================================================
Copy this file to 'config.py' and modify it to customize your simulation.

USAGE:
1. Copy this file: cp config_template.py config.py
2. Edit config.py with your desired parameters
3. Run the simulation: python main.py

The main code will automatically read your settings from config.py
"""


# ============================================================================
# POTENTIAL SELECTION
# ============================================================================
POTENTIAL_TYPE = "quadratic"  # Options: "quadratic", "starobinsky", "hilltop", "natural"

# ============================================================================
# POTENTIAL PARAMETERS (Modify based on your choice above)
# ============================================================================
# You can also use lists here, e.g., {'m': [0.01, 0.02]}

# Quadratic Potential: V = (1/2) * m^2 * phi^2
QUADRATIC_PARAMS = {'m': 0.1}

# Starobinsky Potential: V = V0 * (1 - exp(-sqrt(2/3) * phi))^2
STAROBINSKY_PARAMS = {'V0': 1e-10}

# Hilltop Potential: V = V0 * (1 - (phi/mu)^p)
HILLTOP_PARAMS = {'V0': 1e-10, 'mu': 1.0, 'p': 4}

# Natural Inflation: V = Lambda^4 * (1 + cos(phi/f))
NATURAL_PARAMS = {'Lambda': 1e-3, 'f': 5.0}

# ============================================================================
# INITIAL CONDITIONS
# ============================================================================
# You can provide single values or lists for parameter sweeping
# Example: PHI_INIT = [5.0, 6.0, 7.0] will run 3 simulations.
PHI_INIT = 5.0         # Initial field value  quadratic(recommended) = 5.0, starobinsky = 7.0
PHI_DOT_INIT = 0.0     # Initial velocity (0 for slow-roll start)

# ============================================================================
# SIMULATION PARAMETERS
# ============================================================================
T_START = 0.0
T_END = 500  # quadratic(recommended) = 500, 
NUM_POINTS = 2000 
RTOL = 1e-8
ATOL = 1e-10

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================
OUTPUT_FILENAME = "inflation_dynamics.png"
SHOW_PLOT = True
SAVE_PLOT = True
OUTPUT_FOLDER = "results"
PLOT_WIDTH = 10
PLOT_HEIGHT = 6
DPI = 300

# ============================================================================
# ADVANCED OPTIONS
# ============================================================================
VERBOSE = True
CHECK_SLOW_ROLL = True

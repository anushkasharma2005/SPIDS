#!/usr/bin/env python3
"""
Interactive Configuration Generator
====================================
This script helps you create a custom config.py interactively.
"""

def create_config_interactive():
    print("="*70)
    print("Inflation Simulation - Interactive Config Generator")
    print("="*70)
    print()
    
    # Choose potential
    print("Available potentials:")
    print("  1. Quadratic (V = 1/2 * m^2 * phi^2)")
    print("  2. Starobinsky (V = V0 * (1 - exp(-sqrt(2/3)*phi))^2)")
    print("  3. Hilltop (V = V0 * (1 - (phi/mu)^p))")
    print("  4. Natural Inflation (V = Lambda^4 * (1 + cos(phi/f)))")
    print()
    
    potential_choice = input("Select potential (1-4) [default: 1]: ").strip() or "1"
    potential_map = {
        "1": ("quadratic", "Quadratic"),
        "2": ("starobinsky", "Starobinsky"),
        "3": ("hilltop", "Hilltop"),
        "4": ("natural", "Natural Inflation")
    }
    
    potential_type, potential_name = potential_map.get(potential_choice, ("quadratic", "Quadratic"))
    print(f"\n✓ Selected: {potential_name}")
    
    # Customize potential parameters
    print("\n" + "-"*70)
    print("Potential Parameters")
    print("-"*70)
    
    # Default parameters strings
    defaults_quad = "{'m': 0.1}"
    defaults_star = "{'V0': 1e-10}"
    defaults_hill = "{'V0': 1e-10, 'mu': 1.0, 'p': 4}"
    defaults_nat = "{'Lambda': 1e-3, 'f': 5.0}"
    
    # Setup strings for config file
    s_quad = defaults_quad
    s_star = defaults_star
    s_hill = defaults_hill
    s_nat = defaults_nat
    
    customize = input(f"Customize parameters for {potential_name}? (y/n) [default: n]: ").strip().lower()
    
    if customize == 'y':
        print("\nEnter parameters as python dictionary or just the values.")
        print("You can also enter LISTS for parameter sweeping! e.g. [0.01, 0.02]")
        
        if potential_type == "quadratic":
            val = input(f"m [default: 0.1]: ").strip() or "0.1"
            # simple check if user entered a dictionary or just a number/list
            if val.startswith("{"): s_quad = val
            else: s_quad = f"{{'m': {val}}}"
            
        elif potential_type == "starobinsky":
            val = input(f"V0 [default: 1e-10]: ").strip() or "1e-10"
            if val.startswith("{"): s_star = val
            else: s_star = f"{{'V0': {val}}}"
            
        elif potential_type == "hilltop":
            v0 = input(f"V0 [default: 1e-10]: ").strip() or "1e-10"
            mu = input(f"mu [default: 1.0]: ").strip() or "1.0"
            p = input(f"p [default: 4]: ").strip() or "4"
            s_hill = f"{{'V0': {v0}, 'mu': {mu}, 'p': {p}}}"
            
        elif potential_type == "natural":
            lam = input(f"Lambda [default: 1e-3]: ").strip() or "1e-3"
            f_val = input(f"f [default: 5.0]: ").strip() or "5.0"
            s_nat = f"{{'Lambda': {lam}, 'f': {f_val}}}"
            
        print("✓ Parameters updated.")

    # Get initial conditions
    print("\n" + "-"*70)
    print("Initial Conditions")
    print("-"*70)
    phi_init = input("Initial field value φ₀ [default: 5.0]: ").strip() or "5.0"
    phi_dot_init = input("Initial velocity φ̇₀ [default: 0.0]: ").strip() or "0.0"
    
    # Get simulation parameters
    print("\n" + "-"*70)
    print("Simulation Parameters")
    print("-"*70)
    t_end = input("Maximum time T_END [default: 500]: ").strip() or "500"
    num_points = input("Number of output points [default: 2000]: ").strip() or "2000"
    
    # Get output options
    print("\n" + "-"*70)
    print("Output Options")
    print("-"*70)
    output_file = input("Output filename [default: inflation_dynamics.png]: ").strip() or "inflation_dynamics.png"
    show_plot = input("Show plot after simulation? (y/n) [default: y]: ").strip().lower() or "y"
    verbose = input("Show detailed output? (y/n) [default: y]: ").strip().lower() or "y"
    
    # Generate config file
    show_plot_bool = "True" if show_plot in ["y", "yes"] else "False"
    verbose_bool = "True" if verbose in ["y", "yes"] else "False"
    
    config_content = f'''"""
        Configuration file for Inflation Simulation
        Generated interactively
    """

# ============================================================================
# POTENTIAL SELECTION
# ============================================================================
POTENTIAL_TYPE = "{potential_type}"

# ============================================================================
# POTENTIAL PARAMETERS
# ============================================================================
QUADRATIC_PARAMS = {s_quad}
STAROBINSKY_PARAMS = {s_star}
HILLTOP_PARAMS = {s_hill}
NATURAL_PARAMS = {s_nat}

# ============================================================================
# INITIAL CONDITIONS
# ============================================================================
PHI_INIT = {phi_init}
PHI_DOT_INIT = {phi_dot_init}

# ============================================================================
# SIMULATION PARAMETERS
# ============================================================================
T_START = 0.0
T_END = {t_end}
NUM_POINTS = {num_points}
RTOL = 1e-8
ATOL = 1e-10

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================
OUTPUT_FILENAME = "{output_file}"
SHOW_PLOT = {show_plot_bool}
SAVE_PLOT = True
OUTPUT_FOLDER = "results"
PLOT_WIDTH = 10
PLOT_HEIGHT = 6
DPI = 300

# ============================================================================
# ADVANCED OPTIONS
# ============================================================================
VERBOSE = {verbose_bool}
CHECK_SLOW_ROLL = True
'''
    
    # Save the file
    import os
    os.makedirs("config", exist_ok=True)
    with open("config/config.py", "w") as f:
        f.write(config_content)
    
    print("\n" + "="*70)
    print("✓ Configuration saved to config/config.py")
    print("="*70)
    print("\nYou can now run the simulation with:")
    print("  python3 main.py")
    print()

if __name__ == "__main__":
    create_config_interactive()

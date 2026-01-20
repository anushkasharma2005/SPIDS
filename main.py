#####################################################################################
#                      Simple Inflationary Dynamics Simulator                       #
#                                                                                   #
# DO NOT MODIFY THIS FILE - Edit config.py to customize your simulation            #
#####################################################################################


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import itertools
import os

from src.potentials import QuadraticPotential, StarobinskyPotential, HilltopPotential, NaturalPotential
from src.dynamics import inflation_dynamics, end_inflation_event
from src.utils import save_plot
import config.config as config


def get_potential_instance(potential_type, params):
    """Create a potential instance with specific parameters."""

    potential_type = potential_type.lower()
    
    if potential_type == "quadratic":
        return QuadraticPotential(**params)
    elif potential_type == "starobinsky":
        return StarobinskyPotential(**params)
    elif potential_type == "hilltop":
        return HilltopPotential(**params)
    elif potential_type == "natural":
        return NaturalPotential(**params)
    else:
        raise ValueError(f"Unknown potential type: {potential_type}")




def to_list(param):
    """Ensure parameter is a list for iteration."""

    if isinstance(param, (list, tuple, np.ndarray)):
        return param
    return [param]




def run_simulation(potential, phi_init, phi_dot_init, t_span, t_eval):
    """Run a single simulation."""

    y0 = [phi_init, phi_dot_init]

    def end_event(t, y):
        return end_inflation_event(t, y, potential)
    

    # end_event.terminal = True
    # end_event.direction = -1

    return solve_ivp(
        fun=lambda t, y: inflation_dynamics(t, y, potential),
        t_span=t_span,
        y0=y0,
        events=end_event,
        t_eval=t_eval,
        rtol=config.RTOL,
        atol=config.ATOL
    )




def main():
    if config.VERBOSE:
        print("="*70)
        print("Inflationary Dynamics Simulator - Batch Mode")
        print("="*70)

    # 1. Determine Potential Type
    pot_type = config.POTENTIAL_TYPE.lower()
    
    # 2. Get Potential Parameters (handle lists)
    if pot_type == "quadratic":
        raw_params = config.QUADRATIC_PARAMS
    elif pot_type == "starobinsky":
        raw_params = config.STAROBINSKY_PARAMS
    elif pot_type == "hilltop":
        raw_params = config.HILLTOP_PARAMS
    elif pot_type == "natural":
        raw_params = config.NATURAL_PARAMS
    else:
        print(f"Error: Unknown potential type '{pot_type}'")
        return


    # 3. Prepare Parameter Sweeps
    # Convert all potential params to lists
    param_keys = list(raw_params.keys())
    param_values_list = [to_list(raw_params[k]) for k in param_keys]
    
    # System params
    phi_init_list = to_list(config.PHI_INIT)
    phi_dot_init_list = to_list(config.PHI_DOT_INIT)
    
    # Generate all combinations
    # Combine (pot_params) + (phi_init) + (phi_dot_init)
    all_lists = param_values_list + [phi_init_list, phi_dot_init_list]
    combinations = list(itertools.product(*all_lists))
    
    total_runs = len(combinations)
    print(f"Found {total_runs} parameter combination(s) to run.")
    print(f"Output folder: {config.OUTPUT_FOLDER}/{pot_type}/")
    print("-" * 70)

    # 4. Run Loop
    for idx, combo in enumerate(combinations):
        # Unpack combo
        # First N items are potential params
        pot_param_values = combo[:len(param_keys)]
        current_phi = combo[-2]
        current_phi_dot = combo[-1]
        
        # Build params dict for this run
        current_pot_params = dict(zip(param_keys, pot_param_values))
        
        # Create potential
        potential = get_potential_instance(pot_type, current_pot_params)
        
        # Time setup
        t_eval = np.linspace(config.T_START, config.T_END, config.NUM_POINTS)
        
        if config.VERBOSE:
            param_str = ", ".join([f"{k}={v}" for k,v in current_pot_params.items()])
            print(f"Run {idx+1}/{total_runs}: P({param_str}), φ₀={current_phi}, φ̇₀={current_phi_dot}")

        # Execute
        result = run_simulation(
            potential, 
            phi_init=current_phi, 
            phi_dot_init=current_phi_dot, 
            t_span=(config.T_START, config.T_END), 
            t_eval=t_eval
        )
        
        # Process Results
        process_results(result, pot_type, current_pot_params, current_phi, current_phi_dot, idx+1)




def process_results(result, pot_type, pot_params, phi0, phi_dot0, run_id):
    t = result.t
    phi = result.y[0]
    phi_dot = result.y[1]
    
    # Construct unique folder for this run
    # Format: results/<potential>/run_<id>_<params>_phi<init>/
    safe_param_str = "_".join([f"{k}{v}" for k,v in pot_params.items()])
    run_folder_name = f"run_{run_id}_{safe_param_str}_phi{phi0}"
    run_output_dir = os.path.join(config.OUTPUT_FOLDER, pot_type, run_folder_name)
    
    # Common title parameters
    param_str = ", ".join([f"{k}={v}" for k,v in pot_params.items()])
    base_title = f"{pot_type.capitalize()} ({param_str})\nφ₀={phi0}, φ̇₀={phi_dot0}"

    # --- 1. Combined Plot ---
    plt.figure(figsize=(config.PLOT_WIDTH, config.PLOT_HEIGHT))
    plt.plot(t, phi, label='Inflaton Field φ(t)', linewidth=2)
    plt.plot(t, phi_dot, label='Inflaton Field Derivative φ̇(t)', linewidth=2)
    
    plt.xlabel('Time (Planck units)', fontsize=12)
    plt.ylabel('Values', fontsize=12)
    plt.title(f"{base_title} - Combined Dynamics", fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    
    if config.SAVE_PLOT:
        # Save combined plot
        save_plot("combined_dynamics.png", folder=run_output_dir)

    if config.SHOW_PLOT:
        plt.show()
    else:
        plt.close()

    # --- 2. Field Plot (Phi only) ---
    plt.figure(figsize=(config.PLOT_WIDTH, config.PLOT_HEIGHT))
    plt.plot(t, phi, label='Inflaton Field φ(t)', linewidth=2, color='tab:blue')
    
    plt.xlabel('Time (Planck units)', fontsize=12)
    plt.ylabel('Field Value φ', fontsize=12)
    plt.title(f"{base_title} - Field Evolution", fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    
    if config.SAVE_PLOT:
        save_plot("field_phi.png", folder=run_output_dir)
    plt.close()

    # --- 3. Velocity Plot (Phi_dot only) ---
    plt.figure(figsize=(config.PLOT_WIDTH, config.PLOT_HEIGHT))
    plt.plot(t, phi_dot, label='Velocity φ̇(t)', linewidth=2, color='tab:orange')
    
    plt.xlabel('Time (Planck units)', fontsize=12)
    plt.ylabel('Velocity φ̇', fontsize=12)
    plt.title(f"{base_title} - Velocity Evolution", fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    
    if config.SAVE_PLOT:
        save_plot("velocity_phi_dot.png", folder=run_output_dir)
    plt.close()


if __name__ == "__main__":
    main()   
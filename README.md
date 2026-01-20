# SPIDS: Simple Python Inflation Dynamics Simulator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Research%20Preview-orange.svg)]()

**SPIDS** is a flexible simulation tool for studying cosmological inflation with various inflaton potential models. Its designed to solve the equations of motion for scalar field inflation in a Friedmann-Lemaître-Robertson-Walker (FLRW) universe. It supports multiple potential models, automatic parameter sweeping, and detailed graphical output.


---

## Features

*   **Modular Architecture:** Separation of physics logic (`src/dynamics.py`), potential definitions (`src/potentials.py`), and configuration (`config/`).
*   **Batch Processing:** Automatically runs simulations over lists of parameters (e.g., test 10 different masses in one go).
*   **Detailed Output:** Generates extensive data for every run in organized folders:
    1.  Field Evolution $\phi(t)$
    2.  Velocity Evolution $\dot{\phi}(t)$
    3.  Combined phase plot.
*   **Robust Physics:** Handles "Slow-Roll" epsilon calculation ($\epsilon = -\dot{H}/H^2$) rigorously without approximations.
*   **Interactive Config:** Includes a CLI tool to generate simulation configurations without writing code.



## Quick Start

### 1. Installation

**Automatic Installation (Recommended):**
This script will create a virtual environment (`sim_env`) and install dependencies:
```bash
./install_dependencies.sh
```

### 2. Running the Simulation

**Step 1: Activate the Virtual Environment**
You need to do this every time you open a new terminal:
```bash
source sim_env/bin/activate
```

**Step 2: Run the code**

**Easiest way** - Use the interactive config generator:
```bash
python3 create_config.py  # Creates config.py interactively
python3 main.py           # Runs the simulation
```

**Easy way** - Use the default configuration:
```bash
python3 main.py
```

**Custom way** - Manually edit the configuration file:
```bash
# Edit config.py with your desired parameters
python3 main.py
```

## How to Use

### For Users (No Code Modification Required!)

1. **DO NOT edit `main.py`** - All customization is done through `config.py`
2. Open [config.py](config.py) and modify the parameters
3. Run `python3 main.py` 
4. Results are saved in the `results/` folder

### Configuration Parameters

#### Potential Selection
Choose from four inflation models by setting `POTENTIAL_TYPE`:
- `"quadratic"` - Standard $V = \frac{1}{2}m^2\phi^2$ (Recommended for beginners)
- `"starobinsky"` - $V = V_0(1-e^{-\sqrt{2/3}\phi})^2$
- `"hilltop"` - $V = V_0(1-(\phi/\mu)^p)$
- `"natural"` - $V = \Lambda^4(1+\cos(\phi/f))$

#### Key Parameters (in config.py)

**Initial Conditions:**
- `PHI_INIT` - Starting field value (Recommended: 5.0 for quadratic)
- `PHI_DOT_INIT` - Starting velocity (Recommended: 0.0 for slow-roll)

**Simulation Settings:**
- `T_END` - Maximum simulation time (Recommended: 1e5)
- `NUM_POINTS` - Number of output points (Recommended: 1000-5000)
- `RTOL`, `ATOL` - Integration tolerances (Recommended: 1e-8, 1e-10)

**Output Options:**
- `OUTPUT_FILENAME` - Name for saved plot
- `SHOW_PLOT` - Display plot after simulation (True/False)
- `SAVE_PLOT` - Save plot to file (True/False)
- `VERBOSE` - Print detailed information (True/False)

### Example Configurations

#### Example 1: Quadratic Potential
```python3
POTENTIAL_TYPE = "quadratic"
QUADRATIC_PARAMS = {'m': 0.01}
PHI_INIT = 5.0
PHI_DOT_INIT = 0.0
```

#### Example 2: Starobinsky Potential
```python3
POTENTIAL_TYPE = "starobinsky"
STAROBINSKY_PARAMS = {'V0': 1e-10}
PHI_INIT = 3.0
PHI_DOT_INIT = 0.0
```

### 3. Running Parameter Sweeps 

You can calculate graphs for multiple parameter combinations automatically!
In `config/config.py`, simply provide a list of values instead of a single number.

**Example: Scan different masses and initial conditions**
```python
# Check how mass affects inflation
QUADRATIC_PARAMS = {'m': [0.01, 0.02, 0.05]}

# Check sensitivity to initial conditions
PHI_INIT = [5.0, 6.0, 7.0]
```
Running `python3 main.py` will now run $3 \times 3 = 9$ simulations and save all plots.

## File Structure

```
inflation_simulation/
├── main.py              # Main simulation code (Entry point)
├── config/              # Configuration folder
│   ├── config.py        # User configuration
│   └── config_template.py
├── src/                 # Source code folder
│   ├── dynamics.py      # Physics equations
│   ├── potentials.py    # Potential models
│   └── utils.py         # Utility functions
├── create_config.py     # Helper tool
├── install_dependencies.sh # Installation script
├── requirements.txt     # Dependency list
├── readme.md            # Documentation
└── results/             # Output folder
    └── quadratic/       # Organized by potential type
```




## Output Structure

Results are automatically organized by Potential Type and Run ID to ensure no data is overwritten.

```text
results/
└── quadratic/                        # Normalized by Potential Type
    ├── run_1_m0.01_phi5.0/           # Specific Run Folder
    │   ├── field_evolution.png       # Plot 1: φ vs t
    │   ├── velocity_evolution.png    # Plot 2: φ' vs t
    │   └── combined_dynamics.png     # Plot 3: Combined
    └── run_2_m0.01_phi6.0/
        └── ...
```


## Physics Background
SPIDS numerically solves the Klein-Gordon equation for a homogenous scalar field $\phi(t)$ in an expanding universe:

$$ \ddot{\phi} + 3H\dot{\phi} + \frac{dV}{d\phi} = 0 $$

Where the Hubble parameter $H$ is determined by the Friedmann equation (assuming flat geometry and $M_{pl}=1$):

$$ H^2 = \frac{1}{3} \left( \frac{1}{2}\dot{\phi}^2 + V(\phi) \right) $$

Inflation ends when the generic slow-roll parameter $\epsilon$ reaches unity:

$$ \epsilon = -\frac{\dot{H}}{H^2} = \frac{1}{2} \frac{\dot{\phi}^2}{H^2} = 1 $$

### Supported Potentials

| Potential | Formula | Code Key |
| :--- | :--- | :--- |
| **Quadratic** | $V(\phi) = \frac{1}{2}m^2\phi^2$ | `quadratic` |
| **Starobinsky** | $V(\phi) = V_0(1 - e^{-\sqrt{2/3}\phi})^2$ | `starobinsky` |
| **Hilltop** | $V(\phi) = V_0(1 - (\phi/\mu)^p)$ | `hilltop` |
| **Natural** | $V(\phi) = \Lambda^4(1 + \cos(\phi/f))$ | `natural` |


## Tips

- Start with `VERBOSE = True` to see what's happening
- For faster simulations, reduce `NUM_POINTS`
- For more accurate results, decrease `RTOL` and `ATOL`
- If simulation doesn't finish, increase `T_END`
- Different potentials require different initial conditions

## References

All units are in Planck units where $M_{pl} = 1$.

For more information on inflation, consult:
- Baumann, D. (2009). "TASI Lectures on Inflation"
- Lyth, D. H., & Liddle, A. R. (2009). "The Primordial Density Perturbation"


## Recommended Settings 

### Quadratic Potential
- `PHI_INIT = 5.0`
- `PHI_DOT_INIT = 0.0`
- `T_END = 2000`
- `NUM_POINTS = 1000`
- `m = 0.01` or `m = 0.1`


### Starobinsky Potential
- `V0 = 1`
- `PHI_INIT = 5.8`
- `PHI_DOT_INIT = 0.0`
- `T_END = 200`
- `NUM_POINTS = 2000`

### Hilltop Potential
- `lambda = 1`
- `mu = 1.0`
- `p = 4`
- `PHI_INIT = 0.1`
- `PHI_DOT_INIT = 0.0`
- `T_END = 500`
- `NUM_POINTS = 2000`

### Natural Potential
- `Lambda = 1`
- `f = 10`
- `PHI_INIT = 0.0`
- `PHI_DOT_INIT = 0.0`
- `T_END = 3000`
- `NUM_POINTS = 3000`


---


## License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Author:** Anushka S.  <br>
**Last Updated:** 20 January 2026

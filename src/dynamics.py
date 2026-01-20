import numpy as np


def inflation_dynamics(t, y, potential):
    """Compute the derivatives for the inflationary dynamics.

    Parameters:
    t : float
        The current time (not used in this case as the system is autonomous).
    y : array_like
        The current state vector [phi, phi_dot].
    potential : object
        An instance of a potential class with methods V(phi) and dV_dphi(phi).

    Returns:
    dydt : array_like
        The derivatives [phi_dot, phi_double_dot].
    """

    phi, phi_dot = y
    V = potential.V(phi)
    dV_dphi = potential.dV_dphi(phi)

    # Hubble parameter H
    # Check for negative energy density (Big Crunch / Model invalidity)
    rho = 0.5 * phi_dot**2 + V
    if rho <= 0:
        # Return derivatives that stop evolution or indicate failure
        # Here we just set H=0 to avoid NaN, but the simulation should likely stop.
        H = 0
    else:
        H = np.sqrt((1/3) * rho)

    # Equations of motion
    phi_double_dot = -3 * H * phi_dot - dV_dphi

    return [phi_dot, phi_double_dot]



def end_inflation_event(t, y, potential):
    """Event function to determine when inflation ends (epsilon = 1).

    Parameters:
    t : float
        The current time (not used in this case as the system is autonomous).
    y : array_like
        The current state vector [phi, phi_dot].
    potential : object
        An instance of a potential class with methods V(phi) and dV_dphi(phi).

    Returns:
    float
        The value of epsilon - 1. Inflation ends when this crosses zero.
    """
    phi, phi_dot = y
    V = potential.V(phi)

    # Hubble parameter H
    rho = 0.5 * phi_dot**2 + V
    if rho <= 0:
        return 0.0 # Trigger event immediately if energy <= 0

    H = np.sqrt((1/3) * rho)

    # Slow-roll parameter epsilon (correct definition using Hubble parameter)
    # epsilon = (1/2) * (phi_dot / H)^2
    epsilon = 0.5 * (phi_dot / H)**2

    return epsilon - 1



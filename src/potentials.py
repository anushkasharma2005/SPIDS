import numpy as np

class QuadraticPotential:
    """Standard V = 1/2 * m^2 * phi^2"""
    def __init__(self, m=0.01):
        self.m = m

    def V(self, phi):
        return 0.5 * (self.m**2) * (phi**2)

    def dV_dphi(self, phi):
        return (self.m**2) * phi


class StarobinskyPotential:
    """V = V0 * (1 - exp(-sqrt(2/3) * phi))^2"""
    def __init__(self, V0=1e-10):
        self.V0 = V0
        self.alpha = np.sqrt(2/3)

    def V(self, phi):
        return self.V0 * (1 - np.exp(-self.alpha * phi))**2

    def dV_dphi(self, phi):
        exp_term = np.exp(-self.alpha * phi)
        return 2 * self.V0 * (1 - exp_term) * (self.alpha * exp_term)
    

class HilltopPotential:
    """V = V0 * (1 - (phi/mu)^p)"""
    def __init__(self, V0=1e-10, mu=1.0, p=4):
        self.V0 = V0
        self.mu = mu
        self.p = p

    def V(self, phi):
        return self.V0 * (1 - (phi / self.mu)**self.p)

    def dV_dphi(self, phi):
        return -self.V0 * self.p * (phi**(self.p - 1)) / (self.mu**self.p)
    

class NaturalPotential:
    """V = Lambda^4 * (1 + cos(phi/f))"""
    def __init__(self, Lambda=1e-10, f=1.0):
        self.Lambda = Lambda
        self.f = f

    def V(self, phi):
        return self.Lambda**4 * (1 + np.cos(phi / self.f))

    def dV_dphi(self, phi):
        return - (self.Lambda**4 / self.f) * np.sin(phi / self.f)
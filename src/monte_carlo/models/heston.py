"""Heston stochastic-volatility paths using full-truncation Euler."""
import numpy as np

def generate_heston_paths(spot, rate, v0, kappa, theta, xi, rho, maturity,
                          steps, paths, seed=42):
    if spot <= 0 or v0 < 0 or kappa < 0 or theta < 0 or xi < 0:
        raise ValueError("Invalid Heston parameters")
    if not -1 <= rho <= 1 or maturity <= 0 or steps < 1 or paths < 2:
        raise ValueError("Invalid correlation, maturity, steps, or paths")
    rng = np.random.default_rng(seed)
    dt = maturity / steps
    z1 = rng.standard_normal((paths, steps))
    z_ind = rng.standard_normal((paths, steps))
    z2 = rho * z1 + np.sqrt(max(0.0, 1.0-rho*rho)) * z_ind
    prices = np.empty((paths, steps + 1), dtype=float)
    variances = np.empty_like(prices)
    prices[:, 0], variances[:, 0] = spot, v0
    for t in range(steps):
        v_pos = np.maximum(variances[:, t], 0.0)
        prices[:, t+1] = prices[:, t] * np.exp(
            (rate - 0.5*v_pos)*dt + np.sqrt(v_pos*dt)*z1[:, t])
        variances[:, t+1] = np.maximum(
            variances[:, t] + kappa*(theta-v_pos)*dt
            + xi*np.sqrt(v_pos*dt)*z2[:, t], 0.0)
    return prices, variances

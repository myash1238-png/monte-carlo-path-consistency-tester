"""Geometric Brownian Motion path generator."""
import numpy as np

def generate_gbm_paths(spot, rate, volatility, maturity, steps, paths, seed=42,
                       antithetic=False):
    _validate(spot, volatility, maturity, steps, paths)
    rng = np.random.default_rng(seed)
    dt = maturity / steps
    half_or_all = (paths + 1) // 2 if antithetic else paths
    z = rng.standard_normal((half_or_all, steps))
    if antithetic:
        z = np.concatenate([z, -z], axis=0)[:paths]
    increments = (rate - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * z
    log_paths = np.cumsum(increments, axis=1)
    prices = spot * np.exp(np.concatenate(
        [np.zeros((paths, 1)), log_paths], axis=1))
    return prices

def _validate(spot, volatility, maturity, steps, paths):
    if spot <= 0 or volatility < 0 or maturity <= 0:
        raise ValueError("spot and maturity must be positive; volatility cannot be negative")
    if steps < 1 or paths < 2:
        raise ValueError("steps must be >= 1 and paths must be >= 2")

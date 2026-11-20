from dataclasses import dataclass
import numpy as np
from ..models.gbm import generate_gbm_paths
from ..models.heston import generate_heston_paths
from ..pricing.payoffs import terminal_payoff
from ..statistics.confidence_interval import mean_confidence_interval
from ..statistics.variance_reduction import apply_control_variate

@dataclass
class SimulationResult:
    model: str
    seed: int
    steps: int
    paths: int
    antithetic: bool
    control_variate: bool
    price: float
    standard_error: float
    ci_lower: float
    ci_upper: float
    sample_variance: float
    maturity: float
    spot: float
    strike: float
    rate: float
    volatility: float | None
    option_type: str

def run_gbm(config):
    paths = generate_gbm_paths(config.spot, config.rate, config.volatility,
        config.maturity, config.steps, config.paths, config.seed, config.antithetic)
    discounted = np.exp(-config.rate*config.maturity) * terminal_payoff(
        paths[:, -1], config.strike, config.option_type)
    if config.control_variate:
        # Discounted terminal stock has known expectation S0 for risk-neutral GBM.
        control = np.exp(-config.rate*config.maturity) * paths[:, -1]
        discounted = apply_control_variate(discounted, control, config.spot)
    price, se, low, high = mean_confidence_interval(discounted)
    return SimulationResult("GBM", config.seed, config.steps, config.paths,
        config.antithetic, config.control_variate, price, se, low, high,
        float(np.var(discounted, ddof=1)), config.maturity, config.spot,
        config.strike, config.rate, config.volatility, config.option_type)

def run_heston(*, spot, strike, rate, v0, kappa, theta, xi, rho, maturity,
               steps, paths, seed=42, option_type="call"):
    prices, _ = generate_heston_paths(spot, rate, v0, kappa, theta, xi,
        rho, maturity, steps, paths, seed)
    discounted = np.exp(-rate*maturity) * terminal_payoff(
        prices[:, -1], strike, option_type)
    price, se, low, high = mean_confidence_interval(discounted)
    return SimulationResult("Heston", seed, steps, paths, False, False,
        price, se, low, high, float(np.var(discounted, ddof=1)), maturity,
        spot, strike, rate, None, option_type)

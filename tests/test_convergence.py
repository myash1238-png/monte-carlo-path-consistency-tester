from config.settings import SimulationConfig
from monte_carlo.simulation.engine import run_gbm
from monte_carlo.pricing.black_scholes import black_scholes_price

def test_gbm_price_is_within_sampling_confidence_interval():
    cfg = SimulationConfig(paths=120_000, steps=100, seed=123)
    result = run_gbm(cfg)
    exact = black_scholes_price(cfg.spot,cfg.strike,cfg.rate,cfg.volatility,cfg.maturity)
    assert result.ci_lower <= exact <= result.ci_upper

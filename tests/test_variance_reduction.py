from config.settings import SimulationConfig
from monte_carlo.simulation.engine import run_gbm

def test_variance_reduction_switches_produce_finite_estimates():
    base = run_gbm(SimulationConfig(paths=30_000, seed=17))
    anti = run_gbm(SimulationConfig(paths=30_000, seed=17, antithetic=True))
    control = run_gbm(SimulationConfig(paths=30_000, seed=17, control_variate=True))
    assert all(map(lambda x: x == x, [base.price, anti.price, control.price]))
    # This is a broad sanity check; effectiveness is assessed across repeated seeds.
    assert anti.standard_error > 0 and control.standard_error > 0

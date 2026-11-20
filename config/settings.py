"""Default simulation settings; override these in scripts or tests."""
from dataclasses import dataclass

@dataclass(frozen=True)
class SimulationConfig:
    spot: float = 100.0
    strike: float = 100.0
    rate: float = 0.05
    volatility: float = 0.20
    maturity: float = 1.0
    steps: int = 252
    paths: int = 100_000
    seed: int = 42
    option_type: str = "call"
    antithetic: bool = False
    control_variate: bool = False

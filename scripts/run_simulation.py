import argparse
from config.settings import SimulationConfig
from monte_carlo.simulation.engine import run_gbm, run_heston
from monte_carlo.pricing.black_scholes import black_scholes_price
from monte_carlo.database.db import connect
from monte_carlo.database.repository import save_result
from monte_carlo.reporting.report import print_result

def main():
    parser = argparse.ArgumentParser(description="Run a Monte Carlo pricing experiment")
    parser.add_argument("--model", choices=["gbm","heston"], default="gbm")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--paths", type=int, default=100000)
    parser.add_argument("--steps", type=int, default=252)
    parser.add_argument("--antithetic", action="store_true")
    parser.add_argument("--control-variate", action="store_true")
    args = parser.parse_args()
    if args.model == "gbm":
        cfg = SimulationConfig(seed=args.seed, paths=args.paths, steps=args.steps,
            antithetic=args.antithetic, control_variate=args.control_variate)
        result = run_gbm(cfg)
        benchmark = black_scholes_price(cfg.spot,cfg.strike,cfg.rate,
            cfg.volatility,cfg.maturity,cfg.option_type)
    else:
        result = run_heston(spot=100,strike=100,rate=.05,v0=.04,kappa=2,
            theta=.04,xi=.5,rho=-.7,maturity=1,steps=args.steps,
            paths=args.paths,seed=args.seed)
        benchmark = None
    print_result(result, benchmark)
    with connect() as conn:
        print("Saved simulation_id:", save_result(conn, result))

if __name__ == "__main__":
    main()

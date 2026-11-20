# Monte Carlo Path Consistency Tester

An intermediate–advanced quantitative testing project for validating Monte Carlo pricing engines. It generates GBM and Heston paths, calculates discounted European option payoffs, measures sampling uncertainty, tests reproducibility, and persists run metadata/results in SQLite.

## Features

- GBM paths using `numpy.random.default_rng(seed)`.
- Heston stochastic-volatility paths using correlated Brownian shocks and full-truncation Euler variance updates.
- European call/put payoffs and Black–Scholes analytical benchmark for GBM.
- Student-t confidence intervals, Welch two-sample t-test, one-sample KS normality diagnostic, and two-sample KS test.
- Antithetic GBM paths and a discounted-stock control variate (known risk-neutral expectation is spot).
- SQLite schema for seed, path count, time steps, variance-reduction flags, estimates, standard errors, confidence bounds and sample variance.
- Pytest coverage for path shape, seed reproducibility, Heston variance constraints, convergence and statistics.

## Quick start

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

Run GBM:
```bash
python scripts/run_simulation.py --model gbm --seed 42 --paths 100000 --steps 252
```

Run GBM with antithetic variates:
```bash
python scripts/run_simulation.py --model gbm --seed 42 --paths 100000 --antithetic
```

Run GBM with control variates:
```bash
python scripts/run_simulation.py --model gbm --seed 42 --paths 100000 --control-variate
```

Run Heston:
```bash
python scripts/run_simulation.py --model heston --seed 42 --paths 100000 --steps 252
```

Inspect persisted experiments:
```bash
python scripts/analyze_results.py
```

Run tests:
```bash
pytest -v
```

## How to interpret the tests

1. **Seed reproducibility:** identical model parameters and seed must produce exactly identical paths on the same NumPy bit-generator/software setup. Different seeds should produce different paths.
2. **Convergence:** the GBM Monte Carlo estimate should approach the Black–Scholes price as path count increases. The analytical value is expected to fall inside a nominal 95% confidence interval approximately 95% of repeated experiments, not necessarily every run.
3. **Antithetic variates:** compare estimator variance across many independent seeds against plain Monte Carlo. A single run is not sufficient evidence of variance reduction.
4. **Control variate:** uses discounted terminal stock as the control with known expectation `S0` under risk-neutral GBM. The sample-estimated beta is used; for a formal out-of-sample validation, estimate beta on a pilot sample and freeze it for evaluation.
5. **Heston:** this implementation is a practical full-truncation Euler scheme. It is not an exact Heston simulator; discretization bias should be investigated by increasing time steps. Compare against a trusted Heston characteristic-function implementation before treating it as a production benchmark.
6. **Statistical tests:** p-values are diagnostics. Failure to reject a null hypothesis does not prove two engines are equivalent.

## SQL analysis

The database is created at `data/monte_carlo.sqlite`. Example queries:

```sql
-- Compare stored estimates across seeds
SELECT s.model, s.seed, s.paths, r.price, r.standard_error,
       r.ci_lower, r.ci_upper, r.sample_variance
FROM simulations s
JOIN results r USING (simulation_id)
ORDER BY s.model, s.seed;

-- Average price by variance-reduction configuration
SELECT antithetic, control_variate, COUNT(*) AS runs,
       AVG(price) AS mean_price,
       AVG(sample_variance) AS mean_payoff_variance
FROM simulations s
JOIN results r USING (simulation_id)
WHERE model = 'GBM'
GROUP BY antithetic, control_variate;

-- Price estimate variance across independent seeds
WITH x AS (
  SELECT AVG(r.price) AS mean_price
  FROM simulations s JOIN results r USING (simulation_id)
  WHERE s.model='GBM'
)
SELECT AVG((r.price-x.mean_price)*(r.price-x.mean_price))
       * COUNT(*) / (COUNT(*)-1) AS variance_across_seeds
FROM simulations s JOIN results r USING (simulation_id), x
WHERE s.model='GBM';
```

## Suggested portfolio extensions

- Add barrier, Asian, lookback and digital payoffs.
- Add Sobol quasi-Monte Carlo and Brownian bridge construction.
- Add confidence-interval coverage experiments over 100+ seeds.
- Add a benchmark suite for runtime, peak memory and paths/second.
- Add CI pipeline and coverage reporting.
- Add a Heston reference pricer and time-step bias report.

## Important implementation notes

- `paths` means the number of simulated terminal observations. For antithetic mode, paths are generated in positive/negative shock pairs, with an odd final path if an odd count is requested.
- The stored `sample_variance` is the variance of discounted payoff observations after any control-variate adjustment.
- SQLite is used to keep the project self-contained; the schema can be migrated to PostgreSQL.

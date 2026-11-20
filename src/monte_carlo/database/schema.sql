PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS simulations (
    simulation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL CHECK(model IN ('GBM','Heston')),
    seed INTEGER NOT NULL,
    steps INTEGER NOT NULL CHECK(steps > 0),
    paths INTEGER NOT NULL CHECK(paths >= 2),
    antithetic INTEGER NOT NULL CHECK(antithetic IN (0,1)),
    control_variate INTEGER NOT NULL CHECK(control_variate IN (0,1)),
    spot REAL NOT NULL,
    strike REAL NOT NULL,
    rate REAL NOT NULL,
    volatility REAL,
    maturity REAL NOT NULL,
    option_type TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL REFERENCES simulations(simulation_id),
    price REAL NOT NULL,
    standard_error REAL NOT NULL,
    ci_lower REAL NOT NULL,
    ci_upper REAL NOT NULL,
    sample_variance REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_simulations_model_seed ON simulations(model, seed);

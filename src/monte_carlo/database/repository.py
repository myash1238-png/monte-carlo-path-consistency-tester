def save_result(conn, result):
    cur = conn.execute("""
        INSERT INTO simulations
        (model,seed,steps,paths,antithetic,control_variate,spot,strike,rate,
         volatility,maturity,option_type)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (result.model, result.seed, result.steps, result.paths,
          int(result.antithetic), int(result.control_variate), result.spot,
          result.strike, result.rate, result.volatility, result.maturity,
          result.option_type))
    simulation_id = cur.lastrowid
    conn.execute("""
        INSERT INTO results
        (simulation_id,price,standard_error,ci_lower,ci_upper,sample_variance)
        VALUES (?,?,?,?,?,?)
    """, (simulation_id, result.price, result.standard_error,
          result.ci_lower, result.ci_upper, result.sample_variance))
    conn.commit()
    return simulation_id

def variance_across_seeds(conn, model="GBM"):
    """SQL sample variance of price estimates across independent seeds."""
    return conn.execute("""
        SELECT s.model, COUNT(*) AS runs, AVG(r.price) AS mean_price,
               AVG((r.price - x.mean_price)*(r.price - x.mean_price))
                   * COUNT(*) / NULLIF(COUNT(*)-1,0) AS variance_across_seeds
        FROM simulations s
        JOIN results r ON r.simulation_id=s.simulation_id
        JOIN (SELECT AVG(r2.price) AS mean_price
              FROM simulations s2 JOIN results r2
              ON r2.simulation_id=s2.simulation_id
              WHERE s2.model=?) x
        WHERE s.model=?
        GROUP BY s.model
    """, (model, model)).fetchone()

def list_results(conn, model=None):
    sql = """SELECT s.*, r.price, r.standard_error, r.ci_lower, r.ci_upper,
                    r.sample_variance
             FROM simulations s JOIN results r USING(simulation_id)"""
    if model:
        sql += " WHERE s.model=?"
        return conn.execute(sql + " ORDER BY s.simulation_id", (model,)).fetchall()
    return conn.execute(sql + " ORDER BY s.simulation_id").fetchall()

"""Black-Scholes European option benchmark."""
from math import erf, exp, log, sqrt

def _cdf(x):
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

def black_scholes_price(spot, strike, rate, volatility, maturity, option_type="call"):
    if min(spot, strike, volatility, maturity) <= 0:
        raise ValueError("spot, strike, volatility and maturity must be positive")
    d1 = (log(spot/strike) + (rate + 0.5*volatility**2)*maturity) / (volatility*sqrt(maturity))
    d2 = d1 - volatility*sqrt(maturity)
    if option_type == "call":
        return spot*_cdf(d1) - strike*exp(-rate*maturity)*_cdf(d2)
    if option_type == "put":
        return strike*exp(-rate*maturity)*_cdf(-d2) - spot*_cdf(-d1)
    raise ValueError("option_type must be 'call' or 'put'")

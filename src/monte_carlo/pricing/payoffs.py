import numpy as np

def terminal_payoff(terminal_prices, strike, option_type="call"):
    if option_type == "call":
        return np.maximum(np.asarray(terminal_prices) - strike, 0.0)
    if option_type == "put":
        return np.maximum(strike - np.asarray(terminal_prices), 0.0)
    raise ValueError("option_type must be 'call' or 'put'")

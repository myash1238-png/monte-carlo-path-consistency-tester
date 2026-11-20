import numpy as np

def apply_control_variate(payoffs, control, known_control_mean):
    """Return adjusted observations using beta estimated from this sample."""
    y, x = np.asarray(payoffs, float), np.asarray(control, float)
    if y.shape != x.shape or y.size < 2:
        raise ValueError("payoffs and control must have same shape and >=2 values")
    variance = np.var(x, ddof=1)
    if variance == 0:
        raise ValueError("Control variable has zero variance")
    beta = np.cov(y, x, ddof=1)[0, 1] / variance
    return y - beta * (x - known_control_mean)

def paired_antithetic_payoffs(positive_payoffs, negative_payoffs):
    a, b = np.asarray(positive_payoffs), np.asarray(negative_payoffs)
    if a.shape != b.shape:
        raise ValueError("Antithetic payoff arrays must have matching shapes")
    return (a+b)/2.0

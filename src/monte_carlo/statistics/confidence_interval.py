import numpy as np
from scipy import stats

def mean_confidence_interval(samples, confidence=0.95):
    x = np.asarray(samples, dtype=float)
    if x.size < 2:
        raise ValueError("At least two observations are required")
    mean = float(np.mean(x))
    se = float(stats.sem(x))
    critical = float(stats.t.ppf((1 + confidence)/2, df=x.size-1))
    margin = critical * se
    return mean, se, mean-margin, mean+margin

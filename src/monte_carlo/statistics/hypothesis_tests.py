"""Statistical diagnostics. Tests are diagnostics, not proof of correctness."""
import numpy as np
from scipy import stats

def two_sample_t_test(sample_a, sample_b):
    return stats.ttest_ind(sample_a, sample_b, equal_var=False)

def ks_normality_test(samples):
    x = np.asarray(samples, dtype=float)
    sd = x.std(ddof=1)
    if sd == 0:
        raise ValueError("KS test is undefined for zero-variance samples")
    standardized = (x-x.mean())/sd
    return stats.kstest(standardized, "norm")

def ks_two_sample_test(sample_a, sample_b):
    return stats.ks_2samp(sample_a, sample_b)

import numpy as np
from monte_carlo.statistics.confidence_interval import mean_confidence_interval
from monte_carlo.statistics.hypothesis_tests import two_sample_t_test, ks_two_sample_test

def test_confidence_interval_contains_mean_for_symmetric_sample():
    x = np.random.default_rng(5).normal(3,1,5000)
    mean,se,low,high = mean_confidence_interval(x)
    assert low < 3 < high
    assert se > 0

def test_statistical_tests_return_p_values():
    rng = np.random.default_rng(4)
    a,b = rng.normal(size=100),rng.normal(size=100)
    assert 0 <= two_sample_t_test(a,b).pvalue <= 1
    assert 0 <= ks_two_sample_test(a,b).pvalue <= 1

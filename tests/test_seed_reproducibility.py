import numpy as np
from monte_carlo.models.gbm import generate_gbm_paths

def test_fixed_seed_reproduces_identical_paths():
    a = generate_gbm_paths(100,.05,.2,1,20,1000,seed=7)
    b = generate_gbm_paths(100,.05,.2,1,20,1000,seed=7)
    assert np.array_equal(a,b)

def test_different_seeds_change_paths():
    a = generate_gbm_paths(100,.05,.2,1,20,1000,seed=7)
    b = generate_gbm_paths(100,.05,.2,1,20,1000,seed=8)
    assert not np.array_equal(a,b)

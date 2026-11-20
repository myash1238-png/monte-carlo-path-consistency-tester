import numpy as np
from monte_carlo.models.gbm import generate_gbm_paths

def test_gbm_shape_and_initial_spot():
    p = generate_gbm_paths(100,.05,.2,1,12,200,seed=1)
    assert p.shape == (200,13)
    assert np.all(p[:,0] == 100)
    assert np.all(p > 0)

import numpy as np
from monte_carlo.models.heston import generate_heston_paths

def test_heston_shapes_and_nonnegative_variance():
    p,v = generate_heston_paths(100,.03,.04,2,.04,.5,-.7,1,24,500,seed=2)
    assert p.shape == v.shape == (500,25)
    assert np.all(p > 0)
    assert np.all(v >= 0)

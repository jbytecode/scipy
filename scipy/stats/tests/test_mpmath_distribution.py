import numpy as np
from scipy import stats
from numpy.testing import assert_allclose
from .mpmath_distribution import SkewNormal
from mpmath import mp

def test_basic():
    mp.dps = 20  # high enough to pass, not unreasonably slow

    # Basic tests of mpmath distribution using a SciPy distribution as a
    # reference. The mpmath distribution is assumed to be more accurate;
    # this is just to make sure that the methods are implemented correctly
    # and that broadcasting is working as expected.
    rng = np.random.default_rng(6716188855217730280)

    x = rng.random(size=3)
    a = rng.random(size=(2, 1))
    rtol = 1e-15

    dist = SkewNormal(a=a)
    dist_ref = stats.skewnorm(a)

    assert_allclose(dist.pdf(x), dist_ref.pdf(x), rtol=rtol)
    assert_allclose(dist.cdf(x), dist_ref.cdf(x), rtol=rtol)
    assert_allclose(dist.sf(x), dist_ref.sf(x), rtol=rtol)
    assert_allclose(dist.ppf(x), dist_ref.ppf(x), rtol=rtol)
    assert_allclose(dist.isf(x), dist_ref.isf(x), rtol=rtol)
    assert_allclose(dist.logpdf(x), dist_ref.logpdf(x), rtol=rtol)
    assert_allclose(dist.logcdf(x), dist_ref.logcdf(x), rtol=rtol)
    assert_allclose(dist.logsf(x), dist_ref.logsf(x), rtol=rtol)
    assert_allclose(dist.support(), dist_ref.support(), rtol=rtol)
    assert_allclose(dist.entropy(), dist_ref.entropy(), rtol=rtol)
    assert_allclose(dist.mean(), dist_ref.mean(), rtol=rtol)
    assert_allclose(dist.var(), dist_ref.var(), rtol=rtol)
    assert_allclose(dist.skew(), dist_ref.stats('s'), rtol=rtol)
    assert_allclose(dist.kurtosis(), dist_ref.stats('k'), rtol=rtol)

import numpy as np
from numpy.testing import assert_allclose, assert_array_less
import pytest
from scipy.stats._resampling import BootstrapResult

from scipy.stats import f_ishigami, sobol_indices, uniform
from scipy.stats._sensitivity_analysis import BootstrapSobolResult, sample_AB, sample_A_B

@pytest.fixture(scope='session')
def ishigami_ref_indices():
    """Reference values for Ishigami from Saltelli2007.

    Chapter 4, exercise 5 pages 179-182.
    """
    a = 7.
    b = 0.1

    var = 0.5 + a**2/8 + b*np.pi**4/5 + b**2*np.pi**8/18
    v1 = 0.5 + b*np.pi**4/5 + b**2*np.pi**8/50
    v2 = a**2/8
    v3 = 0
    v12 = 0
    # v13: mistake in the book, see other derivations e.g. in 10.1002/nme.4856
    v13 = b**2*np.pi**8*8/225
    v23 = 0

    s_first = np.array([v1, v2, v3])/var
    s_second = np.array([
        [0., 0., v13],
        [v12, 0., v23],
        [v13, v23, 0.]
    ])/var
    s_total = s_first + s_second.sum(axis=1)

    return [s_first.reshape(1, -1), s_total.reshape(1, -1)]


def f_ishigami_vec(x):
    """Output of shape (2, n)."""
    res = f_ishigami(x)
    return np.concatenate([res, res]).reshape(2, -1)


class TestSobolIndices:

    def test_sample_AB(self):
        # (d, n)
        A = np.array(
            [[1, 4, 7, 10],
             [2, 5, 8, 11],
             [3, 6, 9, 12]]
        )
        B = A + 100
        # (d, n*d)
        ref = np.array(
            [[101, 104, 107, 110, 1, 4, 7, 10, 1, 4, 7, 10],
             [2, 5, 8, 11, 102, 105, 108, 111, 2, 5, 8, 11],
             [3, 6, 9, 12, 3, 6, 9, 12, 103, 106, 109, 112]]
        )

        AB = sample_AB(A=A, B=B)
        assert_allclose(AB, ref)

    @pytest.mark.parametrize(
        'func',
        [f_ishigami, pytest.param(f_ishigami_vec, marks=pytest.mark.slow)],
        ids=['scalar', 'vector']
    )
    def test_ishigami(self, ishigami_ref_indices, func):
        rng = np.random.default_rng(28631265345463262246170309650372465332)
        res = sobol_indices(
            func=func, n=4096,
            dists=[
                uniform(loc=-np.pi, scale=2*np.pi),
                uniform(loc=-np.pi, scale=2*np.pi),
                uniform(loc=-np.pi, scale=2*np.pi)
            ],
            random_state=rng
        )

        if func.__name__ == 'f_ishigami_vec':
            ishigami_ref_indices = [
                np.concatenate(
                    [ishigami_ref_indices[0], ishigami_ref_indices[0]]
                ),
                np.concatenate(
                    [ishigami_ref_indices[1], ishigami_ref_indices[1]]
                )
            ]

        assert_allclose(res.first_order, ishigami_ref_indices[0], atol=1e-2)
        assert_allclose(res.total_order, ishigami_ref_indices[1], atol=1e-2)

        assert res._bootstrap_result is None
        bootstrap_res = res.bootstrap()
        assert isinstance(bootstrap_res, BootstrapSobolResult)
        assert isinstance(res._bootstrap_result, BootstrapResult)

        assert res._bootstrap_result.confidence_interval.low.shape[0] == 2
        assert res._bootstrap_result.confidence_interval.low[1].shape \
               == res.first_order.shape

        assert bootstrap_res.first_order.confidence_interval.low.shape \
               == res.first_order.shape
        assert bootstrap_res.total_order.confidence_interval.low.shape \
               == res.total_order.shape

        assert_array_less(
            bootstrap_res.first_order.confidence_interval.low, res.first_order
        )
        assert_array_less(
            res.first_order, bootstrap_res.first_order.confidence_interval.high
        )
        assert_array_less(
            bootstrap_res.total_order.confidence_interval.low, res.total_order
        )
        assert_array_less(
            res.total_order, bootstrap_res.total_order.confidence_interval.high
        )

        # call again to use previous results and change a param
        assert isinstance(
            res.bootstrap(confidence_level=0.9), BootstrapSobolResult
        )
        assert isinstance(res._bootstrap_result, BootstrapResult)

    def test_func_dict(self, ishigami_ref_indices):
        rng = np.random.default_rng(28631265345463262246170309650372465332)
        n = 4096
        dists = [
            uniform(loc=-np.pi, scale=2*np.pi),
            uniform(loc=-np.pi, scale=2*np.pi),
            uniform(loc=-np.pi, scale=2*np.pi)
        ]

        A, B = sample_A_B(n=n, dists=dists, random_state=rng)
        AB = sample_AB(A=A, B=B)

        func = {
            'f_A': f_ishigami(A),
            'f_B': f_ishigami(B),
            'f_AB': f_ishigami(AB)
        }

        res = sobol_indices(
            func=func, n=n,
            dists=dists,
            random_state=rng
        )
        assert_allclose(res.first_order, ishigami_ref_indices[0], atol=1e-2)

        res = sobol_indices(
            func=func, n=n,
            random_state=rng
        )
        assert_allclose(res.first_order, ishigami_ref_indices[0], atol=1e-2)

    def test_method(self, ishigami_ref_indices):
        def jansen_sobol(f_A, f_B, f_AB):
            """Jansen for S and Sobol' for St.

            From Saltelli2010, table 2 formulations (c) and (e)."""
            s_, n = f_A.shape
            f_AB = f_AB.reshape((-1, s_, n))

            var = np.var(np.concatenate([f_A, f_B], axis=1), axis=1)

            s = (var - 0.5*np.mean((f_B - f_AB)**2, axis=-1)) / var
            st = np.mean(f_A*(f_A - f_AB), axis=-1) / var

            return s.reshape(s_, -1), st.reshape(s_, -1)

        rng = np.random.default_rng(28631265345463262246170309650372465332)
        res = sobol_indices(
            func=f_ishigami, n=4096,
            dists=[
                uniform(loc=-np.pi, scale=2*np.pi),
                uniform(loc=-np.pi, scale=2*np.pi),
                uniform(loc=-np.pi, scale=2*np.pi)
            ],
            method=jansen_sobol,
            random_state=rng
        )

        assert_allclose(res.first_order, ishigami_ref_indices[0], atol=1e-2)
        assert_allclose(res.total_order, ishigami_ref_indices[1], atol=1e-2)

    def test_raises(self):

        message = r"The method `ppf` must be specified"
        with pytest.raises(ValueError, match=message):
            sobol_indices(n=0, func=f_ishigami, dists="uniform")

        with pytest.raises(ValueError, match=message):
            sobol_indices(n=0, func=f_ishigami, dists=[lambda x: x])

        message = r"The balance properties of Sobol'"
        with pytest.raises(ValueError, match=message):
            sobol_indices(n=7, func=f_ishigami, dists=[uniform()])

        message = r"The balance properties of Sobol'"
        with pytest.raises(ValueError, match=message):
            sobol_indices(n=4.1, func=f_ishigami, dists=[uniform()])

        message = r"'toto' is not a valid 'method'"
        with pytest.raises(ValueError, match=message):
            sobol_indices(n=0, func=f_ishigami, method='toto')

        message = r"must have the following signature"
        with pytest.raises(ValueError, match=message):
            sobol_indices(n=0, func=f_ishigami, method=lambda x: x)

        message = r"'dists' must be defined when 'func' is a callable"
        with pytest.raises(ValueError, match=message):
            sobol_indices(n=0, func=f_ishigami)

        def func_wrong_shape_output(x):
            return x.reshape(-1, 1)

        message = r"'func' output should have a shape"
        with pytest.raises(ValueError, match=message):
            sobol_indices(n=2, func=func_wrong_shape_output, dists=[uniform()])

        message = r"When 'func' is a dictionary"
        with pytest.raises(ValueError, match=message):
            sobol_indices(n=2, func={'f_A': [], 'f_AB': []}, dists=[uniform()])

        message = r"When 'func' is a dictionary"
        with pytest.raises(ValueError, match=message):
            # f_B malformed
            sobol_indices(
                n=2,
                func={'f_A': [1, 2], 'f_B': [3], 'f_AB': [5, 6, 7, 8]},
            )

        with pytest.raises(ValueError, match=message):
            # f_AB malformed
            sobol_indices(
                n=2,
                func={'f_A': [1, 2], 'f_B': [3, 4], 'f_AB': [5, 6, 7]},
            )

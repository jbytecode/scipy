from dataclasses import dataclass, field
import numpy as np
from ._censored_data import CensoredData
from scipy import special
from ._common import ConfidenceInterval
import warnings


__all__ = ['ecdf']


@dataclass
class ECDFNestedResult:
    points: np.ndarray
    # Exclude these from __str__
    _n: np.ndarray = field(repr=False)  # number "at risk"
    _d: np.ndarray = field(repr=False)  # number of "deaths"
    _sf: np.ndarray = field(repr=False)  # survival function for var estimate

    def confidence_interval(self, confidence_level=0.95):
        sf, d, n = self._sf, self._d, self._n

        # When n == d, Greenwood's formula divides by zero.
        # When s != 0, this can be ignored: var == inf, and CI is [0, 1]
        # When s == 0, this results in NaNs. Produce an informative warning.
        with np.errstate(divide='ignore', invalid='ignore'):
            var = sf ** 2 * np.cumsum(d / (n * (n - d)))

        message = ("The variance estimate is undefined at some observations. "
                   "This is feature of the mathematical formula.")
        if np.any(np.isnan(var)):
            warnings.warn(message, RuntimeWarning, stacklevel=2)

        se = np.sqrt(var)
        z = special.ndtri(1 / 2 + confidence_level / 2)

        low = np.clip(self.points - z * se, 0, 1)
        high = np.clip(self.points + z * se, 0, 1)
        return ConfidenceInterval(low, high)


@dataclass
class ECDFResult:
    x: np.ndarray
    cdf: ECDFNestedResult
    sf: ECDFNestedResult

    def __init__(self, x, cdf, sf, n, d):
        self.x = x
        self.cdf = ECDFNestedResult(cdf, n, d, sf)  # Both CDF and SF results
        self.sf = ECDFNestedResult(sf, n, d, sf)    # need SF for variance est.


def ecdf(sample):
    """Empirical cumulative distribution function of a sample.

    The empirical cumulative distribution function (ECDF) is a step function
    estimate of the CDF of the distribution underlying a sample.

    Parameters
    ----------
    sample : 1D array_like or `scipy.stats.CensoredData`
        Besides array_like, instances of `scipy.stats.CensoredData` containing
        uncensored and right-censored observations are supported. Currently,
        other instances of `stats.CensoredData` will result in a
        ``NotImplementedError``.

    Returns
    -------
    An object with the following attributes.

    x : ndarray
        The unique values at which the ECDF changes.
    cdf : ECDFNestedResult
        An object representing the empirical cumulative distribution function
    sf : ECDFNestedResult
        An object representing the complement of the empirical cumulative
        distribution function.

    The `cdf` and `sf` attributes themselves have the following attributes.

    points : ndarray
        The point estimate of the CDF/SF at the values in `x`.

    And the following methods:

    proportion_ci(confidence_level=0.95) :
        Compute the confidence interval around the CDF/SF at the values in `x`.

    Notes
    -----
    When each observation of the sample is a precise measurement, the ECDF
    steps up by ``1/len(sample)`` at each of the observations [1]_.

    When observations are lower bounds, upper bounds, or both upper and lower
    bounds, the data is said to be "censored", and `sample` may be provided as
    an instance of `scipy.stats.CensoredData`.

    For right-censored data, the ECDF is given by the Kaplan-Meier estimator
    [2]_; other forms of censoring are not supported at this time.

    References
    ----------
    .. [1] Conover, William Jay. Practical nonparametric statistics. Vol. 350.
           John Wiley & Sons, 1999.

    .. [2] Kaplan, Edward L., and Paul Meier. "Nonparametric estimation from
           incomplete observations." Journal of the American statistical
           association 53.282 (1958): 457-481.

    .. [3] Goel, Manish Kumar, Pardeep Khanna, and Jugal Kishore.
           "Understanding survival analysis: Kaplan-Meier estimate."
           International journal of Ayurveda research 1.4 (2010): 274.

    Examples
    --------
    **Uncensored Data**

    As in the example from [1]_ page 79, five boys were selected at random from
    those in a single high school. Their one-mile run times were recorded as
    follows.

    >>> sample = [6.23, 5.58, 7.06, 6.42, 5.20]  # one-mile run times (minutes)

    The empirical distribution function, which approximates the distribution
    function of one-mile run times of the population from which the boys were
    sampled, is calculated as follows.

    >>> from scipy import stats
    >>> res = stats.ecdf(sample)
    >>> res.x
    array([5.2 , 5.58, 6.23, 6.42, 7.06])
    >>> res.cdf.points
    array([0.2, 0.4, 0.6, 0.8, 1. ])

    To plot the result as a step function:

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> ax = plt.subplot()
    >>> ax.step(np.insert(res.x, 0, 4), np.insert(res.cdf.points, 0, 0),
    ...         where='post')
    >>> ax.set_xlabel('One-Mile Run Time (minutes)')
    >>> ax.set_ylabel('Empirical CDF')
    >>> plt.show()

    **Right-censored Data**

    As in the example from [1]_ page 91, the lives of ten car fanbelts were
    tested. Five tests concluded because the fanbelt being tested broke, but
    the remaining tests concluded for other reasons (e.g. the study ran out of
    funding, but the fanbelt was still functional). The mileage driven
    with the fanbelts were recorded as follows.

    >>> broken = [77, 47, 81, 56, 80]  # in thousands of miles driven
    >>> unbroken = [62, 60, 43, 71, 37]

    Precise survival times of the fanbelts that were still functional at the
    end of the tests are unknown, but they are known to exceed the values
    recorded in ``unbroken``. Therefore, these observations are said to be
    "right-censored", and the data is represented using
    `scipy.stats.CensoredData`.

    >>> sample = stats.CensoredData(uncensored=broken, right=unbroken)

    The empirical survival function is calculated as follows.

    >>> res = stats.ecdf(sample)
    >>> res.x
    array([37., 43., 47., 56., 60., 62., 71., 77., 80., 81.])
    >>> res.sf.points
    array([1.   , 1.   , 0.875, 0.75 , 0.75 , 0.75 , 0.75 , 0.5  , 0.25 , 0.   ])

    To plot the result as a step function:

    >>> ax = plt.subplot()
    >>> ax.step(np.insert(res.x, 0, 30), np.insert(res.sf.points, 0, 1),
    ...                   where='post')
    >>> ax.set_xlabel('Fanbelt Survival Time (thousands of miles)')
    >>> ax.set_ylabel('Empirical SF')
    >>> plt.show()

    """
    if not isinstance(sample, CensoredData):
        try:  # takes care of input standardization/validation
            sample = CensoredData(uncensored=sample)
        except ValueError as e:
            message = str(e).replace('uncensored', 'sample')
            raise type(e)(message) from e

    if sample.num_censored() == 0:
        res = _ecdf_uncensored(sample._uncensor())
    elif sample.num_censored() == sample._right.size:
        res = _ecdf_right_censored(sample)
    else:
        # Support additional censoring options in follow-up PRs
        message = ("Currently, only uncensored and right-censored data is "
                   "supported.")
        raise NotImplementedError(message)

    t, cdf, sf, n, d = res
    return ECDFResult(t, cdf, sf, n, d)


def _ecdf_uncensored(sample):
    sample = np.sort(sample)
    x, counts = np.unique(sample, return_counts=True)

    # [1].81 "the fraction of [observations] that are less than or equal to x
    cdf = np.cumsum(counts) / sample.size

    # [1].89 "the relative frequency of the sample that exceeds x in value"
    sf = 1 - cdf

    _n = sf*sample.size
    _d = counts

    return x, cdf, sf, _n, _d


def _ecdf_right_censored(sample):
    # It is conventional to discuss right-censored data in terms of
    # "survival time", "death", and "loss" (e.g. [2]). We'll use that
    # terminology here.
    # This implementation was influenced by the references cited and also
    # https://www.youtube.com/watch?v=lxoWsVco_iM
    # https://en.wikipedia.org/wiki/Kaplan%E2%80%93Meier_estimator
    # In retrospect it is probably most easily compared against [3].
    # Ultimately, the data needs to be sorted, so this implementation is
    # written to avoid a separate call to `unique` after sorting. In hope of
    # better performance on large datasets, it also computes survival
    # probabilities at unique times only rather than at each observation.
    tod = sample._uncensored  # time of "death"
    tol = sample._right  # time of "loss"
    times = np.concatenate((tod, tol))
    died = np.asarray([1]*tod.size + [0]*tol.size)

    # sort by times
    i = np.argsort(times)
    times = times[i]
    died = died[i]
    at_risk = np.arange(times.size, 0, -1)

    # logical indices of unique times
    j = np.diff(times, prepend=-np.inf, append=np.inf) > 0
    j_l = j[:-1]  # first instances of unique times
    j_r = j[1:]  # last instances of unique times

    # get number at risk and deaths at each unique time
    t = times[j_l]  # unique times
    n = at_risk[j_l]  # number at risk at each unique time
    cd = np.cumsum(died)[j_r]  # cumulative deaths up to/including unique times
    d = np.diff(cd, prepend=0)  # deaths at each unique time

    # compute survival function
    sf = np.cumprod((n - d) / n)
    cdf = 1 - sf
    return t, cdf, sf, n, d
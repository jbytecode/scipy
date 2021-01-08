import scipy.stats as stats
import numpy as np
from scipy._lib._util import check_random_state


def _resample_data(data, n_resamples=None, random_state=None):
    '''Resample the data'''
    n = data.shape[-1]
    if n_resamples:
        # bootstrap - each row is a random resample of original observations
        i = random_state.randint(0, n, (n_resamples, n))
    else:
        # jackknife - each row leaves out one observation
        j = np.ones((n, n), dtype=bool)
        np.fill_diagonal(j, False)
        i = np.arange(n)
        i = np.broadcast_to(i, (n, n))
        i = i[j].reshape((n, n-1))
    resamples = data[..., i]
    return resamples


def _percentile_of_score(data, score, axis):
    '''Vectorized, simplified scipy.stats.percentileofscore'''
    B = data.shape[axis]
    return (data < score).sum(axis=axis) / B


def _percentile_along_axis(theta_hat_b, alpha):
    '''np.percentile with different percentile for each slice'''
    shape = theta_hat_b.shape[:-1]
    alpha = np.broadcast_to(alpha, shape)
    percentiles = np.zeros_like(alpha)
    for indices, alpha_i in np.ndenumerate(alpha):
        theta_hat_b_i = theta_hat_b[indices]
        percentiles[indices] = np.percentile(theta_hat_b_i, alpha_i)
    return percentiles


def _bca_interval(data, statistic, axis, alpha, theta_hat_b):
    """Bias-corrected and accelerated interval """
    # closely follows [1] "BCa Bootstrap CIs"
    data = data[0]  # only works with 1 sample statistics right now

    # calculate z0_hat
    theta_hat = statistic(data, axis=axis)[..., None]
    percentile = _percentile_of_score(theta_hat_b, theta_hat, axis=-1)
    z0_hat = stats.norm.ppf(percentile)

    # calculate a_hat
    jackknife_data = _resample_data(data)
    theta_hat_i = statistic(jackknife_data, axis=-1)
    theta_hat_dot = theta_hat_i.mean(axis=-1)[..., None]
    num = ((theta_hat_dot - theta_hat_i)**3).sum(axis=-1)
    den = 6*((theta_hat_dot - theta_hat_i)**2).sum(axis=-1)**(3/2)
    a_hat = num / den

    # calculate alpha_1, alpha_2
    z_alpha = stats.norm.ppf(alpha)
    z_1alpha = -z_alpha
    num1 = z0_hat + z_alpha
    alpha_1 = stats.norm.cdf(z0_hat + num1/(1 - a_hat*(num1)))
    num2 = z0_hat + z_1alpha
    alpha_2 = stats.norm.cdf(z0_hat + num2/(1 - a_hat*(num2)))
    return alpha_1, alpha_2


def _bootstrap_ci_iv(data, statistic, axis, confidence_level, n_resamples,
                     method, random_state):
    """Input validation for bootstrap_ci"""

    axis_int = int(axis)
    if axis != axis_int:
        raise ValueError("`axis` must be an integer.")

    if not data:
        raise ValueError("`data` must be a sequence of samples.")

    data_iv = []
    for sample in data:
        sample = np.atleast_1d(sample)
        if sample.shape[axis] <= 1:
            raise ValueError("`data` must contain two or more observations "
                             "along `axis`.")
        sample = np.moveaxis(sample, axis_int, -1)
        data_iv.append(sample)

    # should we try: statistic(data, axis=axis) here?

    confidence_level_float = float(confidence_level)

    n_resamples_int = int(n_resamples)
    if n_resamples != n_resamples_int or n_resamples_int <= 0:
        raise ValueError("`n_resamples` must be a positive integer.")

    methods = {'percentile', 'bca'}
    method = method.lower()
    if method not in methods:
        raise ValueError(f"`method` must be in {methods}")

    random_state = check_random_state(random_state)

    return (data_iv, statistic, axis_int, confidence_level_float,
            n_resamples_int, method, random_state)


def bootstrap_ci(data, statistic, axis=0, confidence_level=0.95,
                 n_resamples=1000, method='bca', random_state=None):
    r"""
    Compute a two-sided bootstrap confidence interval of a statistic

    When `method` is ``'percentile'``, a bootstrap confidence interval is
    computed according to the following procedure.

    1. Resample the data: for each sample in `data` and for each of
       `n_resamples`, take a random sample of the original sample
       (with replacement) of the same size as the original sample.

    2. Compute the bootstrap distribution of the statistic: for each set of
       resamples, compute the test statistic.

    3. Find the interval of the bootstrap distribution that is

        - symmetric about the median and
        - contains `confidence_level` of the resampled statistic values.

    When `method` is ``'bca'``, the bias-corrected and accelerated
    interval [1]_ is used in step 3.

    If the samples in `data` are  taken at random from their respective
    distributions :math:`n` times, the confidence interval returned by
    `bootstrap_ci` will contain the true value of the statistic for those
    distributions approximately `confidence_level`:math:`\times n` times.

    Parameters
    ----------
    data : sequence of array-like
         Each element of data is a sample from an underlying distribution.
    statistic : callable
        Statistic for which the confidence interval is to be calculated.
        `statistic` must be a callable that accepts ``len(data)`` samples
        as separate arguments and returns the resulting statistic.
        ``statistic`` must also accept a keyword argument `axis` and be
        vectorized to compute the statistic along the provided `axis`.
    axis : int, optional
        The axis of the samples in `data` along which the `statistic` is
        calculated. The default is ``0``.
    confidence_level : float, optional
        The confidence level of the confidence interval.
        The default is ``0.95``.
    n_samples : int, optional
        The number of resamples performed to form the bootstrap distribution
        of the statistic. The default is ``10000``.
    method : str in {'percentile', 'bca'}, optional
        Whether to return the 'percentile' bootstrap confidence interval
        (``'percentile'``) or the bias-corrected and accelerated bootstrap
        confidence interval (``'bca'``). The default is 'bca'.
    random_state: int, RandomState, or Generator, optional
        Pseudorandom number generator state used to generate resamples.

    Returns
    -------
    ci_l : float
        The lower bound of the confidence interval.
    ci_u : float
        The upper bound of the confidence interval.

    References
    ----------
    .. [1] Nathaniel E. Helwig, "Bootstrap Confidence Intervals",
       http://users.stat.umn.edu/~helwig/notes/bootci-Notes.pdf

    Examples
    --------
    Suppose we have sampled data from an unknown distribution.

    >>> import numpy as np
    >>> np.random.seed(0)
    >>> from scipy.stats import norm
    >>> dist = norm(loc=2, scale = 4)  # our "unknown" distribution
    >>> data = dist.rvs(size=100)      # a random sample from the distribution

    We are interested int the standard deviation of the distribution.

    >>> std_true = dist.std()          # the true value of the statistic
    >>> print(std_true)
    4.0
    >>> std_sample = np.std(data)      # the sample statistic
    >>> print(std_sample)
    4.0315289788663184

    We can calculate a 90% confidence interval of the statistic using
    `bootstrap_ci`.

    >>> from scipy.stats import bootstrap_ci
    >>> data = (data,)  # samples must be in a sequence
    >>> ci_l, ci_u = bootstrap_ci(data, np.std, confidence_level=0.9)
    >>> print(ci_l, ci_u)
    3.6358417469634423 4.505860501007106

    If we sample from the distribution 1000 times and form a bootstrap
    confidence interval for each sample, the confidence interval
    contains the true value of the statistic approximately 900 times.

    >>> n_trials = 1000
    >>> ci_contains_true_std = 0
    >>> for i in range(n_trials):
    ...    data = (dist.rvs(size=100),)
    ...    ci = bootstrap_ci(data, np.std, confidence_level=0.9)
    ...    if ci[0] < std_true < ci[1]:
    ...        ci_contains_true_std+=1
    >>> print(ci_contains_true_std)
    891

    Rather than writing a loop, we can also determine the confidence intervals
    for all 1000 samples at once.

    >>> data = (dist.rvs(size=(n_trials, 100)),)
    >>> ci_l, ci_u = bootstrap_ci(data, np.std, axis=-1,
    ...                                 confidence_level=0.9)
    >>> print(np.sum((ci_l < std_true) & (std_true < ci_u)))
    885

    `bootstrap_ci` can also be used to estimate confidence intervals of
    multi-sample statistics, including those calculated by hypothesis
    tests. `scipy.stats.mood` perform's Mood's test for equal scale parameters,
    and it returns two outputs: a statistic, and a p-value. To get a
    confidence interval on the test statistic, we first wrap `scipy.stats.mood`
    in a function that accepts two sample arguments, accepts an `axis` keyword
    argument, and returns only the statistic.

    >>> from scipy.stats import mood
    >>> def my_statistic(sample1, sample2, axis):
    ...     statistic, _ = mood(sample1, sample2, axis=-1)
    ...     return statistic

    Here, we use the 'percentile' method with the default 95% confidence level.

    >>> np.random.seed(0)
    >>> sample1 = norm.rvs(scale=1, size=100)
    >>> sample2 = norm.rvs(scale=2, size=100)
    >>> data = (sample1, sample2)
    >>> ci = bootstrap_ci(data, my_statistic, method='percentile')
    >>> print(ci)
    (-8.14095008342057, -5.131676847309245)

    """
    # Input validation
    args = _bootstrap_ci_iv(data, statistic, axis, confidence_level,
                            n_resamples, method, random_state)
    data, statistic, axis, confidence_level = args[:4]
    n_resamples, method, random_state = args[4:]

    # Generate resamples
    resampled_data = []
    for sample in data:
        resample = _resample_data(sample, n_resamples=n_resamples,
                                  random_state=random_state)
        resampled_data.append(resample)

    # Compute bootstrap distribution of statistic
    theta_hat_b = statistic(*resampled_data, axis=-1)

    # Calculate percentile interval
    alpha = (1 - confidence_level)/2
    if method == 'bca':
        interval = _bca_interval(data, statistic, axis, alpha, theta_hat_b)
        percentile_fun = _percentile_along_axis
    else:
        interval = alpha, 1-alpha
        percentile_fun = lambda a, q: np.percentile(a=a, q=q, axis=-1)

    # Calculate confidence interval of statistic
    ci_l = percentile_fun(theta_hat_b, interval[0]*100)
    ci_u = percentile_fun(theta_hat_b, interval[1]*100)
    return ci_l, ci_u

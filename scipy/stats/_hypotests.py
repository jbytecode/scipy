from __future__ import division, print_function, absolute_import
from collections import namedtuple
import numpy as np
import warnings
from ._continuous_distns import chi2
from ._discrete_distns import poisson


Epps_Singleton_2sampResult = namedtuple('Epps_Singleton_2sampResult',
                                        ('statistic', 'pvalue'))


def epps_singleton_2samp(x, y, t=(0.4, 0.8)):
    """
    Compute the Epps-Singleton (ES) test statistic.

    Test the null hypothesis that two samples have the same underlying
    probability distribution.

    Parameters
    ----------
    x, y : array-like
        The two samples of observations to be tested. Input must not have more
        than one dimension. Samples can have different lengths.
    t : array-like, optional
        The points (t1, ..., tn) where the empirical characteristic function is
        to be evaluated. It should be positive distinct numbers. The default
        value (0.4, 0.8) is proposed in [1]_. Input must not have more than
        one dimension.

    Returns
    -------
    statistic : float
        The test statistic.
    pvalue : float
        The associated p-value based on the asymptotic chi2-distribution.

    See Also
    --------
    ks_2samp, anderson_ksamp

    Notes
    -----
    Testing whether two samples are generated by the same underlying
    distribution is a classical question in statistics. A widely used test is
    the Kolmogorov-Smirnov (KS) test which relies on the empirical
    distribution function. Epps and Singleton introduce a test based on the
    empirical characteristic function in [1]_.

    One advantage of the ES test compared to the KS test is that is does
    not assume a continuous distribution. In [1]_, the authors conclude
    that the test also has a higher power than the KS test in many
    examples. They recommend the use of the ES test for discrete samples as
    well as continuous samples with at least 25 observations each, whereas
    `anderson_ksamp` is recommended for smaller sample sizes in the
    continuous case.

    The p-value is computed from the asymptotic distribution of the test
    statistic which follows a `chi2` distribution. If the sample size of both
    `x` and `y` is below 25, the small sample correction proposed in [1]_ is
    applied to the test statistic.

    The default values of `t` are determined in [1]_ by considering
    various distributions and finding good values that lead to a high power
    of the test in general. Table III in [1]_ gives the optimal values for
    the distributions tested in that study. The values of `t` are scaled by
    the semi-interquartile range in the implementation, see [1]_.

    References
    ----------
    .. [1] T. W. Epps and K. J. Singleton, "An omnibus test for the two-sample
       problem using the empirical characteristic function", Journal of
       Statistical Computation and Simulation 26, p. 177--203, 1986.

    .. [2] S. J. Goerg and J. Kaiser, "Nonparametric testing of distributions
       - the Epps-Singleton two-sample test using the empirical characteristic
       function", The Stata Journal 9(3), p. 454--465, 2009.

    """

    x, y, t = np.asarray(x), np.asarray(y), np.asarray(t)
    # check if x and y are valid inputs
    if x.ndim > 1:
        raise ValueError('x must be 1d, but x.ndim equals {}.'.format(x.ndim))
    if y.ndim > 1:
        raise ValueError('y must be 1d, but y.ndim equals {}.'.format(y.ndim))
    nx, ny = len(x), len(y)
    if (nx < 5) or (ny < 5):
        raise ValueError('x and y should have at least 5 elements, but len(x) '
                         '= {} and len(y) = {}.'.format(nx, ny))
    if not np.isfinite(x).all():
        raise ValueError('x must not contain nonfinite values.')
    if not np.isfinite(y).all():
        raise ValueError('y must not contain nonfinite values.')
    n = nx + ny

    # check if t is valid
    if t.ndim > 1:
        raise ValueError('t must be 1d, but t.ndim equals {}.'.format(t.ndim))
    if np.less_equal(t, 0).any():
        raise ValueError('t must contain positive elements only.')

    # rescale t with semi-iqr as proposed in [1]; import iqr here to avoid
    # circular import
    from scipy.stats import iqr
    sigma = iqr(np.hstack((x, y))) / 2
    ts = np.reshape(t, (-1, 1)) / sigma

    # covariance estimation of ES test
    gx = np.vstack((np.cos(ts*x), np.sin(ts*x))).T  # shape = (nx, 2*len(t))
    gy = np.vstack((np.cos(ts*y), np.sin(ts*y))).T
    cov_x = np.cov(gx.T, bias=True)  # the test uses biased cov-estimate
    cov_y = np.cov(gy.T, bias=True)
    est_cov = (n/nx)*cov_x + (n/ny)*cov_y
    est_cov_inv = np.linalg.pinv(est_cov)
    r = np.linalg.matrix_rank(est_cov_inv)
    if r < 2*len(t):
        warnings.warn('Estimated covariance matrix does not have full rank. '
                      'This indicates a bad choice of the input t and the '
                      'test might not be consistent.')  # see p. 183 in [1]_

    # compute test statistic w distributed asympt. as chisquare with df=r
    g_diff = np.mean(gx, axis=0) - np.mean(gy, axis=0)
    w = n*np.dot(g_diff.T, np.dot(est_cov_inv, g_diff))

    # apply small-sample correction
    if (max(nx, ny) < 25):
        corr = 1.0/(1.0 + n**(-0.45) + 10.1*(nx**(-1.7) + ny**(-1.7)))
        w = corr * w

    p = chi2.sf(w, r)

    return Epps_Singleton_2sampResult(w, p)


def poisson_etest(k1, k2, n1, n2, diff=0, alternative='two-sided'):
    """
    Calculate E-test for the mean difference of two samples

    The test requires two samples coming from poisson distribution. This is a
    right-sided and two-sided test.

    Parameters
    ----------
    k1, k2 : int or float
        Count from the first and second samples respectively
    n1, n2 : int or float
        Sample size of each sample
    diff : int of float, optional
        The difference of mean between two samples under null hypothesis
    alternative : {'two-sided', 'greater'}, optional
        Whether to get p-value for two-sided hypothesis or right sided hypothesis.
        Right-sided test that mean from sample one is greater than sample two

    Returns
    -------
    pvalue : float
        The associated p-value based on estimated p-value of the standardized
        difference.

    Notes
    -----
    The Poisson distribution is commonly used to model many processes such as
    transactions per user. The usual test to compare difference between two
    means of Poisson samples is C-test, based on conditional distribution.
    Meanwhile the E-test is an unconditional test

    Based the author results [1]_, E-test is more powerful than C-test. The E-test
    is almost exact because the test exceed the nominal value only by negligible
    amount. Compared to C-test which produce smaller size than nominal value.

    References
    ----------
    .. [1]  https://userweb.ucs.louisiana.edu/~kxk4695/JSPI-04.pdf

    Examples
    --------
    >>> from scipy import stats

    Taken from Przyborowski and Wilenski (1940). Suppose that a purchaser wishes to
    test the number of dodder seeds (a weed) in a sack of clover seeds that he bought
    from a seed manufacturing company. A 100 g sample is drawn from a sack of clover
    seeds prior to being shipped to the purchaser. The sample is analyzed and found to
    contain no dodder seeds; that is, k1 = 0. Upon arrival, the purchaser also draws
    a 100 g sample from the sack. This time, three dodder seeds are found in the sample;
    that is, k2 = 3. The purchaser wishes to determine if the difference between the
    samples could not be due to chance.

    >>> stats.poisson_etest(0, 3, 100, 100)
    0.08837900929018155
    """

    if k1 < 0 or k2 < 0:
        raise ValueError('k1 and k2 should have values greater than or equal to 0')

    if n1 <= 0 or n2 <= 0:
        raise ValueError('n1 and n2 should have values greater than 0')

    if diff < 0:
        raise ValueError('diff can not have negative values')

    if alternative not in ['two-sided', 'greater']:
        raise ValueError("alternative should be one of {'two-sided', 'greater'}")

    lmbd_hat2 = (k1 + k2) / (n1 + n2) - diff * n1 / (n1 + n2)

    # based on paper explanation, we do not need to calculate p-value
    # if the `lmbd_hat2` less than or equals zero, see paper page 26 below eq. 3.6
    if lmbd_hat2 <= diff:
        return 1

    var = k1 / n1 ** 2 + k2 / n2 ** 2

    t_k1k2 = (k1 / n1 - k2 / n2 - diff) / np.sqrt(var)

    nlmbd_hat1 = n1 * (lmbd_hat2 + diff)
    nlmbd_hat2 = n2 * lmbd_hat2

    x1_lb, x1_ub = poisson.ppf([1e-10, 1 - 1e-10], nlmbd_hat1)
    x2_lb, x2_ub = poisson.ppf([1e-10, 1 - 1e-10], nlmbd_hat2)

    x1 = np.repeat(np.arange(x1_lb, x1_ub + 1), x2_ub - x2_lb + 1)
    x2 = np.resize(np.arange(x2_lb, x2_ub + 1), len(x1))

    prob_x1 = poisson.pmf(x1, nlmbd_hat1)
    prob_x2 = poisson.pmf(x2, nlmbd_hat2)

    lmbd_hat_x1 = x1 / n1
    lmbd_hat_x2 = x2 / n2

    diff_lmbd_x1x2 = lmbd_hat_x1 - lmbd_hat_x2 - diff
    var_x1x2 = lmbd_hat_x1 / n1 + lmbd_hat_x2 / n2

    if alternative == 'two-sided':
        t_x1x2 = np.divide(
            diff_lmbd_x1x2,
            np.sqrt(var_x1x2),
            out=np.zeros_like(diff_lmbd_x1x2),
            where=(np.abs(lmbd_hat_x1 - lmbd_hat_x2) > diff)
        )
        p_x1x2 = np.multiply(
            prob_x1,
            prob_x2,
            out=np.zeros_like(prob_x1),
            where=(np.abs(t_x1x2) >= np.abs(t_k1k2))
        )
    else:
        t_x1x2 = np.divide(
            diff_lmbd_x1x2,
            np.sqrt(var_x1x2),
            out=np.zeros_like(diff_lmbd_x1x2),
            where=(diff_lmbd_x1x2 > 0)
        )
        p_x1x2 = np.multiply(
            prob_x1,
            prob_x2,
            out=np.zeros_like(prob_x1),
            where=(t_x1x2 >= t_k1k2)
        )

    pvalue = np.sum(p_x1x2)

    return pvalue

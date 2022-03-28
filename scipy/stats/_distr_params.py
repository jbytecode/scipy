"""
Sane parameters for stats.distributions.
"""
import numpy as np

distcont = [
    ['alpha', (3.5704770516650459,)],
    ['anglit', ()],
    ['arcsine', ()],
    ['argus', (1.0,)],
    ['beta', (2.3098496451481823, 0.62687954300963677)],
    ['betaprime', (5, 6)],
    ['bradford', (0.29891359763170633,)],
    ['burr', (10.5, 4.3)],
    ['burr12', (10, 4)],
    ['cauchy', ()],
    ['chi', (78,)],
    ['chi2', (55,)],
    ['cosine', ()],
    ['crystalball', (2.0, 3.0)],
    ['dgamma', (1.1023326088288166,)],
    ['dweibull', (2.0685080649914673,)],
    ['erlang', (10,)],
    ['expon', ()],
    ['exponnorm', (1.5,)],
    ['exponpow', (2.697119160358469,)],
    ['exponweib', (2.8923945291034436, 1.9505288745913174)],
    ['f', (29, 18)],
    ['fatiguelife', (29,)],   # correction numargs = 1
    ['fisk', (3.0857548622253179,)],
    ['foldcauchy', (4.7164673455831894,)],
    ['foldnorm', (1.9521253373555869,)],
    ['gamma', (1.9932305483800778,)],
    ['gausshyper', (13.763771604130699, 3.1189636648681431,
                    2.5145980350183019, 5.1811649903971615)],  # veryslow
    ['genexpon', (9.1325976465418908, 16.231956600590632, 3.2819552690843983)],
    ['genextreme', (-0.1,)],
    ['gengamma', (4.4162385429431925, 3.1193091679242761)],
    ['gengamma', (4.4162385429431925, -3.1193091679242761)],
    ['genhalflogistic', (0.77274727809929322,)],
    ['genhyperbolic', (0.5, 1.5, -0.5,)],
    ['geninvgauss', (2.3, 1.5)],
    ['genlogistic', (0.41192440799679475,)],
    ['gennorm', (1.2988442399460265,)],
    ['halfgennorm', (0.6748054997000371,)],
    ['genpareto', (0.1,)],   # use case with finite moments
    ['gilbrat', ()],
    ['gompertz', (0.94743713075105251,)],
    ['gumbel_l', ()],
    ['gumbel_r', ()],
    ['halfcauchy', ()],
    ['halflogistic', ()],
    ['halfnorm', ()],
    ['hypsecant', ()],
    ['invgamma', (4.0668996136993067,)],
    ['invgauss', (0.14546264555347513,)],
    ['invweibull', (10.58,)],
    ['johnsonsb', (4.3172675099141058, 3.1837781130785063)],
    ['johnsonsu', (2.554395574161155, 2.2482281679651965)],
    ['kappa4', (0.0, 0.0)],
    ['kappa4', (-0.1, 0.1)],
    ['kappa4', (0.0, 0.1)],
    ['kappa4', (0.1, 0.0)],
    ['kappa3', (1.0,)],
    ['ksone', (1000,)],  # replace 22 by 100 to avoid failing range, ticket 956
    ['kstwo', (10,)],
    ['kstwobign', ()],
    ['laplace', ()],
    ['laplace_asymmetric', (2,)],
    ['levy', ()],
    ['levy_l', ()],
    ['levy_stable', (1.8, -0.5)],
    ['loggamma', (0.41411931826052117,)],
    ['logistic', ()],
    ['loglaplace', (3.2505926592051435,)],
    ['lognorm', (0.95368226960575331,)],
    ['loguniform', (0.01, 1.25)],
    ['log_uniform', (125,)],
    ['lomax', (1.8771398388773268,)],
    ['maxwell', ()],
    ['mielke', (10.4, 4.6)],
    ['moyal', ()],
    ['nakagami', (4.9673794866666237,)],
    ['ncf', (27, 27, 0.41578441799226107)],
    ['nct', (14, 0.24045031331198066)],
    ['ncx2', (21, 1.0560465975116415)],
    ['norm', ()],
    ['norminvgauss', (1.25, 0.5)],
    ['pareto', (2.621716532144454,)],
    ['pearson3', (0.1,)],
    ['powerlaw', (1.6591133289905851,)],
    ['powerlognorm', (2.1413923530064087, 0.44639540782048337)],
    ['powernorm', (4.4453652254590779,)],
    ['rayleigh', ()],
    ['rdist', (1.6,)],
    ['recipinvgauss', (0.63004267809369119,)],
    ['reciprocal', (0.01, 1.25)],
    ['rice', (0.7749725210111873,)],
    ['semicircular', ()],
    ['skewcauchy', (0.5,)],
    ['skewnorm', (4.0,)],
    ['studentized_range', (3.0, 10.0)],
    ['t', (2.7433514990818093,)],
    ['trapezoid', (0.2, 0.8)],
    ['triang', (0.15785029824528218,)],
    ['truncexpon', (4.6907725456810478,)],
    ['truncnorm', (-1.0978730080013919, 2.7306754109031979)],
    ['truncnorm', (0.1, 2.)],
    ['truncweibull_min', (2.5, 0.25, 1.75)],
    ['tukeylambda', (3.1321477856738267,)],
    ['uniform', ()],
    ['vonmises', (3.9939042581071398,)],
    ['vonmises_line', (3.9939042581071398,)],
    ['wald', ()],
    ['weibull_max', (2.8687961709100187,)],
    ['weibull_min', (1.7866166930421596,)],
    ['wrapcauchy', (0.031071279018614728,)]]


distdiscrete = [
    ['bernoulli',(0.3,)],
    ['betabinom', (5, 2.3, 0.63)],
    ['binom', (5, 0.4)],
    ['boltzmann',(1.4, 19)],
    ['dlaplace', (0.8,)],  # 0.5
    ['geom', (0.5,)],
    ['hypergeom',(30, 12, 6)],
    ['hypergeom',(21,3,12)],  # numpy.random (3,18,12) numpy ticket:921
    ['hypergeom',(21,18,11)],  # numpy.random (18,3,11) numpy ticket:921
    ['nchypergeom_fisher', (140, 80, 60, 0.5)],
    ['nchypergeom_wallenius', (140, 80, 60, 0.5)],
    ['logser', (0.6,)],  # re-enabled, numpy ticket:921
    ['nbinom', (0.4, 0.4)],  # from tickets: 583
    ['nbinom', (5, 0.5)],
    ['planck', (0.51,)],   # 4.1
    ['poisson', (0.6,)],
    ['randint', (7, 31)],
    ['skellam', (15, 8)],
    ['zipf', (6.5,)],
    ['zipfian', (0.75, 15)],
    ['zipfian', (1.25, 10)],
    ['yulesimon', (11.0,)],
    ['nhypergeom', (20, 7, 1)]
]


invdistdiscrete = [
    # In each of the following, at least one shape parameter is invalid
    ['hypergeom', (3, 3, 4)],
    ['nhypergeom', (5, 2, 8)],
    ['nchypergeom_fisher', (3, 3, 4, 1)],
    ['nchypergeom_wallenius', (3, 3, 4, 1)],
    ['bernoulli', (1.5, )],
    ['binom', (10, 1.5)],
    ['betabinom', (10, -0.4, -0.5)],
    ['boltzmann', (-1, 4)],
    ['dlaplace', (-0.5, )],
    ['geom', (1.5, )],
    ['logser', (1.5, )],
    ['nbinom', (10, 1.5)],
    ['planck', (-0.5, )],
    ['poisson', (-0.5, )],
    ['randint', (5, 2)],
    ['skellam', (-5, -2)],
    ['zipf', (-2, )],
    ['yulesimon', (-2, )],
    ['zipfian', (-0.75, 15)]
]


invdistcont = [
    # In each of the following, at least one shape parameter is invalid
    ['alpha', (-1, )],
    ['anglit', ()],
    ['arcsine', ()],
    ['argus', (-1, )],
    ['beta', (-2, 2)],
    ['betaprime', (-2, 2)],
    ['bradford', (-1, )],
    ['burr', (-1, 1)],
    ['burr12', (-1, 1)],
    ['cauchy', ()],
    ['chi', (-1, )],
    ['chi2', (-1, )],
    ['cosine', ()],
    ['crystalball', (-1, 2)],
    ['dgamma', (-1, )],
    ['dweibull', (-1, )],
    ['erlang', (-1, )],
    ['expon', ()],
    ['exponnorm', (-1, )],
    ['exponweib', (1, -1)],
    ['exponpow', (-1, )],
    ['f', (10, -10)],
    ['fatiguelife', (-1, )],
    ['fisk', (-1, )],
    ['foldcauchy', (-1, )],
    ['foldnorm', (-1, )],
    ['genlogistic', (-1, )],
    ['gennorm', (-1, )],
    ['genpareto', (np.inf, )],
    ['genexpon', (1, 2, -3)],
    ['genextreme', (np.inf, )],
    ['genhyperbolic', (0.5, -0.5, -1.5,)],
    ['gausshyper', (1, 2, 3, -4)],
    ['gamma', (-1, )],
    ['gengamma', (-1, 0)],
    ['genhalflogistic', (-1, )],
    ['geninvgauss', (1, 0)],
    ['gilbrat', ()],
    ['gompertz', (-1, )],
    ['gumbel_r', ()],
    ['gumbel_l', ()],
    ['halfcauchy', ()],
    ['halflogistic', ()],
    ['halfnorm', ()],
    ['halfgennorm', (-1, )],
    ['hypsecant', ()],
    ['invgamma', (-1, )],
    ['invgauss', (-1, )],
    ['invweibull', (-1, )],
    ['johnsonsb', (1, -2)],
    ['johnsonsu', (1, -2)],
    ['kappa4', (np.nan, 0)],
    ['kappa3', (-1, )],
    ['ksone', (-1, )],
    ['kstwo', (-1, )],
    ['kstwobign', ()],
    ['laplace', ()],
    ['laplace_asymmetric', (-1, )],
    ['levy', ()],
    ['levy_l', ()],
    ['levy_stable', (-1, 1)],
    ['logistic', ()],
    ['loggamma', (-1, )],
    ['loglaplace', (-1, )],
    ['lognorm', (-1, )],
    ['loguniform', (10, 5)],
    ['log_uniform', (0.5,)],
    ['lomax', (-1, )],
    ['maxwell', ()],
    ['mielke', (1, -2)],
    ['moyal', ()],
    ['nakagami', (-1, )],
    ['ncx2', (-1, 2)],
    ['ncf', (10, 20, -1)],
    ['nct', (-1, 2)],
    ['norm', ()],
    ['norminvgauss', (5, -10)],
    ['pareto', (-1, )],
    ['pearson3', (np.nan, )],
    ['powerlaw', (-1, )],
    ['powerlognorm', (1, -2)],
    ['powernorm', (-1, )],
    ['rdist', (-1, )],
    ['rayleigh', ()],
    ['rice', (-1, )],
    ['recipinvgauss', (-1, )],
    ['semicircular', ()],
    ['skewnorm', (np.inf, )],
    ['studentized_range', (-1, 1)],
    ['t', (-1, )],
    ['trapezoid', (0, 2)],
    ['triang', (2, )],
    ['truncexpon', (-1, )],
    ['truncnorm', (10, 5)],
    ['truncweibull_min', (-2.5, 0.25, 1.75)],
    ['tukeylambda', (np.nan, )],
    ['uniform', ()],
    ['vonmises', (-1, )],
    ['vonmises_line', (-1, )],
    ['wald', ()],
    ['weibull_min', (-1, )],
    ['weibull_max', (-1, )],
    ['wrapcauchy', (2, )],
    ['reciprocal', (15, 10)],
    ['skewcauchy', (2, )]
]

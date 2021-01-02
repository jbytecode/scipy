# distutils: language = c++

from .biasedurn cimport CFishersNCHypergeometric, StochasticLib3
import numpy as np
from numpy.random cimport bitgen_t
# from numpy.random.mtrand cimport RandomState
from cpython.pycapsule cimport PyCapsule_GetPointer, PyCapsule_IsValid

cdef class _PyFishersNCHypergeometric:
    cdef CFishersNCHypergeometric c_fnch

    def __cinit__(self, int n, int m, int N, double odds, double accuracy):
        self.c_fnch = CFishersNCHypergeometric(n, m, N, odds, accuracy)

    def mode(self):
        return self.c_fnch.mode()

    def mean(self):
        return self.c_fnch.mean()

    def variance(self):
        return self.c_fnch.variance()

    def probability(self, int x):
        return self.c_fnch.probability(x)

    def moments(self):
        cdef double mean, var
        self.c_fnch.moments(&mean, &var)
        return mean, var


cdef bitgen_t* make_rng(random_state=None):
    # get a bit_generator object
    if random_state is None or isinstance(random_state, int):
        bg = np.random.RandomState(random_state)._bit_generator
    elif isinstance(random_state, np.random.RandomState):
        bg = random_state._bit_generator
    elif isinstance(random_state, np.random.Generator):
        bg = random_state.bit_generator
    else:
        raise ValueError('random_state is not in {None, int, RandomState, Generator}')

    # get the bitgen_t pointer
    cdef const char *capsule_name = "BitGenerator"
    capsule = bg.capsule
    if not PyCapsule_IsValid(capsule, capsule_name):
        raise ValueError("Invalid pointer to anon_func_state")
    cdef bitgen_t* crng = <bitgen_t *> PyCapsule_GetPointer(capsule, capsule_name)
    return crng


cdef class _PyStochasticLib3:
    cdef StochasticLib3 c_sl3

    def __cinit__(self):
        self.c_sl3 = StochasticLib3(0)

    def Random(self):
        return self.c_sl3.Random();

    def SetAccuracy(self, double accur):
        return self.c_sl3.SetAccuracy(accur)

    def rvs_fisher(self, int n, int m, int N, double odds, int size, random_state=None):
        # handle random state
        self.c_sl3.SetBitGen(make_rng(random_state))

        # call for each
        rvs = np.empty(size, dtype=np.float64)
        for ii in range(size):
            rvs[ii] = self.c_sl3.FishersNCHyp(n, m, N, odds)
        return rvs

    def FishersNCHyp(self, int n, int m, int N, double odds):
        self.c_sl3.SetBitGen(make_rng())  # get default rng
        return self.c_sl3.FishersNCHyp(n, m, N, odds)

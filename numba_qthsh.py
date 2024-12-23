import ctypes as ct
import numba as nb
import numpy as np
import os

# define the signature of the input function 
qthsh_sig = nb.types.double(nb.types.double, \
                    nb.types.CPointer(nb.types.double))

# load the shared object and define its signature and the output type
rootdir = os.path.dirname(os.path.realpath(__file__))+'/'
libqthsh = ct.CDLL(rootdir+'qthsh.so')
qthsh_ = libqthsh.qthsh
qthsh_.argtypes = [ct.c_void_p, ct.c_double, ct.c_double, ct.c_int, \
                                         ct.c_double, ct.c_void_p, ct.c_void_p]
qthsh_.restype = ct.c_double

@nb.njit()
def qthsh(funcptr, a, b, n=6, eps=1e-09, data=np.array([0.0], np.float64)):
    """Tanh-Sinh approximation of the integral of analytical function f.
        Adapted from https://www.genivia.com/qthsh.html.
        Inputs:
            <*func<double, *double>> - pointer to a function to be integrated,
                                        the function must accept two inputs
                                        first one corresponding to the variable
                                        of integration and the second one
                                        corresponding to the pointer to the
                                        array of any other input data required
            <float>                  - lower bound of integration
            <float>                  - upper bound of integration
            <int>                    - level, an integer
                                        (default 6 -- recommended)
            <float>                  - desired precision
                                        (default 1e-09 -- recommended)
            <array<float>>           - array of any other input data passed
                                        through to the integrated function
        Outputs:
            <float>                  - result of the numerical integration
            <float>                  - en estimate of a relative error in the
                                        approximation of the integral"""
    err = np.array(0.0, np.float64)
    sol = qthsh_(funcptr, a, b, n, eps, data.ctypes.data, err.ctypes.data)
    return sol, err.item()

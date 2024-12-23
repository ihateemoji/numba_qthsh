from numba_qthsh import qthsh, qthsh_sig
import numba as nb
import numpy as np
import math

#------------------------------TEST FUNCTIONS---------------------------------#
"""Single integral with pole at zero -- expect 2"""
@nb.cfunc(qthsh_sig)
def f1(x, args_):
    return x**(-1/2)
f1_ptr = f1.address

"""Simple double integral -- expect about 0.781302"""
@nb.cfunc(qthsh_sig)
def f2_level1(x, args_):
    args = nb.carray(args_, (1,))
    y = args[0]
    return (1+x*y+x**2*y**2)**(-1)
f2_level1_ptr = f2_level1.address
@nb.cfunc(qthsh_sig)
def f2(y, args_):
    return qthsh(f2_level1_ptr, 0, 1, data=np.array([y], np.float64))[0]
f2_ptr = f2.address

"""Integration over narrow resonance -- expect about 95.35120322775237"""
@nb.cfunc(qthsh_sig)
def f3(x, args_):
    return ((x-0.5)**2+1e-03)**(-1)
f3_ptr = f3.address
#-----------------------------------------------------------------------------#

# print results of integration
print(qthsh(f1_ptr, 0, 1))
print(qthsh(f2_ptr, 0, 1))
print(qthsh(f3_ptr, 0, 1))

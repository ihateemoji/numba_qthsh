import numba as nb
import numpy as np
from numba_qthsh import qthsh, qthsh_sig

@nb.cfunc(qthsh_sig)
def f1(x, args_):
    return (1-x)**(-0.8)
f1_ptr = f1.address

@nb.cfunc(qthsh_sig)
def f2_level1(x, args_):
    # Convert the args_ pointer to a Numba array
    args = nb.carray(args_, (1,))
    y = args[0]
    return (1 + x * y + x**2 * y**2)**(-1)
f2_level1_ptr = f2_level1.address
@nb.cfunc(qthsh_sig)
def f2(y, args_):
    return qthsh(f2_level1_ptr, 0, 1, data=np.array([y], np.float64))[0]
f2_ptr = f2.address

def test_example1():
    assert qthsh(f1_ptr, 0, 1) == (4.997295850834395, 5.06627157291822e-06)
def test_example1_extra():
    assert qthsh(f1_ptr, 0, 1, n=15, eps=1e-15) == (4.997462936822409, 2.4813017661657574e-08)
def test_example2():
    assert qthsh(f2_ptr, 0, 1) == (0.7813024128964848, 1.0373228016881988e-14)

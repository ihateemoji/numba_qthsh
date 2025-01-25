import pytest
import numba as nb
import numpy as np
from numba_qthsh import qthsh, qthsh_sig

# Define test functions
@nb.cfunc(qthsh_sig, error_model="numpy")
def linear_func(x, data):
    return x

@nb.cfunc(qthsh_sig, error_model="numpy")
def quadratic_func(x, data):
    return x * x

@nb.cfunc(qthsh_sig, error_model="numpy")
def sine_func(x, data):
    return np.sin(x)

@nb.cfunc(qthsh_sig, error_model="numpy")
def exponential_func(x, data):
    return np.exp(-abs(x))

@nb.cfunc(qthsh_sig, error_model="numpy")
def gaussian_func(x, data):
    return np.exp(-x * x)

@nb.cfunc(qthsh_sig, error_model="numpy")
def reciprocal_func(x, data):
    return 1.0 / x**(1/2)

@nb.cfunc(qthsh_sig, error_model="numpy")
def log_func(x, data):
    return np.log(x)

@nb.cfunc(qthsh_sig)
def dblinteg_func_level1(x, args_):
    args = nb.carray(args_, (1,))
    y = args[0]
    return (1 + x * y + x**2 * y**2)**(-1)
dblinteg_func_level1_ptr = dblinteg_func_level1.address
@nb.cfunc(qthsh_sig)
def dblinteg_func(y, args_):
    return qthsh(dblinteg_func_level1_ptr, 0, 1, data=np.array([y], np.float64))[0]

# Run the tests
def test_linear_function():
    result, error = qthsh(linear_func.address, 0.0, 1.0)
    assert pytest.approx(result, abs=1e-6) == 0.5
    assert error < 1e-6

def test_quadratic_function():
    result, error = qthsh(quadratic_func.address, 0.0, 1.0)
    assert pytest.approx(result, abs=1e-6) == 1.0 / 3.0
    assert error < 1e-6

def test_sine_function():
    result, error = qthsh(sine_func.address, 0.0, np.pi)
    assert pytest.approx(result, abs=1e-6) == 2.0
    assert error < 1e-6

def test_exponential_function():
    result, error = qthsh(exponential_func.address, 0.0, 1.0)
    assert pytest.approx(result, abs=1e-6) == 1 - np.exp(-1)
    assert error < 1e-6

def test_gaussian_function():
    result, error = qthsh(gaussian_func.address, -np.inf, np.inf)
    assert pytest.approx(result, abs=1e-6) == np.sqrt(np.pi)
    assert error < 1e-6

def test_swapped_bounds():
    result, error = qthsh(linear_func.address, 1.0, 0.0)
    assert pytest.approx(result, abs=1e-6) == -0.5
    assert error < 1e-6

def test_finite_to_infinite():
    result, error = qthsh(exponential_func.address, 0.0, np.inf)
    assert pytest.approx(result, abs=1e-6) == 1.0
    assert error < 1e-6

def test_finite_to_infinite1():
    result, error = qthsh(gaussian_func.address, 2, np.inf)
    assert pytest.approx(result, abs=1e-6) == 0.004145534690336334
    assert error < 1e-6

def test_infinite_to_finite():
    result, error = qthsh(exponential_func.address, -np.inf, 0.0)
    assert pytest.approx(result, abs=1e-6) == 1.0
    assert error < 1e-6

def test_infinite_to_finite():
    result, error = qthsh(exponential_func.address, -np.inf, -4)
    assert pytest.approx(result, abs=1e-6) == 0.01831563888873418
    assert error < 1e-6

def test_reciprocal_function():
    result, error = qthsh(reciprocal_func.address, 0.0, 1.0)
    assert pytest.approx(result, abs=1e-6) == 2.0
    assert error < 1e-6

def test_log_function():
    result, error = qthsh(log_func.address, 0.0, 1.0)
    assert pytest.approx(result, abs=1e-6) == -1.0
    assert error < 1e-6

def test_dblinteg():
    result, error = qthsh(dblinteg_func.address, 0.0, 1.0)
    assert pytest.approx(result, abs=1e-6) == 0.7813024128964874
    assert error < 1e-6

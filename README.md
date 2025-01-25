# numba_qthsh

[![Python package](https://github.com/ihateemoji/numba_qthsh/actions/workflows/python-package.yml/badge.svg)](https://github.com/ihateemoji/numba_qthsh/actions/workflows/python-package.yml)

`numba_qthsh` is a Python package that integrates the C implementation of the tanh-sinh quadrature with Numba.

## Installation

### Linux and macOS

To install `numba_qthsh` on Linux or macOS, clone the repository and install the package using pip:

```bash
git clone https://github.com/ihateemoji/numba_qthsh.git
cd numba_qthsh
pip install .
```

### Windows

Installation instructions for Windows are not provided. Users are encouraged to figure it out on their own. If you manage to install it on Windows, please consider opening a pull request with the installation instructions as I do not have a Windows machine available.

## Usage

The tanh-sinh quadrature is particularly effective for handling integrals with singularities. This can be done by ensuring that the singularity is placed on the edge of the domain of integration.

Here is a snippet of Python code that performs the integral of (1-x)^{-0.8} between 0 and 1 (note the integrable singularity at x = 0):

```python
import numba as nb
from numba_qthsh import qthsh, qthsh_sig

@nb.cfunc(qthsh_sig)
def f1(x, args_):
    return (1-x)**(-0.8)

f1_ptr = f1.address
print(qthsh(f1_ptr, 0, 1))
```

### Optional Inputs

The `qthsh` function has several optional inputs that allow for more control over the integration process. The function's signature is as follows:

```python
def qthsh(func_ptr, lower_bound, upper_bound, level=6, precision=1e-09, data=None):
    """
    Tanh-Sinh approximation of the integral of an analytical function.
    Adapted from https://www.genivia.com/qthsh.html.

    Inputs:
        <*func<double, *double>> - pointer to a function to be integrated,
                                    the function must accept two inputs:
                                    - first one corresponding to the variable
                                      of integration
                                    - second one corresponding to the pointer
                                      to the array of any other input data required
        <float>                  - lower bound of integration
        <float>                  - upper bound of integration
        <int>                    - level, an integer (default is 6 -- recommended)
        <float>                  - desired precision (default is 1e-09 -- recommended)
        <array<float>>           - array of any other input data passed through
                                    to the integrated function
    Outputs:
        <float>                  - result of the numerical integration
        <float>                  - an estimate of the relative error in the
                                    approximation of the integral
    """
```


## Examples

### Example 1: Basic Integration

```python
import numba as nb
from numba_qthsh import qthsh, qthsh_sig

@nb.cfunc(qthsh_sig)
def basic_integral(x, args_):
    return x**2

basic_integral_ptr = basic_integral.address
result = qthsh(basic_integral_ptr, 0, 1)
print("Integral of x^2 from 0 to 1:", result)
```

### Example 2: Double Integral with Data Passing

This advanced example demonstrates how to perform a double integral, where the data from the outer integral function is passed into the inner integral function.

```python
import numba as nb
import numpy as np
from numba_qthsh import qthsh, qthsh_sig

# Define the first-level integrand function
@nb.cfunc(qthsh_sig)
def f2_level1(x, args_):
    # Convert the args_ pointer to a Numba array
    args = nb.carray(args_, (1,))
    y = args[0]
    # Calculate the integrand value
    return (1 + x * y + x**2 * y**2)**(-1)

# Get the function pointer for the first-level integrand
f2_level1_ptr = f2_level1.address

# Define the second-level integrand function
@nb.cfunc(qthsh_sig)
def f2(y, args_):
    # Perform the inner integral using the first-level integrand
    # Pass the current value of y as data to the inner integrand
    return qthsh(f2_level1_ptr, 0, 1, data=np.array([y], np.float64))[0]

# Get the function pointer for the second-level integrand
f2_ptr = f2.address

# Perform the outer integral
result = qthsh(f2_ptr, 0, 1)

# Print the result of the double integral
print("Result of the double integral:", result)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Credits

This project uses the C implementation of the tanh-sinh quadrature adapted from [Robert-van-Engelen/Tanh-Sinh](https://github.com/Robert-van-Engelen/Tanh-Sinh), which is published under the MIT license.

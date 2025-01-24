# numba_qthsh

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

Installation instructions for Windows are not provided. Users are encouraged to figure it out on their own.

## Usage

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
```

Feel free to copy this markdown code into your README.md file. If you need any further modifications, let me know!

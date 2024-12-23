#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define FUDGE1 10
#define FUDGE2 1

// integrate function f, range a..b, max levels n (6 is recommended), 
// relative error tolerance eps, estimated relative error err
double qthsh(double (*f)(double, double*), double a, double b, int n, 
                                double eps, double* data, double* err) {
  // qthsh: Tanh-Sinh quadrature formula
  // adapted from https://www.genivia.com/qthsh.html
  const double tol = FUDGE1*eps;
  double c = (a+b)/2;
  double d = (b-a)/2;
  double s = (*f)(c, data);
  double v, h = 2;
  int k = 0;
  do {
    double p = 0, q, fp = 0, fm = 0, t, eh;
    h /= 2;
    eh = exp(h);
    t = eh;
    if (k > 0)
      eh *= eh;
    do {
      double u = exp(1/t-t);      // = exp(-2*sinh(j*h)) = 1/exp(sinh(j*h))^2
      double r = 2*u/(1+u);       // = 1 - tanh(sinh(j*h))
      double w = (t+1/t)*r/(1+u); // = cosh(j*h)/cosh(sinh(j*h))^2
      double x = d*r;
      if (a+x > a) {              // if too close to a then reuse previous fp
        double y = (*f)(a+x, data);
        if (isfinite(y))
          fp = y;                 // if f(x) is finite, add to local sum
      }
      if (b-x < b) {              // if too close to b then reuse previous fm
        double y = (*f)(b-x, data);
        if (isfinite(y))
          fm = y;                 // if f(x) is finite, add to local sum
      }
      q = w*(fp+fm);
      p += q;
      t *= eh;
    } while (fabs(q) > eps*fabs(p));
    v = s-p;
    s += p;
    ++k;
  } while (fabs(v) > tol*fabs(s) && k <= n);
  // result with estimated relative error err
  *err = fabs(v)/(FUDGE2*fabs(s)+eps);
  return d*s*h;
}

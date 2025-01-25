#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define FUDGE1 10
#define FUDGE2 1

// integrate function f, range a..b, max levels n (6 is recommended), 
// relative error tolerance eps, estimated relative error err
double qthsh_main(double (*f)(double, double*), double a, double b, int n, 
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

double qthsh(double (*f)(double, double*), double a, double b, int n, 
                                double eps, double* data, double* err) {
    /* Wrapper of the qthsh quadrature */ 
    double temp = 0.0;
    double sign = 1.0;
    double out = 0.0;
    /* take care of the case if the bounds are swapped */
    if (b < a) { temp = b; b = a; a = temp; sign = -1.0*sign; }
    /* compute the integral is both bounds are finite */
    if (isfinite(a) && isfinite(b)) {
        out = sign*qthsh_main(f, a, b, n, eps, data, err);
    }
    /* if both bounds are infinite we split and do and do x=1/y-1 transform */
    if (!isfinite(a) && !isfinite(b)) {
        double integ1 = 0.0;
        double integ2 = 0.0;
        double err1 = 0.0;
        double err2 = 0.0;
        double g1(double y, double* data) {
            double x = 1.0/y - 1.0;
            double dx = 1.0/(y*y);
            return (*f)(x, data)*dx;
        }
        double g2(double y, double* data) {
            double x = 1.0/y - 1.0;
            double dx = 1.0/(y*y);
            return (*f)(-1.0*x, data)*dx;
        }
        /* do backwards and forewords integrals and propagate the error */
        integ1 = qthsh_main(&g1, 0.0, 1.0, n, eps, data, &err1);
        integ2 = qthsh_main(&g2, 0.0, 1.0, n, eps, data, &err2);
        *err = sqrt(err1*err1 + err2*err2);
        out = sign*(integ1 + integ2);
    } 
    /* if top bound is infinite we do x=1/y-1+a transform */
    else if (!isfinite(b)) {
        double g1(double y, double* data) {
            double x = 1.0/y - 1.0 + a;
            double dx = 1.0/(y*y);
            return (*f)(x, data)*dx;
        }
        out = sign*qthsh_main(&g1, 0.0, 1.0, n, eps, data, err);
    } 
    /* if bottom bound is infinite we do x=1/y-1-b transform and reflect,
        this is an only possible case left */
    else if (!isfinite(a)) {
        double g1(double y, double* data) {
            double x = 1.0/y - 1.0 - b;
            double dx = 1.0/(y*y);
            return (*f)(-1.0*x, data)*dx;
        }
        out = sign*qthsh_main(&g1, 0.0, 1.0, n, eps, data, err);
    }
    return out;
}

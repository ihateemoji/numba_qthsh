#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define FUDGE1 10
#define FUDGE2 1

// struct used to pass data for the change of integration variable
typedef struct {
    double (*f)(double, double*);
    double a, b;
    double* orig_data;
} qthsh_ctx;

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

// integrand function with changed variable for improper integrals
double g1_infinite(double y, double* data) {
    qthsh_ctx* ctx = (qthsh_ctx*)data;
    double x = (1.0 - y) / y - y / (1.0 - y);
    double dx = 1.0 / ((y - 1.0) * (y - 1.0)) + 1.0 / (y * y);
    return ctx->f(x, ctx->orig_data) * dx;
}
double g1_upper(double y, double* data) {
    qthsh_ctx* ctx = (qthsh_ctx*)data;
    double x = 1.0 / y - 1.0 + ctx->a;
    double dx = 1.0 / (y * y);
    return ctx->f(x, ctx->orig_data) * dx;
}
double g1_lower(double y, double* data) {
    qthsh_ctx* ctx = (qthsh_ctx*)data;
    double x = 1.0 / y - 1.0 - ctx->b;
    double dx = 1.0 / (y * y);
    return ctx->f(-1.0 * x, ctx->orig_data) * dx;
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
    /* if both bounds are infinite we do x=(1-y)/y - y/(1-y) transform */
    else if (!isfinite(a) && !isfinite(b)) {
        qthsh_ctx ctx = {f, a, b, data};
        out = sign * 
                qthsh_main(g1_infinite, 0.0, 1.0, n, eps, (double*)&ctx, err);
    } 
    /* if top bound is infinite we do x=1/y-1+a transform */
    else if (!isfinite(b)) {
        qthsh_ctx ctx = {f, a, b, data};
        out = sign * 
                qthsh_main(g1_upper, 0.0, 1.0, n, eps, (double*)&ctx, err);
    } 
    /* if bottom bound is infinite we do x=1/y-1-b transform and reflect,
        this is an only possible case left */
    else if (!isfinite(a)) {
        qthsh_ctx ctx = {f, a, b, data};
        out = sign * 
                qthsh_main(g1_lower, 0.0, 1.0, n, eps, (double*)&ctx, err);
    }
    return out;
}

"""Operations on sequences of i.i.d. variables."""

import operator

import pacal.distr
from pacal.utils import binomial_coeff
from pacal.standard_distr import PDistr, FunDistr

from pacal import params

def _int_exp(x, n, op = operator.mul):
    """Right to left exponentiation by squaring."""
    res = None
    for b in bin(n)[2:]:
        if res is not None:
            res = op(res, res)
        if b == "1":
            if res is not None:
                res = op(res, x)
            else:
                res = x
    return res
def _int_exp_all(x, n, op = operator.mul):
    """Exponentiation by squaring returning all powers."""
    res = [None] * (n+1)
    res[1] = x
    for i in xrange(2, n+1):
        res[i] = op(res[i // 2], res[i - i // 2])
    return res[1:]

def iid_op(X, n, op, all = False):
    old_warn = params.general.warn_on_dependent
    params.general.warn_on_dependent = False
    if all:
        y = _int_exp_all(X, n, op)
    else:
        y = _int_exp(X, n, op)
    params.general.warn_on_dependent = old_warn
    return y
def iid_sum(X, n, all = False):
    return iid_op(X, n, op = operator.add, all = all)
def iid_prod(X, n, all = False):
    return iid_op(X, n, op = operator.mul, all = all)
def iid_min(X, n, all = False):
    return iid_op(X, n, op = pacal.distr.min, all = all)
def iid_max(X, n, all = False):
    return iid_op(X, n, op = pacal.distr.max, all = all)

def iid_order_stat(X, n, k, **kwargs):
    pdf = X.get_piecewise_pdf()
    cdf = X.get_piecewise_cdf()
    ccdf = 1 - X.get_piecewise_cdf()
    fun = (k * binomial_coeff(n, k)) * pdf * (pow(cdf, k-1) * pow(ccdf, n-k))
    #return PDistr(fun.toInterpolated())
    return FunDistr(fun=fun.toInterpolated(), breakPoints=X.get_piecewise_pdf().getBreaks(), **kwargs)

def iid_median(X, n):
    return iid_order_stat(X, n, n // 2)

# averages need special treatment
def _int_exp2(x, n, op = operator.mul):
    """Right to left exponentiation by squaring.

    Extended operator arguments."""
    res = None
    for i, b in enumerate(bin(n)[2:]):
        if res is not None:
            res = op(i, res, i, res)
        if b == "1":
            if res is not None:
                res = op(i, res, 1, x)
            else:
                res = x
    return res
def _int_exp_all2(x, n, op = operator.mul):
    """Exponentiation by squaring returning all powers.

    Extended operator arguments."""
    res = [None] * (n+1)
    res[1] = x
    for i in xrange(2, n+1):
        i1 = i // 2
        i2 = i - i // 2
        res[i] = op(i1, res[i1], i2, res[i2])
    return res[1:]
def iid_op2(X, n, op, all = False):
    old_warn = params.general.warn_on_dependent
    params.general.warn_on_dependent = False
    if all:
        y = _int_exp_all2(X, n, op)
    else:
        y = _int_exp2(X, n, op)
    params.general.warn_on_dependent = old_warn
    return y
def _lambda_average(n1, x1, n2, x2):
    n = float(n1 + n2)
    return (n1 * x1 + n2 * x2) / n
def iid_average(X, n, all = False):
    return iid_op2(X, n, op = _lambda_average, all = all)

def _lambda_average_geom(n1, x1, n2, x2):
    n = float(n1 + n2)
    return ((x1**n1) * (x2**n2))**(1.0/n)
def iid_average_geom(X, n, all = False):
    #return iid_op2(X, n, op = _lambda_average_geom, all = all)
    return iid_prod(X, n)**(1.0/n)



if __name__ == "__main__":
    from pacal import *
    from pylab import *
#    X = UniformDistr(0.5, 1.5)
#    Y = iid_average_geom(X, 10)
#    Y.summary()
#    Y.plot()
#    show()
#    0/0
#    figure()
    T = UniformDistr()+UniformDistr()
    T.plot(linewidth=2.0)
    n = 11
    for k in xrange(0, n):
        print k
        fun = iid_order_stat(T, n, k+1)
        fun.plot(xmin=0,xmax=2)
        fun.summary()
    axis((0,2,0,3))
    figure()
    med = iid_median(BetaDistr(3, 2), 51)
    med.summary()
    med.plot()
    show()

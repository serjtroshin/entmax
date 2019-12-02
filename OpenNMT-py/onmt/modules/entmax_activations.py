import torch
from torch.autograd import Function
import torch.nn as nn


def _bisection(z, alpha, dim=0, iters=100):
    pow_exp = 1.0 / (alpha - 1.0)

    def _p(z, tau):
        return torch.pow(
            torch.clamp(z - tau, min=0.0),
            exponent=pow_exp)

    d = float(z.size(dim))
    z = (alpha - 1.0) * z.clone()
    z_max_value, _ = torch.max(z, dim=dim, keepdim=True)
    tau_min = z_max_value - 1.0
    tau_max = z_max_value - d ** (1 - alpha)

    p = None
    Z = None
    for _ in range(iters):
        tau = (tau_min + tau_max) / 2.0
        p = _p(z, tau)
        Z = p.sum(dim)
        mask = Z < 1.0
        tau_max[mask] = tau[mask]
        tau_min[~mask] = tau[~mask]

    return p / Z.unsqueeze(1)


class EntmaxBisectionFunction(Function):

    @staticmethod
    def forward(ctx, input, dim=1, alpha=1.5, iters=100):
        p_star = _bisection(input, alpha=alpha, dim=dim, iters=iters)
        ctx.save_for_backward(p_star)
        ctx.dim = dim
        ctx.alpha = alpha
        return p_star

    @staticmethod
    def backward(ctx, grad_output):
        p_star, = ctx.saved_tensors
        s = torch.zeros_like(p_star)
        mask = p_star > 0.0
        s[mask] = p_star[mask].pow(2.0 - ctx.alpha)

        g_diag_s = grad_output * s
        s_l1 = s.sum(ctx.dim)
        g_ss_t_div_s_l1 = (g_diag_s.sum(ctx.dim) / s_l1).unsqueeze(ctx.dim) * s
        d = g_diag_s - g_ss_t_div_s_l1
        return d, None, None, None

entmax_bisect = EntmaxBisectionFunction.apply


if __name__ == "__main__":
    import numpy as np
    tensor = torch.tensor(
        np.array([[0.1, 0.1, 0.8],
                 [0.8, 0.1, 0.1],
                 [0.5, 0.4, 0.1],
                 [0.33, 0.34, 0.33],
                 [1.0, 0.0, 0.0]])
        )

    print(entmax_bisect(tensor, -1, 1.5, 100))

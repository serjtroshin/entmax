import torch
import torch.nn as nn
from onmt.modules.entmax_utils import bisection, entmax15
from torch.autograd import Function

class EntmaxBaseFunction(Function):

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


class EntmaxBisectionFunction(EntmaxBaseFunction):

    @staticmethod
    def forward(ctx, input, dim=-1, alpha=1.5, iters=100):
        p_star = bisection(input, alpha=alpha, dim=dim, iters=iters)
        ctx.save_for_backward(p_star)
        ctx.dim = dim
        ctx.alpha = alpha
        return p_star


class Entmax15Function(EntmaxBaseFunction):

    @staticmethod
    def forward(ctx, input, dim=-1):
        p_star = entmax15(input, dim)
        ctx.save_for_backward(p_star)
        ctx.dim = dim
        ctx.alpha = 1.5
        return p_star


class LogEntmax15(nn.Module):

    def __init__(self, dim=-1):
        self.dim = dim
        super(LogEntmax15, self).__init__()

    def forward(self, input):
        return torch.log(entmax_15_exact(input, self.dim))


class LogEntmaxBisect(nn.Module):

    def __init__(self, dim=-1, iters=100, alpha=1.5):
        self.dim = dim
        self.iters = iters
        self.alpha = alpha
        super(LogEntmaxBisect, self).__init__()

    def forward(self, input):
        return torch.log(entmax_bisect(input, self.dim, self.alpha, self.iters))


entmax_bisect = EntmaxBisectionFunction.apply
entmax_15_exact = Entmax15Function.apply
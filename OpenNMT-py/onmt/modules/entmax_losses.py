import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Function
from onmt.modules.entmax_utils import entmax15, bisection
from onmt.utils.misc import aeq


class EntmaxLossFunction(Function):

    @staticmethod
    def forward(ctx, input, target,
        dim=-1,
        alpha=1.5,
        entmax_type='entmax15',
        iters=100
    ):
        """
        input (FloatTensor): ``(n, num_classes)``.
        target (LongTensor): ``(n,)``, the indices of the target classes
        """

        if entmax_type == 'entmax_bisection':
            p_star = bisection(input, dim=dim, iters=iters, alpha=alpha)
        elif entmax_type == 'entmax15':
            p_star = entmax15(input, dim)
            assert alpha == 1.5
        target_onehot = F.one_hot(target, input.size(-1))
        loss = (
            torch.sum((p_star - target_onehot) * input, dim=dim)
            +
            torch.sum(p_star - p_star ** alpha, dim=dim) / (alpha * (alpha - 1.0))
        )
        ctx.save_for_backward(target_onehot, p_star)

        return loss

    @staticmethod
    def backward(ctx, grad_output):
        target, p_star = ctx.saved_tensors
        return p_star - target, None, None, None, None, None


entmax_loss = EntmaxLossFunction.apply


class EntmaxLoss(nn.Module):
    def __init__(self,
        ignore_index=-100,
        weight=None,
        entmax_type='entmax15',
        alpha=1.5,
        iters=100,
        reduction='elementwise_mean'
    ):
        assert reduction in ['elementwise_mean', 'sum', 'none']
        self.reduction = reduction
        self.weight = weight
        self.entmax_type = entmax_type
        self.alpha = alpha
        self.iters = iters
        self.ignore_index=ignore_index
        super(EntmaxLoss, self).__init__()

    def forward(self, input, target):
        loss = entmax_loss(input, target,
            -1,
            self.alpha,
            self.entmax_type,
            self.iters
        )

        if self.ignore_index >= 0:
            ignored_positions = target == self.ignore_index
            size = float((target.size(0) - ignored_positions.sum()).item())
            loss.masked_fill_(ignored_positions, 0.0)
        else:
            size = float(target.size(0))
        if self.reduction == 'sum':
            loss = loss.sum()
        elif self.reduction == 'elementwise_mean':
            loss = loss.sum() / size
        return loss
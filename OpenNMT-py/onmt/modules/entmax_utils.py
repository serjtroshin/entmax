import torch
import torch.nn.functional as F


def bisection(z, alpha=1.5, dim=-1, iters=100):
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


def entmax15(z, dim=-1):
    # z: [batch_size, d]
    z, indices = torch.sort(z, descending=True)
    _, rev_indices = torch.sort(indices, descending=False)
    z = z / 2.0
    bs = z.shape[0]
    d = z.shape[-1]
    z_cum = torch.cumsum(z, dim=dim)
    p_star = torch.ones_like(z) * (-1)
    # history = [] # for debug only

    for p in range(d):
        m_p = z_cum[:,p] / (p + 1)
        s_p = torch.cumsum((z - m_p.unsqueeze(1))**2, dim=dim)[:,p]
        t_p = m_p - (1.0/(p + 1.0) * (1.0 - s_p))**0.5
        if p == d - 1:
            p_star = torch.where(p_star == -1, (F.relu(z - t_p.unsqueeze(1)))**2, p_star)
        else:
            p_star = torch.where(((z[:,p+1] <= t_p) & (t_p <= z[:,p])).unsqueeze(1),
                             (F.relu(z - t_p.unsqueeze(1)))**2,
                              p_star)
            # history.append(((z[:,p+1] <= t_p) & (t_p <= z[:,p])).unsqueeze(1))

    return torch.gather(p_star, dim=1, index=rev_indices)


if __name__ == "__main__":
    import numpy as np
    tensor = torch.tensor(
        np.array([[0.1, 0.1, 0.8],
                 [0.8, 0.1, 0.1],
                 [0.5, 0.4, 0.1],
                 [0.33, 0.34, 0.33],
                 [1.0, 0.0, 0.0]])
        )
    print(bisection(tensor, 1.5, iters=10))
    print(entmax15(tensor, -1))
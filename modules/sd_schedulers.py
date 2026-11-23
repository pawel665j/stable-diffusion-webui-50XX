import dataclasses
import math
import torch
import k_diffusion
import numpy as np
from scipy import stats

from modules import shared


def to_d(x, sigma, denoised):
    """Converts a denoiser output to a Karras ODE derivative."""
    return (x - denoised) / sigma


k_diffusion.sampling.to_d = to_d


@dataclasses.dataclass
class Scheduler:
    name: str
    label: str
    function: any

    default_rho: float = -1
    need_inner_model: bool = False
    aliases: list = None


def uniform(n, sigma_min, sigma_max, inner_model, device):
    return inner_model.get_sigmas(n).to(device)


def sgm_uniform(n, sigma_min, sigma_max, inner_model, device):
    start = inner_model.sigma_to_t(torch.tensor(sigma_max))
    end = inner_model.sigma_to_t(torch.tensor(sigma_min))
    sigs = [
        inner_model.t_to_sigma(ts)
        for ts in torch.linspace(start, end, n + 1)[:-1]
    ]
    sigs += [0.0]
    return torch.FloatTensor(sigs).to(device)


def get_align_your_steps_sigmas(n, sigma_min, sigma_max, device):
    # https://research.nvidia.com/labs/toronto-ai/AlignYourSteps/howto.html
    def loglinear_interp(t_steps, num_steps):
        """
        Performs log-linear interpolation of a given array of decreasing numbers.
        """
        xs = np.linspace(0, 1, len(t_steps))
        ys = np.log(t_steps[::-1])

        new_xs = np.linspace(0, 1, num_steps)
        new_ys = np.interp(new_xs, xs, ys)

        interped_ys = np.exp(new_ys)[::-1].copy()
        return interped_ys

    if shared.sd_model.is_sdxl:
        sigmas = [14.615, 6.315, 3.771, 2.181, 1.342, 0.862, 0.555, 0.380, 0.234, 0.113, 0.029]
    else:
        # Default to SD 1.5 sigmas.
        sigmas = [14.615, 6.475, 3.861, 2.697, 1.886, 1.396, 0.963, 0.652, 0.399, 0.152, 0.029]

    if n != len(sigmas):
        sigmas = np.append(loglinear_interp(sigmas, n), [0.0])
    else:
        sigmas.append(0.0)

    return torch.FloatTensor(sigmas).to(device)


def kl_optimal(n, sigma_min, sigma_max, device):
    alpha_min = torch.arctan(torch.tensor(sigma_min, device=device))
    alpha_max = torch.arctan(torch.tensor(sigma_max, device=device))
    step_indices = torch.arange(n + 1, device=device)
    sigmas = torch.tan(step_indices / n * alpha_min + (1.0 - step_indices / n) * alpha_max)
    return sigmas


def simple_scheduler(n, sigma_min, sigma_max, inner_model, device):
    sigs = []
    ss = len(inner_model.sigmas) / n
    for x in range(n):
        sigs += [float(inner_model.sigmas[-(1 + int(x * ss))])]
    sigs += [0.0]
    return torch.FloatTensor(sigs).to(device)


def normal_scheduler(n, sigma_min, sigma_max, inner_model, device, sgm=False, floor=False):
    start = inner_model.sigma_to_t(torch.tensor(sigma_max))
    end = inner_model.sigma_to_t(torch.tensor(sigma_min))

    if sgm:
        timesteps = torch.linspace(start, end, n + 1)[:-1]
    else:
        timesteps = torch.linspace(start, end, n)

    sigs = []
    for x in range(len(timesteps)):
        ts = timesteps[x]
        sigs.append(inner_model.t_to_sigma(ts))
    sigs += [0.0]
    return torch.FloatTensor(sigs).to(device)


def ddim_scheduler(n, sigma_min, sigma_max, inner_model, device):
    sigs = []
    ss = max(len(inner_model.sigmas) // n, 1)
    x = 1
    while x < len(inner_model.sigmas):
        sigs += [float(inner_model.sigmas[x])]
        x += ss
    sigs = sigs[::-1]
    sigs += [0.0]
    return torch.FloatTensor(sigs).to(device)


def beta_scheduler(n, sigma_min, sigma_max, inner_model, device):
    # From "Beta Sampling is All You Need" [arXiv:2407.12173] (Lee et. al, 2024) """
    alpha = shared.opts.beta_dist_alpha
    beta = shared.opts.beta_dist_beta
    timesteps = 1 - np.linspace(0, 1, n)
    timesteps = [stats.beta.ppf(x, alpha, beta) for x in timesteps]
    sigmas = [sigma_min + (x * (sigma_max-sigma_min)) for x in timesteps]
    sigmas += [0.0]
    return torch.FloatTensor(sigmas).to(device)


def turbo_scheduler(n, sigma_min, sigma_max, inner_model, device):
    unet = inner_model.inner_model.forge_objects.unet
    timesteps = torch.flip(torch.arange(1, n + 1) * float(1000.0 / n) - 1, (0,)).round().long().clip(0, 999)
    sigmas = unet.model.predictor.sigma(timesteps)
    sigmas = torch.cat([sigmas, sigmas.new_zeros([1])])
    return sigmas.to(device)

def get_align_your_steps_sigmas_GITS(n, sigma_min, sigma_max, device):
    def loglinear_interp(t_steps, num_steps):
        """
        Performs log-linear interpolation of a given array of decreasing numbers.
        """
        xs = np.linspace(0, 1, len(t_steps))
        ys = np.log(t_steps[::-1])

        new_xs = np.linspace(0, 1, num_steps)
        new_ys = np.interp(new_xs, xs, ys)

        interped_ys = np.exp(new_ys)[::-1].copy()
        return interped_ys

    if shared.sd_model.is_sdxl:
        sigmas = [14.615, 4.734, 2.567, 1.529, 0.987, 0.652, 0.418, 0.268, 0.179, 0.127, 0.029]
    else:
        sigmas = [14.615, 4.617, 2.507, 1.236, 0.702, 0.402, 0.240, 0.156, 0.104, 0.094, 0.029]

    if n != len(sigmas):
        sigmas = np.append(loglinear_interp(sigmas, n), [0.0])
    else:
        sigmas.append(0.0)

    return torch.FloatTensor(sigmas).to(device)

def ays_11_sigmas(n, sigma_min, sigma_max, device='cpu'):
    def loglinear_interp(t_steps, num_steps):
        """
        Performs log-linear interpolation of a given array of decreasing numbers.
        """
        xs = np.linspace(0, 1, len(t_steps))
        ys = np.log(t_steps[::-1])

        new_xs = np.linspace(0, 1, num_steps)
        new_ys = np.interp(new_xs, xs, ys)

        interped_ys = np.exp(new_ys)[::-1].copy()
        return interped_ys

    if shared.sd_model.is_sdxl:
        sigmas = [14.615, 6.315, 3.771, 2.181, 1.342, 0.862, 0.555, 0.380, 0.234, 0.113, 0.029]
    else:
        sigmas = [14.615, 6.475, 3.861, 2.697, 1.886, 1.396, 0.963, 0.652, 0.399, 0.152, 0.029]

    if n != len(sigmas):
        sigmas = np.append(loglinear_interp(sigmas, n), [0.0])
    else:
        sigmas.append(0.0)

    return torch.FloatTensor(sigmas).to(device)

def ays_32_sigmas(n, sigma_min, sigma_max, device='cpu'):
    def loglinear_interp(t_steps, num_steps):
        """
        Performs log-linear interpolation of a given array of decreasing numbers.
        """
        xs = np.linspace(0, 1, len(t_steps))
        ys = np.log(t_steps[::-1])
        new_xs = np.linspace(0, 1, num_steps)
        new_ys = np.interp(new_xs, xs, ys)
        interped_ys = np.exp(new_ys)[::-1].copy()
        return interped_ys
    if shared.sd_model.is_sdxl:
        sigmas = [14.61500000000000000, 11.14916180000000000, 8.505221270000000000, 6.488271510000000000, 5.437074020000000000, 4.603986190000000000, 3.898547040000000000, 3.274074570000000000, 2.743965270000000000, 2.299686590000000000, 1.954485140000000000, 1.671087150000000000, 1.428781520000000000, 1.231810090000000000, 1.067896490000000000, 0.925794430000000000, 0.802908860000000000, 0.696601210000000000, 0.604369030000000000, 0.528525520000000000, 0.467733440000000000, 0.413933790000000000, 0.362581860000000000, 0.310085170000000000, 0.265189250000000000, 0.223264610000000000, 0.176538770000000000, 0.139591920000000000, 0.105873810000000000, 0.055193690000000000, 0.028773340000000000, 0.015000000000000000]
    else:
        sigmas = [14.61500000000000000, 11.23951352000000000, 8.643630810000000000, 6.647294240000000000, 5.572508620000000000, 4.716485460000000000, 3.991960650000000000, 3.519560900000000000, 3.134904660000000000, 2.792287880000000000, 2.487736280000000000, 2.216638650000000000, 1.975083510000000000, 1.779317200000000000, 1.614753350000000000, 1.465409530000000000, 1.314849000000000000, 1.166424970000000000, 1.034755470000000000, 0.915737440000000000, 0.807481690000000000, 0.712023610000000000, 0.621739000000000000, 0.530652020000000000, 0.452909600000000000, 0.374914550000000000, 0.274618190000000000, 0.201152900000000000, 0.141058730000000000, 0.066828810000000000, 0.031661210000000000, 0.015000000000000000]
    if n != len(sigmas):
        sigmas = np.append(loglinear_interp(sigmas, n), [0.0])
    else:
        sigmas.append(0.0)
    return torch.FloatTensor(sigmas).to(device)




# ============================================================
# FLUX / Flow-Matching Schedulers
# ============================================================
# FLUX uses Flow-Matching where sigmas represent pseudo-timesteps
# from 1 (noisy) to 0 (clean). These schedulers are designed for
# that formulation.
# ============================================================


def flow_linear(n, sigma_min, sigma_max, device='cpu'):
    """Linear schedule for Flow-Matching.
    
    Uniform spacing in pseudo-time t = sigma.
    This is the default schedule used by FLUX.
    """
    sigmas = torch.linspace(1.0, 0.0, n + 1, device=device)
    return sigmas


def flow_cosine(n, sigma_min, sigma_max, device='cpu'):
    """Cosine schedule for Flow-Matching.
    
    Based on the cosine schedule from \"Simple Cosine Schedule\" [arXiv:2407.00057].
    Often produces better quality than linear for flow-matching.
    """
    s = 0.008
    t = torch.linspace(0, 1, n + 1, device=device)
    sigmas = torch.cos((t + s) / (1 + s) * math.pi / 2) / (1 + s)
    sigmas = sigmas / sigmas[0]
    sigmas = torch.clamp(sigmas, 0, 1)
    return sigmas


def flow_sqrt(n, sigma_min, sigma_max, device='cpu'):
    """Square root schedule for Flow-Matching.
    
    Spacing proportional to sqrt(t), concentrates steps near the beginning.
    """
    t = torch.linspace(0, 1, n + 1, device=device)
    sigmas = 1 - torch.sqrt(t)
    sigmas = torch.clamp(sigmas, 0, 1)
    return sigmas


def flow_linear_inv(n, sigma_min, sigma_max, device='cpu'):
    """Inverse linear schedule for Flow-Matching.
    
    Concentrates steps near the end (clean image).
    Useful when you want more refinement in later steps.
    """
    t = torch.linspace(0, 1, n + 1, device=device)
    sigmas = 1 - t ** 2
    sigmas = torch.clamp(sigmas, 0, 1)
    return sigmas


def flow_polyexponential(n, sigma_min, sigma_max, device='cpu', rho=3.0):
    """Polynomial in log sigma schedule for Flow-Matching.
    
    Similar to polyexponential but adapted for flow-matching range [0, 1].
    """
    ramp = torch.linspace(1, 0, n + 1, device=device)
    sigmas = ramp ** rho
    return sigmas


def flow_loglinear(n, sigma_min, sigma_max, device='cpu'):
    """Log-linear schedule for Flow-Matching.
    
    Linear interpolation in log space of a reference schedule.
    Based on the AlignYourSteps approach adapted for flow-matching.
    """
    ref_sigmas = torch.tensor([
        0.9999, 0.8621, 0.6554, 0.4734, 0.3157,
        0.2053, 0.1232, 0.0668, 0.0288, 0.0099, 0.0000
    ], device=device)
    
    if n != len(ref_sigmas):
        xs = np.linspace(0, 1, len(ref_sigmas))
        ys = np.log(ref_sigmas.cpu().numpy() + 1e-8)
        new_xs = np.linspace(0, 1, n + 1)
        new_ys = np.interp(new_xs, xs, ys)
        sigmas = torch.tensor(np.exp(new_ys), device=device)
    else:
        sigmas = ref_sigmas.clone()
    
    return sigmas


def flow_adaptive(n, sigma_min, sigma_max, inner_model, device):
    """Adaptive schedule based on latent image dimensions.
    
    Adjusts the number of effective steps based on the latent resolution.
    Higher resolutions get more steps for better quality.
    """
    unet = inner_model.inner_model.forge_objects.unet if hasattr(inner_model, 'inner_model') else None
    if unet is not None and hasattr(unet, 'model') and hasattr(unet.model, 'predictor'):
        predictor = unet.model.predictor
        if hasattr(predictor, 'mu'):
            mu = predictor.mu
            effective_n = max(n, int(n * mu))
            sigmas = torch.linspace(1.0, 0.0, effective_n + 1, device=device)
            if effective_n > n:
                indices = torch.linspace(0, effective_n, n + 1).long()
                sigmas = sigmas[indices]
            return sigmas
    return flow_linear(n, sigma_min, sigma_max, device)

schedulers = [
    Scheduler('automatic', 'Automatic', None),
    Scheduler('uniform', 'Uniform', uniform, need_inner_model=True),
    Scheduler('karras', 'Karras', k_diffusion.sampling.get_sigmas_karras, default_rho=7.0),
    Scheduler('exponential', 'Exponential', k_diffusion.sampling.get_sigmas_exponential),
    Scheduler('polyexponential', 'Polyexponential', k_diffusion.sampling.get_sigmas_polyexponential, default_rho=1.0),
    Scheduler('sgm_uniform', 'SGM Uniform', sgm_uniform, need_inner_model=True, aliases=["SGMUniform"]),
    Scheduler('kl_optimal', 'KL Optimal', kl_optimal),
    Scheduler('align_your_steps', 'Align Your Steps', get_align_your_steps_sigmas),
    Scheduler('simple', 'Simple', simple_scheduler, need_inner_model=True),
    Scheduler('normal', 'Normal', normal_scheduler, need_inner_model=True),
    Scheduler('ddim', 'DDIM', ddim_scheduler, need_inner_model=True),
    Scheduler('beta', 'Beta', beta_scheduler, need_inner_model=True),
    Scheduler('turbo', 'Turbo', turbo_scheduler, need_inner_model=True),
    Scheduler('align_your_steps_GITS', 'Align Your Steps GITS', get_align_your_steps_sigmas_GITS),
    Scheduler('align_your_steps_11', 'Align Your Steps 11', ays_11_sigmas),
    Scheduler('align_your_steps_32', 'Align Your Steps 32', ays_32_sigmas),
    # FLUX / Flow-Matching Schedulers
    Scheduler('flow_linear', 'Flow Linear', flow_linear),
    Scheduler('flow_cosine', 'Flow Cosine', flow_cosine),
    Scheduler('flow_sqrt', 'Flow Sqrt', flow_sqrt),
    Scheduler('flow_linear_inv', 'Flow Linear Inv', flow_linear_inv),
    Scheduler('flow_polyexponential', 'Flow Polyexp', flow_polyexponential),
    Scheduler('flow_loglinear', 'Flow LogLinear', flow_loglinear),
    Scheduler('flow_adaptive', 'Flow Adaptive', flow_adaptive, need_inner_model=True),
]

schedulers_map = {**{x.name: x for x in schedulers}, **{x.label: x for x in schedulers}}

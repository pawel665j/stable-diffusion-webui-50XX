# Stable Diffusion WebUI Forge

Stable Diffusion WebUI Forge is a platform on top of [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) (based on [Gradio](https://www.gradio.app/) <a href='https://github.com/gradio-app/gradio'><img src='https://img.shields.io/github/stars/gradio-app/gradio'></a>) to make development easier, optimize resource management, speed up inference, and study experimental features.

The name "Forge" is inspired from "Minecraft Forge". This project is aimed at becoming SD WebUI's Forge.

Forge is currently based on SD-WebUI 1.10.1 at [this commit](https://github.com/AUTOMATIC1111/stable-diffusion-webui/commit/82a973c04367123ae98bd9abdf80d9eda9b910e2). (Because original SD-WebUI is almost static now, Forge will sync with original WebUI every 90 days, or when important fixes.)

News are moved to this link: [Click here to see the News section](https://github.com/lllyasviel/stable-diffusion-webui-forge/blob/main/NEWS.md)

# Quick List

[Gradio 4 UI Must Read (TLDR: You need to use RIGHT MOUSE BUTTON to move canvas!)](https://github.com/lllyasviel/stable-diffusion-webui-forge/discussions/853)

[Flux Tutorial (BitsandBytes Models, NF4, "GPU Weight", "Offload Location", "Offload Method", etc)](https://github.com/lllyasviel/stable-diffusion-webui-forge/discussions/981)

[Flux Tutorial 2 (Seperated Full Models, GGUF, Technically Correct Comparison between GGUF and NF4, etc)](https://github.com/lllyasviel/stable-diffusion-webui-forge/discussions/1050)

[Forge Extension List and Extension Replacement List (Temporary)](https://github.com/lllyasviel/stable-diffusion-webui-forge/discussions/1754)

[How to make LoRAs more precise on low-bit models; How to Skip" Patching LoRAs"; How to only load LoRA one time rather than each generation; How to report LoRAs that do not work](https://github.com/lllyasviel/stable-diffusion-webui-forge/discussions/1038)

[Report Flux Performance Problems (TLDR: DO NOT set "GPU Weight" too high! Lower "GPU Weight" solves 99% problems!)](https://github.com/lllyasviel/stable-diffusion-webui-forge/discussions/1181)

[How to solve "Connection errored out" / "Press anykey to continue ..." / etc](https://github.com/lllyasviel/stable-diffusion-webui-forge/discussions/1474)

[(Save Flux BitsandBytes UNet/Checkpoint)](https://github.com/lllyasviel/stable-diffusion-webui-forge/discussions/1224#discussioncomment-10384104)

[LayerDiffuse Transparent Image Editing](https://github.com/lllyasviel/stable-diffusion-webui-forge/discussions/854)

[Tell us what is missing in ControlNet Integrated](https://github.com/lllyasviel/stable-diffusion-webui-forge/discussions/932)

[(Policy) Soft Advertisement Removal Policy](https://github.com/lllyasviel/stable-diffusion-webui-forge/discussions/1286)

(Flux BNB NF4 / GGUF Q8_0/Q5_0/Q5_1/Q4_0/Q4_1 are all natively supported with GPU weight slider and Quene/Async Swap toggle and swap location toggle. All Flux BNB NF4 / GGUF Q8_0/Q5_0/Q4_0 have LoRA support.)

# Installing Forge

**Just use this one-click installation package (with git and python included).**

> **⚡ RTX 50xx Series (Blackwell) — Recommended:** CUDA 13.2 + PyTorch 2.15 + SDPA attention

After you download, you uncompress, use `update.bat` to update, and use `run.bat` to run.

Note that running `update.bat` is important, otherwise you may be using a previous version with potential bugs unfixed.

### Requirements

- **NVIDIA GPU:** RTX 30xx / 40xx / 50xx series (sm_86 / sm_89 / sm_100 / sm_120)
- **CUDA Toolkit:** 13.2 (for RTX 50xx Blackwell)
- **Python:** 3.10–3.13
- **PyTorch:** 2.15+ (with CUDA 13.2 support)

### Advanced Install

If you are proficient in Git and you want to install Forge as another branch of SD-WebUI, please see [here](https://github.com/continue-revolution/sd-webui-animatediff/blob/forge/master/docs/how-to-use.md#you-have-a1111-and-you-know-git). In this way, you can reuse all SD checkpoints and all extensions you installed previously in your OG SD-WebUI, but you should know what you are doing.

If you know what you are doing, you can also install Forge using same method as SD-WebUI. (Install Git, Python, Git Clone the forge repo `https://github.com/lllyasviel/stable-diffusion-webui-forge.git` and then run webui-user.bat).

### Changelog

This fork includes significant updates over the original WebUI Forge:

- **CUDA 13.2** — full support for RTX 50xx (Blackwell, sm_120)
- **PyTorch 2.15** — latest with improved SDPA and memory management
- **SDPA attention** — replaced xformers for better compatibility with new architectures
- **Python 3.10–3.13** — broad version support
- **Auto dtype detection** — FP8/NF4 models loaded automatically by filename
- **Memory optimizations** — model stays in VRAM between generations

# Forge Status

Based on manual test one-by-one:

| Component                                           | Status                                      | Last Test    |
|-----------------------------------------------------|---------------------------------------------|--------------|
| Basic Diffusion                                     | Normal                                      | 2024 Aug 26  |
| GPU Memory Management System                        | Normal                                      | 2024 Aug 26  |
| LoRAs                                               | Normal                                      | 2024 Aug 26  |
| All Preprocessors                                   | Normal                                      | 2024 Aug 26  |
| All ControlNets                                     | Normal                                      | 2024 Aug 26  |
| All IP-Adapters                                     | Normal                                      | 2024 Aug 26  |
| All Instant-IDs                                     | Normal                                      | 2024 July 27 |
| All Reference-only Methods                          | Normal                                      | 2024 July 27 |
| All Integrated Extensions                           | Normal                                      | 2024 July 27 |
| Popular Extensions (Adetailer, etc)                 | Normal                                      | 2024 July 27 |
| Gradio 4 UIs                                        | Normal                                      | 2024 July 27 |
| Gradio 4 Forge Canvas                               | Normal                                      | 2024 Aug 26  |
| LoRA/Checkpoint Selection UI for Gradio 4           | Normal                                      | 2024 July 27 |
| Photopea/OpenposeEditor/etc for ControlNet          | Normal                                      | 2024 July 27 |
| Wacom 128 level touch pressure support for Canvas   | Normal                                      | 2024 July 15 |
| Microsoft Surface touch pressure support for Canvas | Broken, pending fix                         | 2024 July 29 |
| ControlNets (Union)                                 | Not implemented yet, pending implementation | 2024 Aug 26  |
| ControlNets (Flux)                                  | Not implemented yet, pending implementation | 2024 Aug 26  |
| API endpoints (txt2img, img2img, etc)               | Normal, but pending improved Flux support   | 2024 Aug 29  |
| OFT LoRAs                                           | Broken, pending fix                         | 2024 Sep 9   |

Feel free to open issue if anything is broken and I will take a look every several days. If I do not update this "Forge Status" then it means I cannot reproduce any problem. In that case, fresh re-install should help most.

# UnetPatcher

Below are self-supported **single file** of all codes to implement FreeU V2.

See also `extension-builtin/sd_forge_freeu/scripts/forge_freeu.py`:

```python
import torch
import gradio as gr

from modules import scripts


def Fourier_filter(x, threshold, scale):
    # FFT
    x_freq = torch.fft.fftn(x.float(), dim=(-2, -1))
    x_freq = torch.fft.fftshift(x_freq, dim=(-2, -1))

    B, C, H, W = x_freq.shape
    mask = torch.ones((B, C, H, W), device=x.device)

    crow, ccol = H // 2, W // 2
    mask[..., crow - threshold:crow + threshold, ccol - threshold:ccol + threshold] = scale
    x_freq = x_freq * mask

    # IFFT
    x_freq = torch.fft.ifftshift(x_freq, dim=(-2, -1))
    x_filtered = torch.fft.ifftn(x_freq, dim=(-2, -1)).real

    return x_filtered.to(x.dtype)


def patch_freeu_v2(unet_patcher, b1, b2, s1, s2):
    model_channels = unet_patcher.model.diffusion_model.config["model_channels"]
    scale_dict = {model_channels * 4: (b1, s1), model_channels * 2: (b2, s2)}
    on_cpu_devices = {}

    def output_block_patch(h, hsp, transformer_options):
        scale = scale_dict.get(h.shape[1], None)
        if scale is not None:
            hidden_mean = h.mean(1).unsqueeze(1)
            B = hidden_mean.shape[0]
            hidden_max, _ = torch.max(hidden_mean.view(B, -1), dim=-1, keepdim=True)
            hidden_min, _ = torch.min(hidden_mean.view(B, -1), dim=-1, keepdim=True)
            hidden_mean = (hidden_mean - hidden_min.unsqueeze(2).unsqueeze(3)) / (hidden_max - hidden_min).unsqueeze(2).unsqueeze(3)

            h[:, :h.shape[1] // 2] = h[:, :h.shape[1] // 2] * ((scale[0] - 1) * hidden_mean + 1)

            if hsp.device not in on_cpu_devices:
                try:
                    hsp = Fourier_filter(hsp, threshold=1, scale=scale[1])
                except:
                    print("Device", hsp.device, "does not support the torch.fft.")
                    on_cpu_devices[hsp.device] = True
                    hsp = Fourier_filter(hsp.cpu(), threshold=1, scale=scale[1]).to(hsp.device)
            else:
                hsp = Fourier_filter(hsp.cpu(), threshold=1, scale=scale[1]).to(hsp.device)

        return h, hsp

    m = unet_patcher.clone()
    m.set_model_output_block_patch(output_block_patch)
    return m


class FreeUForForge(scripts.Script):
    sorting_priority = 12  # It will be the 12th item on UI.

    def title(self):
        return "FreeU Integrated"

    def show(self, is_img2img):
        # make this extension visible in both txt2img and img2img tab.
        return scripts.AlwaysVisible

    def ui(self, *args, **kwargs):
        with gr.Accordion(open=False, label=self.title()):
            freeu_enabled = gr.Checkbox(label='Enabled', value=False)
            freeu_b1 = gr.Slider(label='B1', minimum=0, maximum=2, step=0.01, value=1.01)
            freeu_b2 = gr.Slider(label='B2', minimum=0, maximum=2, step=0.01, value=1.02)
            freeu_s1 = gr.Slider(label='S1', minimum=0, maximum=4, step=0.01, value=0.99)
            freeu_s2 = gr.Slider(label='S2', minimum=0, maximum=4, step=0.01, value=0.95)

        return freeu_enabled, freeu_b1, freeu_b2, freeu_s1, freeu_s2

    def process_before_every_sampling(self, p, *script_args, **kwargs):
        # This will be called before every sampling.
        # If you use highres fix, this will be called twice.

        freeu_enabled, freeu_b1, freeu_b2, freeu_s1, freeu_s2 = script_args

        if not freeu_enabled:
            return

        unet = p.sd_model.forge_objects.unet

        unet = patch_freeu_v2(unet, freeu_b1, freeu_b2, freeu_s1, freeu_s2)

        p.sd_model.forge_objects.unet = unet

        # Below codes will add some logs to the texts below the image outputs on UI.
        # The extra_generation_params does not influence results.
        p.extra_generation_params.update(dict(
            freeu_enabled=freeu_enabled,
            freeu_b1=freeu_b1,
            freeu_b2=freeu_b2,
            freeu_s1=freeu_s1,
            freeu_s2=freeu_s2,
        ))

        return
```

See also [Forge's Unet Implementation](https://github.com/lllyasviel/stable-diffusion-webui-forge/blob/main/backend/nn/unet.py).

# Under Construction

WebUI Forge is now under some constructions, and docs / UI / functionality may change with updates.

# Custom Modifications (RTX 5060 Ti 16GB / Blackwell sm_120)

This is a modified version optimized for NVIDIA RTX 50xx series (Blackwell architecture, sm_120) with CUDA 13.2 and PyTorch 2.15.

## Key Changes

### Startup Optimizations
- **`--skip-install`** — extension installers run once, not every launch
- **`--skip-torch-cuda-test`** — skips redundant CUDA availability subprocess check
- **`--attention-sdpa`** — uses native PyTorch SDPA instead of xformers (better sm_120 compatibility)
- **`--model-dtype-map`** — automatic FP8/NF4 detection by model filename

### Python Version Support
- Python 3.10+ supported (was locked to 3.10 only)
- Python 3.11/3.12/3.13 supported with warning for 3.13+

### CUDA/PyTorch Auto-Detection
- `get_cuda_version_from_gpu()` — detects GPU architecture and selects appropriate CUDA version
- `get_torch_versions_from_requirements()` — reads torch/torchvision versions from `requirements_versions.txt`
- No more hardcoded `cu121` + `torch 2.3.1`

### xformers Removed
- Heavy xformers import removed from `memory_management.py` (~1-2s startup time saved)
- SDPA enabled by default for NVIDIA + PyTorch 2.x
- No more xformers conflicts with CUDA 13.2 / Windows

### Model Format Auto-Detection
- `backend/model_dtype_config.py` — automatic dtype detection by filename patterns
- Priority: file format (FP8/NF4) → filename suffix → model type defaults
- Default: FLUX → FP8, SDXL → FP8, SD1.5 → FP16
- Custom rules via `model_dtype_map.json`

### Memory Management
- `need_global_unload` disabled — model stays in VRAM between generations
- Only unloads when checkpoint or unet_storage_dtype actually changes
- Prevents expensive PCIe transfer on every generation

### Package Compatibility
- `pkg_resources` → `importlib.metadata` / `packaging.version` everywhere
- Compatible with setuptools 77+ (pkg_resources removed)
- Updated `bitsandbytes==0.50.2` for NF4 support
- Fixed `pytorch-lightning` package name (underscore → hyphen)

### Files Modified
- `webui-user.bat` — optimized launch flags
- `backend/args.py` — added `--attention-sdpa` flag
- `backend/memory_management.py` — removed xformers import, simplified attention logic
- `backend/args.py` — added `--model-dtype-map` flag
- `backend/model_dtype_config.py` — improved dtype detection, added fp4 support
- `backend/loader.py` — integrated model_dtype_config into UNet loading
- `modules/launch_utils.py` — CUDA version detection, Python version check relaxed, requirements parsing
- `modules/sd_models.py` — passes model path for dtype detection
- `modules/processing.py` — no changes (global unload disabled in main_entry.py)
- `modules_forge/main_entry.py` — disabled global unload, smart reload logic
- `modules/textual_inversion/autocrop.py` — pkg_resources → packaging.version
- `extensions-builtin/forge_legacy_preprocessors/install.py` — pkg_resources → importlib.metadata
- `extensions-builtin/sd_forge_controlnet/install.py` — pkg_resources → importlib.metadata
- `extensions-builtin/forge_legacy_preprocessors/annotator/oneformer/detectron2/model_zoo/model_zoo.py` — pkg_resources → importlib.resources
- `requirements_versions.txt` — synced with installed versions

### Performance Results (RTX 5060 Ti 16GB)
| Metric | Before | After |
|--------|--------|-------|
| FLUX Dev load | 38.8s | 1.3s |
| FLUX Dev T5 load | 14.95s | 3.55s |
| FLUX Dev UNet load | 98.55s | 5.29s |
| FLUX Dev 20 steps | 56s | 42s |
| SDXL 2x speedup | — | ~2.39 it/s |

### Known Limitations
- PCIe 4.0 x8 bottleneck on 5060 Ti — model reload takes ~5-12s via PCIe
- DDR4 2400 RAM — slow CPU↔GPU memory transfers
- FLUX limited by GDDR6 bandwidth (~288 GB/s, same as 4060)
- FP8 inference works but BF16 computation still used

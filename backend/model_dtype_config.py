import os
import json
import re
import torch

_model_dtype_config = None
_model_dtype_cache = {}


DEFAULT_DTYPE_MAP = {
    "flux": "fp8-e4m3fn",
    "flux1": "fp8-e4m3fn",
    "flux-schnell": "fp8-e4m3fn",
    "flux-dev": "fp8-e4m3fn",
    "sdxl": "fp8-e4m3fn",
    "sd3": "fp8-e4m3fn",
    "chroma": "fp8-e4m3fn",
    "sd15": "fp16",
}


def load_model_dtype_config(config_path=None):
    global _model_dtype_config
    
    if _model_dtype_config is not None:
        return _model_dtype_config
    
    _model_dtype_config = dict(DEFAULT_DTYPE_MAP)
    
    if config_path is None:
        config_path = getattr(backend.args.args, 'model_dtype_map', None)
    
    if config_path and os.path.isfile(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)
            if isinstance(custom_config, dict):
                _model_dtype_config.update(custom_config)
                print(f"Loaded model dtype config from {config_path}")
        except Exception as e:
            print(f"Warning: Failed to load model dtype config: {e}")
    
    return _model_dtype_config


def detect_model_type_from_filename(filename):
    basename = os.path.basename(filename).lower()
    
    if 'flux' in basename:
        return 'flux'
    
    if 'sdxl' in basename or 'sd-xl' in basename or 'sd_xl' in basename:
        return 'sdxl'
    
    if 'sd3' in basename or 'sd-3' in basename or 'sd_3' in basename:
        return 'sd3'
    
    if 'chroma' in basename:
        return 'chroma'
    
    if 'sd1' in basename or 'v1-5' in basename or 'v1-4' in basename or 'v2' in basename:
        return 'sd15'
    
    return 'unknown'


def detect_dtype_from_filename(filename):
    basename = os.path.basename(filename).lower()
    
    if 'nf4' in basename:
        return 'nf4'
    
    if 'fp4' in basename:
        return 'fp4'
    
    if 'fp8' in basename:
        if 'e5m2' in basename:
            return 'fp8-e5m2'
        return 'fp8-e4m3fn'
    
    if 'fp32' in basename or 'bf16' in basename or 'bfloat16' in basename:
        return 'bf16'
    
    if 'fp16' in basename or 'float16' in basename:
        return 'fp16'
    
    return None


def get_dtype_for_model(filename):
    if filename in _model_dtype_cache:
        return _model_dtype_cache[filename]
    
    dtype = detect_dtype_from_filename(filename)
    
    if dtype is None:
        model_type = detect_model_type_from_filename(filename)
        config = load_model_dtype_config()
        dtype = config.get(model_type, 'fp16')
    
    dtype_map = {
        'fp32': torch.float32,
        'fp16': torch.float16,
        'bf16': torch.bfloat16,
        'fp8-e4m3fn': torch.float8_e4m3fn,
        'fp8-e5m2': torch.float8_e5m2,
        'nf4': 'nf4',
        'fp4': 'fp4',
    }
    
    result = dtype_map.get(dtype, torch.float16)
    _model_dtype_cache[filename] = result
    
    return result


def clear_dtype_cache():
    global _model_dtype_cache
    _model_dtype_cache = {}

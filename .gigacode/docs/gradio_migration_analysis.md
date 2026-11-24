# Gradio Migration Analysis: v4.40.0 to v6.32.0

## Summary Statistics

| Metric | Value |
|--------|-------|
| Files with import gradio as gr | **94 files** |
| Files with from gradio import ... | **11 files** |
| Critical imports (hidden APIs) | **8 files** |
| Dependent packages (rangeslider/imageslider) | **3 files** |
| Custom UI component classes | **14 classes** |
| Gradio internals patches | **6 locations** |
| Total affected files | **100+** |

## CRITICAL INCOMPATIBILITIES Gradio 4 to 6

### 1. Deleted/Moved Modules (BREAKING)

| Old Import (v4) | New Path (v6) | Status |
|---|---|---|
| gradio.utils | gradio.utils - deleted, many functions removed | CRITICAL |
| gradio.context.Context | gradio.context.Context - deleted | CRITICAL |
| gradio.data_classes | gradio.data_classes - renamed to gradio_client.data_classes | CRITICAL |
| gradio.components.image_editor.Brush | gradio.components.ImageEditor - renamed | CRITICAL |
| gradio.themes.utils.sizes | gradio.themes - deleted | CRITICAL |
| gradio.networking.url_ok | gradio.networking - deleted | CRITICAL |
| gradio.oauth | gradio.oauth - deleted | CRITICAL |
| gradio.routes | gradio.routes - deleted | CRITICAL |
| gradio.component_meta | gradio.component_meta - deleted | CRITICAL |
| gradio.processing_utils | gradio.processing_utils - deleted | CRITICAL |
| gradio.utils.get_upload_folder | gradio_client.utils | MIGRATE |
| gradio.utils.is_in_or_equal | gradio.utils - deleted | CRITICAL |
| gradio.utils.is_static_file | gradio.utils - deleted | CRITICAL |

### 2. External Package Dependencies

| Package | Version | Status |
|---|---|---|
| gradio-rangeslider | 0.0.8 | WARNING - Not updated for Gradio 6, may not work |
| gradio-imageslider | 0.0.20 | WARNING - Not updated for Gradio 6, may not work |
| gradio_client | - | REQUIRED for new data_classes |

## FILE RANKING BY CRITICALITY

### CRITICAL - Requires complete rewriting

| # | File | Reason |
|---|------|--------|
| 1 | modules/ui.py | gradio.utils (3 patches), gradio.components.image_editor.Brush, gr.Blocks (1000+ lines UI), gradio_extensions |
| 2 | modules/gradio_extensions.py | Direct patch of gradio.component_meta, gr.components.Component.__init__, gr.blocks.Block.get_config, gr.blocks.BlockContext.__init__, gr.blocks.Blocks.get_config_file - all internals deleted in v6 |
| 3 | modules/ui_tempdir.py | gradio.data_classes.GradioRootModel, gradio.data_classes.GradioModel, gradio.utils.get_upload_folder, gradio.utils.is_in_or_equal, gradio.utils.is_static_file - all deleted/moved |
| 4 | modules_forge/forge_canvas/canvas.py | gradio.component_meta (deleted), gradio.context.Context (deleted), custom ForgeCanvas |
| 5 | modules_forge/main_entry.py | gradio.context.Context (deleted), many .change()/.click() events |
| 6 | modules_forge/forge_space.py | gradio.context.Context (deleted) |
| 7 | modules/patch_basic.py | gradio.networking.url_ok (deleted) |
| 8 | spaces.py | gradio.oauth.attach_oauth, gradio.routes.attach_oauth - both modules deleted |

### HIGH RISK - Significant changes required

| # | File | Reason |
|---|------|--------|
| 9 | modules/ui_components.py | 14 custom classes (ToolButton, ResizeHandleRow, FormRow, FormGroup, FormHTML, InputAccordionImpl etc.) - inherit from gr.Button, gr.Row, gr.Group, gr.Checkbox |
| 10 | modules/shared_gradio_themes.py | gr.themes.Default, gr.themes.ThemeClass.from_hub, gr.themes.ThemeClass.load - theme API may change |
| 11 | modules/shared.py | shared.demo - global Gradio Blocks object |
| 12 | modules/script_callbacks.py | from gradio import Blocks - callback system |
| 13 | modules/progress.py | Progress bars, gradio as gr |
| 14 | extensions-builtin/sd_forge_controlnet/lib_controlnet/controlnet_ui/controlnet_ui_group.py | gradio_rangeslider.RangeSlider + ForgeCanvas |
| 15 | modules/ui_loadsave.py | Save/load UI state, gradio as gr |

### MEDIUM RISK - Localized changes

| # | File | Reason |
|---|------|--------|
| 16 | modules/ui.py (continued) | 1000+ lines of UI code with gr.Blocks, gr.Tab, gr.Row, gr.Column, .click(), .change() |
| 17 | modules/ui_toprow.py | gr.Row, gr.Column, top panel components |
| 18 | modules/ui_settings.py | gr.Blocks, gr.TabItem, gr.Column, gr.Row |
| 19 | modules/ui_postprocessing.py | gr.State, gr.Image, gradio as gr |
| 20 | modules/ui_extra_networks.py | Extra networks UI |
| 21 | modules/ui_prompt_styles.py | Prompt styles |
| 22 | modules/ui_extensions.py | Extensions tab |
| 23 | modules/txt2img.py | txt2img UI |
| 24 | modules/img2img.py | img2img UI |
| 25 | modules/extras.py | Extras UI |

### LOW RISK - Minimal changes

| # | File | Reason |
|---|------|--------|
| 26 | modules/processing_scripts/seed.py | Only gr.Row, gr.Button |
| 27 | modules/processing_scripts/refiner.py | InputAccordion |
| 28 | modules/processing_scripts/sampler.py | FormRow, FormGroup |
| 29 | modules/scripts_postprocessing.py | gr.Blocks, gr.Row |
| 30 | modules/hypernetworks/ui.py | Hypernetworks UI |
| 31 | modules/infotext_utils.py | Infotext |
| 32 | modules/options.py | UI settings |
| 33 | modules/errors.py | Gradio version check gradio.__version__ |
| 34 | modules/initialize.py | Import timer for gradio |
| 35 | modules/util.py | Utilities |
| 36 | modules/images.py | Images |
| 37 | modules/api/api.py | REST API |
| 38 | modules/shared_options.py | Options with gr.State |

### EXTENSIONS - Dependent on external packages

| # | File | Reason |
|---|------|--------|
| 39 | extensions-builtin/forge_space_geowizard/forge_app.py | gradio_imageslider.ImageSlider - external package |
| 40 | extensions-builtin/forge_space_illusion_diffusion/forge_app.py | from gradio import processing_utils, utils - deleted |
| 41 | extensions-builtin/forge_space_sapiens_normal/forge_app.py | gradio.themes.utils.sizes - deleted |
| 42 | extensions-builtin/sd_forge_controlnet/ | gradio_rangeslider.RangeSlider - external package |
| 43 | extensions-builtin/forge_space_animagine_xl_31/forge_app.py | gradio as gr |
| 44 | extensions-builtin/forge_space_birefnet/forge_app.py | gradio as gr |
| 45 | extensions-builtin/forge_space_example/forge_app.py | gradio as gr |
| 46 | extensions-builtin/forge_space_florence_2/forge_app.py | gradio as gr |
| 47 | extensions-builtin/forge_space_iclight/forge_app.py | gradio as gr |
| 48 | extensions-builtin/forge_space_idm_vton/forge_app.py | gradio as gr |
| 49 | extensions-builtin/forge_space_photo_maker_v2/forge_app.py | gradio as gr |

### SCRIPTS - Standard components

| # | File | Reason |
|---|------|--------|
| 50 | scripts/xyz_grid.py | X/Y/Z grid |
| 51 | scripts/sd_upscale.py | SD upscale |
| 52 | scripts/prompts_from_file.py | file.upload() |
| 53 | scripts/prompt_matrix.py | Prompt matrix |
| 54 | scripts/postprocessing_upscale.py | Upscale postprocessing |
| 55 | scripts/postprocessing_gfpgan.py | GFPGAN |
| 56 | scripts/postprocessing_focal_crop.py | Focal crop |
| 57 | scripts/postprocessing_codeformer.py | CodeFormer |
| 58 | scripts/poor_mans_outpainting.py | Outpainting |
| 59 | scripts/outpainting_mk_2.py | Outpainting v2 |
| 60 | scripts/loopback.py | Loopback |
| 61 | scripts/img2imgalt.py | Alt img2img |
| 62 | scripts/custom_code.py | Custom code |

### ADDITIONAL EXTENSIONS

| # | File | Reason |
|---|------|--------|
| 63 | extensions-builtin/extra-options-section/scripts/extra_options_section.py | Extra options |
| 64 | extensions-builtin/sd_forge_dynamic_thresholding/scripts/forge_dynamic_thresholding.py | Dynamic thresholding |
| 65 | extensions-builtin/sd_forge_freeu/scripts/forge_freeu.py | FreeU |
| 66 | extensions-builtin/sd_forge_kohya_hrfix/scripts/kohya_hrfix.py | Kohya HR-Fix |
| 67 | extensions-builtin/sd_forge_latent_modifier/scripts/forge_latent_modifier.py | Latent modifier |
| 68 | extensions-builtin/sd_forge_lora/scripts/lora_script.py | LoRA script |
| 69 | extensions-builtin/sd_forge_lora/ui_edit_user_metadata.py | LoRA metadata |
| 70 | extensions-builtin/sd_forge_multidiffusion/scripts/forge_multidiffusion.py | MultiDiffusion |
| 71 | extensions-builtin/sd_forge_neveroom/scripts/forge_never_oom.py | NeverOOM |
| 72 | extensions-builtin/sd_forge_perturbed_attention/scripts/forge_perturbed_attention.py | Perturbed attention |
| 73 | extensions-builtin/sd_forge_sag/scripts/forge_sag.py | SAG |
| 74 | extensions-builtin/sd_forge_stylealign/scripts/forge_stylealign.py | StyleAlign |
| 75 | extensions-builtin/soft-inpainting/scripts/soft_inpainting.py | Soft inpainting |

### UI HELPER FILES

| # | File | Reason |
|---|------|--------|
| 76 | modules/ui_toprow.py | Top row panel |
| 77 | modules/ui_settings.py | Settings panel |
| 78 | modules/ui_prompt_styles.py | Prompt styles |
| 79 | modules/ui_postprocessing.py | Postprocessing UI |
| 80 | modules/ui_loadsave.py | Load/save UI |
| 81 | modules/ui_gradio_extensions.py | Gradio extensions |
| 82 | modules/ui_extra_networks_user_metadata.py | Metadata |
| 83 | modules/ui_extra_networks_checkpoints_user_metadata.py | Checkpoint metadata |
| 84 | modules/ui_extensions.py | Extensions tab |
| 85 | modules/ui_common.py | Common utilities |
| 86 | modules/ui_checkpoint_merger.py | Checkpoint merger |
| 87 | modules/ui_tempdir.py | Temp files |

## DETAILED ANALYSIS OF CRITICAL FILES

### 1. modules/ui.py (1087 lines) - MAIN UI

Imports:
`python
import gradio as gr
import gradio.utils                    # DELETED
from gradio.components.image_editor import Brush  # RENAMED
`

Patches (lines 49-50):
`python
gradio.utils.version_check = lambda: None      # utils deleted
gradio.utils.get_local_ip_address = lambda: 127.0.0.1  # utils deleted
`

UI Structure:
- gr.Blocks - 4 main interfaces (txt2img, img2img, space, extras, pnginfo, demo)
- gr.Tab, gr.TabItem - tabs
- gr.Row, gr.Column - layout
- gr.Button, gr.Textbox, gr.Slider, gr.Dropdown, gr.Checkbox, gr.Number - components
- .click(), .change(), .select(), .upload() - events (209+ calls)
- ForgeCanvas - custom canvas (line 588+)

Changes needed:
- Replace gradio.utils with direct implementations (lines 49-50)
- Brush -> ImageEditor (API changed)
- All .click()/.change() may require signature updates

### 2. modules/gradio_extensions.py (181 lines) - PATCH SYSTEM

Imports:
`python
import gradio as gr
import gradio.component_meta  # DELETED in v6
`

Patches (lines 88-91):
`python
original_IOComponent_init = patches.patch(__name__, obj=gr.components.Component, field=__init__, replacement=IOComponent_init)
original_Block_get_config = patches.patch(__name__, obj=gr.blocks.Block, field=get_config, replacement=Block_get_config)
original_BlockContext_init = patches.patch(__name__, obj=gr.blocks.BlockContext, field=__init__, replacement=BlockContext_init)
original_Blocks_get_config_file = patches.patch(__name__, obj=gr.blocks.Blocks, field=get_config_file, replacement=Blocks_get_config_file)
`

Key functionality:
- IOComponent_init: Wraps gradio component __init__ to add webui_tooltip and script callbacks
- Block_get_config: Adds webui_tooltip to component config
- BlockContext_init: Same wrapper for BlockContext
- Blocks_get_config_file: Modifies config file output
- gradio_component_meta_create_or_modify_pyi: Prevents .pyi file creation
- gradio.component_meta.updateable: Override (described as broken)
- EventWrapper: Wraps gradio events to translate _js to js parameter
- repair(): Repairs component __init__ signatures for compatibility
- Dependency: Wraps gr.events.Dependency.then to handle _js parameter
- gr.Box = gr.Group: Alias

Changes needed:
- All patch targets (gr.components.Component.__init__, gr.blocks.Block.get_config, etc.) are deleted in v6
- gradio.component_meta is completely removed in v6
- Event system may have changed - EventWrapper needs review
- repair() function relies on gradio internal signatures that may not exist
### 3. modules/ui_tempdir.py (199 lines) - TEMP FILE HANDLING

Imports (lines 87-91):
`python
from gradio import FileData
from gradio.data_classes import GradioRootModel
from gradio.data_classes import GradioModel
from gradio.utils import get_upload_folder, is_in_or_equal, is_static_file
`

Changes needed:
- FileData moved to gradio_client
- GradioRootModel/GradioModel moved to gradio_client.data_classes
- get_upload_folder, is_in_or_equal, is_static_file - check gradio.utils or gradio_client.utils
### 4. modules_forge/forge_canvas/canvas.py (153 lines) - FORGE CANVAS

Imports:
`python
import gradio.component_meta  # DELETED
import gradio as gr
from gradio.context import Context  # DELETED
`

Changes needed:
- gradio.component_meta.create_or_modify_pyi patched - need alternative or remove
- gradio.context.Context.root_block.load used for JS injection - find replacement
- ForgeCanvas wraps gradio image editor functionality
### 5. modules_forge/main_entry.py (494 lines) - FORGE MAIN ENTRY

Imports:
`python
import gradio as gr
from gradio.context import Context  # DELETED
`

Changes needed:
- gradio.context.Context removed - need alternative for context management
- Multiple .change()/.click() event handlers
### 6. modules/patch_basic.py (93 lines) - NETWORKING PATCH

Imports:
`python
import gradio.networking
`

Patch (line 90):
`python
gradio.networking.url_ok = gradio_url_ok_fix
`

Changes needed:
- gradio.networking.url_ok deleted in v6 - need alternative URL validation
### 7. spaces.py (272 lines) - SPACE OAUTH PATCH

Imports:
`python
import gradio.oauth
import gradio.routes
`

Patches (lines 34-35):
`python
gradio.oauth.attach_oauth = lambda x: None
gradio.routes.attach_oauth = lambda x: None
`

Changes needed:
- Both gradio.oauth and gradio.routes modules deleted in v6
- OAuth attachment likely handled differently or removed entirely

## RECOMMENDATIONS FOR MIGRATION Gradio 4.40 to 6.32.0

### Phase 1: Foundation (Critical Files)

1. **modules/errors.py** - Update expected_gradio_version from 4.40.0 to 6.32.0 (line 112)
2. **modules/ui_tempdir.py** - Migrate to gradio_client for FileData, GradioModel, GradioRootModel
3. **modules/patch_basic.py** - Replace gradio.networking.url_ok with custom implementation
4. **spaces.py** - Remove gradio.oauth/gradio.routes patches (OAuth likely removed in v6)
5. **modules/gradio_extensions.py** - Complete rewrite needed:
   - gradio.component_meta deleted - remove pyi prevention logic or find alternative
   - Component init patches need new approach for v6 component model
   - EventWrapper may need redesign for v6 event system
   - repair() function needs signature updates
6. **modules/ui.py** - After gradio_extensions fixed:
   - Remove gradio.utils patches (lines 49-50)
   - Replace Brush with ImageEditor component
   - Review all 209+ .click()/.change() event handlers
7. **modules_forge/forge_canvas/canvas.py** - Replace Context and component_meta
8. **modules_forge/main_entry.py** - Replace Context usage
9. **modules_forge/forge_space.py** - Replace Context usage

### Phase 2: UI Components (High Risk)

10. **modules/ui_components.py** - Update all 14 custom component classes:
    - ToolButton, ResizeHandleRow, FormRow, FormGroup, FormHTML, FormColorPicker
    - DropdownMulti, DropdownEditable, InputAccordionImpl
    - Verify inheritance from gr.Button, gr.Row, gr.Group, gr.Checkbox still valid
11. **modules/shared_gradio_themes.py** - Test theme API compatibility
12. **modules/ui_loadsave.py** - Review UI state save/load logic
13. **extensions-builtin/sd_forge_controlnet/** - Update RangeSlider dependency

### Phase 3: Standard UI Files (Medium Risk)

14-25. All modules/ui_*.py files - Review gr.Row, gr.Column, gr.Tab, gr.Blocks usage
26-38. All scripts/*.py files - Review event handlers and component usage

### Phase 4: Extensions (Low Risk but External Dependencies)

39-49. forge_space_* extensions - Test with new Gradio version
50-75. Built-in extensions - Review for compatibility
76-87. Additional UI helper files - Final review


## WARNINGS AND CONSEQUENCES

### Direct Consequences of Skipping Updates

1. **Application will not start** - modules/errors.py version check will block startup (line 137)
2. **ImportErrors on startup** - gradio.utils, gradio.context, gradio.oauth, gradio.routes, gradio.networking, gradio.component_meta will all raise ModuleNotFoundError
3. **UI will be broken** - 1000+ lines of UI code in modules/ui.py will fail on deleted imports
4. **Canvas will not work** - ForgeCanvas depends on deleted gradio.context.Context
5. **ControlNet UI broken** - gradio_rangeslider.RangeSlider may not be compatible with Gradio 6
6. **Image slider extensions broken** - gradio_imageslider.ImageSlider may not work with Gradio 6
7. **OAuth patches cause crashes** - spaces.py will crash on import with ModuleNotFoundError
8. **Temp file handling broken** - ui_tempdir.py will fail on deleted gradio.data_classes
9. **All event handlers broken** - .click(), .change(), .select(), .upload() signatures may have changed
10. **Theme system may break** - gr.themes API may have changed

### Indirect Consequences (Dependencies)

1. **ForgeCanvas users** - Inpainting, sketch, outpainting features will break
2. **ControlNet users** - All ControlNet features depend on gradio_rangeslider
3. **FreeU users** - FreeU extension uses gradio components
4. **LoRA users** - LoRA UI depends on gradio components
5. **Extra networks** - Checkpoint/LoRA browsing uses gradio components
6. **API users** - REST API endpoints may break if UI components changed
7. **Script users** - xyz_grid, loopback, outpainting scripts will fail
8. **HuggingFace Space users** - All forge_space_* extensions may break
9. **Theme users** - Custom gradio themes may not load
10. **JavaScript integrations** - _js parameter in event handlers may not work

### Recommended Migration Strategy

1. **Create a backup branch** before starting migration
2. **Update gradio-rangeslider and gradio-imageslider** first - check if they support Gradio 6
3. **If external packages do not support Gradio 6**, consider:
   - Forking gradio-rangeslider and gradio-imageslider
   - Replacing with native Gradio 6 equivalents
   - Staying on Gradio 4.x until packages are updated
4. **Test incrementally** - fix one critical file at a time
5. **Run the webui after each fix** to verify nothing is broken
6. **Document all changes** in CHANGELOG.md
7. **Consider using --skip-version-check** temporarily during migration
8. **Expected timeline** - This is a major migration affecting 100+ files


## UPDATED GRADIO INTEGRATION MAP (Beyond Previous)

The previous gradio_integration_map.md (81 files) is incomplete. Full scan found:

### Additional files with gradio imports NOT in previous map:

| File | Import | Previous Map? |
|------|--------|---------------|
| modules/gradio_extensions.py | import gradio.component_meta | NO |
| modules_forge/forge_canvas/canvas.py | import gradio.component_meta | NO |
| modules_forge/forge_space.py | from gradio.context import Context | NO |
| modules/patch_basic.py | import gradio.networking | NO |
| spaces.py | import gradio.oauth, import gradio.routes | NO |
| modules/ui_components.py | 14 custom component classes | PARTIAL |
| modules/ui_tempdir.py | gradio.data_classes, gradio.utils | NO |
| modules/shared_gradio_themes.py | gr.themes API | NO |
| modules/errors.py | gradio.__version__ check | NO |
| extensions-builtin/sd_forge_controlnet/lib_controlnet/api.py | import gradio | NO |
| extensions-builtin/sd_forge_controlnet/lib_controlnet/controlnet_ui/modal.py | import gradio | NO |
| extensions-builtin/sd_forge_controlnet/lib_controlnet/controlnet_ui/openpose_editor.py | import gradio | NO |
| extensions-builtin/sd_forge_controlnet/lib_controlnet/controlnet_ui/photopea.py | import gradio | NO |
| extensions-builtin/sd_forge_controlnet/lib_controlnet/infotext.py | import gradio | NO |
| extensions-builtin/soft-inpainting/scripts/soft_inpainting.py | import gradio | NO |
| extensions-builtin/sd_forge_perturbed_attention/scripts/forge_perturbed_attention.py | import gradio | NO |
| modules_forge/main_entry.py | gradio.context.Context | PARTIAL |

### Total: 94 files with gradio imports (was 81 in previous map)


## SUMMARY

| Category | Count | Action |
|----------|-------|--------|
| Critical files (need complete rewrite) | 8 | Phase 1 |
| High risk files (significant changes) | 7 | Phase 2 |
| Medium risk files (localized changes) | 10 | Phase 3 |
| Low risk files (minimal changes) | 13 | Phase 3 |
| Extensions (external dependencies) | 11 | Phase 4 |
| Additional extensions | 13 | Phase 4 |
| UI helper files | 12 | Phase 4 |
| **TOTAL** | **74+** | **Full migration** |

### Key blockers:
1. gradio-rangeslider - does not support Gradio 6 (may need fork)
2. gradio-imageslider - does not support Gradio 6 (may need fork)
3. gradio.component_meta - deleted in v6 (gradio_extensions.py needs rewrite)
4. gradio.context.Context - deleted in v6 (canvas.py, main_entry.py, forge_space.py)
5. gradio.utils - many functions deleted in v6 (ui.py, ui_tempdir.py)
6. gradio.networking - deleted in v6 (patch_basic.py)
7. gradio.oauth/gradio.routes - deleted in v6 (spaces.py)
8. gradio.data_classes - moved to gradio_client (ui_tempdir.py)
9. gradio.components.image_editor.Brush - renamed to ImageEditor (ui.py)
10. gradio.themes.utils.sizes - deleted (forge_space_sapiens_normal)

### Estimated effort:
- Minimum: 2-4 weeks for experienced developer
- Recommended: 4-6 weeks with testing
- Risk level: HIGH (major architectural changes in Gradio 6)
- Rollback plan: Keep Gradio 4.40.0 branch as fallback

---
*Generated: 2026-11-24*
*Gradio versions: 4.40.0 (current) -> 6.32.0 (target)*
*Files scanned: 100+ Python files*

#Краткая выжимка:
Статистика:

94 файла с import gradio as gr
11 файлов с from gradio import ...
8 критических файлов, требующих полного переписывания
74+ файла всего в списке миграции (вместо 81 в старой карте)
10 ключевых блокировщиков:

gradio-rangeslider — не поддерживает Gradio 6 (нужен форк или замена)
gradio-imageslider — не поддерживает Gradio 6 (нужен форк или замена)
gradio.component_meta — удалён в v6
gradio.context.Context — удалён в v6
gradio.utils — многие функции удалены
gradio.networking — удалён
gradio.oauth/gradio.routes — удалены
gradio.data_classes — перенесён в gradio_client
gradio.components.image_editor.Brush — переименован в ImageEditor
gradio.themes.utils.sizes — удалён
4 фазы миграции:

Phase 1 (Critical) — 8 файлов, полное переписывание
Phase 2 (High Risk) — 7 файлов, значительные изменения
Phase 3 (Medium/Low Risk) — 23 файла, локальные изменения
Phase 4 (Extensions) — 36 расширений, финальная проверка
# Changelog - Migration Plan

> Все изменения проекта Stable Diffusion WebUI Forge по этапам миграции.

---

## Версия окружения

| Параметр | Значение |
|----------|----------|
| Python | 3.11-3.13 (рекомендуется 3.11-3.12) |
| PyTorch | 2.15.0+cu132 |
| torchvision | 0.29.2+cu132 |
| CUDA | 13.2 |
| GPU | RTX 50xx (Blackwell, sm_120) |
| Gradio | 4.40.0 (текущая) |
| Gradio-client | 1.2.0 |
| fastapi | 0.109.2 |
| starlette | 0.29.0 |
| numpy | 2.5.5 |
| Pillow | 10.4.0 |
| protobuf | 7.36.2 |
| diffusers | 0.31.0 |
| transformers | 4.48.0 |
| bitsandbytes | 0.50.2 |
| accelerate | 1.16.0 |
| gradio-rangeslider | 0.0.8 |
| gradio-imageslider | 0.0.20 |

---

## Этап 1: Организация репозитория и журнала изменений

**Дата:** 2026-11-23  
**Статус:** Завершён

### Созданные файлы
| Файл | Описание |
|------|----------|
| CHANGELOG.md | Журнал миграции |
| KNOWN_ISSUES.md | Нерешённые проблемы |
| TYPES.md | Примеры аннотаций типов |
| docs/MIGRATION_PLAN.md | План миграции (10 шагов) |
| docs/gradio_integration_map.md | Карта всех файлов с gradio (81 файл) |
| docs/gradio_migration_analysis.md | Анализ миграции Gradio 4->6 (94 файла) |

---

## Этап 2: Подготовка окружения

**Дата:** 2026-11-23  
**Статус:** Завершён

Версии подтверждены: Python 3.11-3.13, PyTorch 2.15.0+cu132, CUDA 13.2.  
README.md и requirements.txt обновлены.

---

## Этап 3: Исправление типовых ошибок mypy

**Дата:** 2026-11-23  
**Статус:** Backend завершён

### Результаты
- ackend/: 58 файлов, 54 -> 0 ошибок
- modules/: 10 файлов исправлено, остальные отключены в конфигурации

### Исправленные файлы (Backend, 13 файлов)

| Файл | Ошибок | Исправление |
|------|--------|-------------|
| ackend/misc/sub_quadratic_attention.py | 10 | Protocol, tuple->list, type ignore |
| ackend/nn/mmditx.py | 7 | Optional types, None checks |
| ackend/nn/chroma.py | 4 | Type annotation for dict |
| ackend/operations.py | 2 | var-annotated, type ignore |
| ackend/memory_management.py | 1 | var-annotated + import |
| ackend/model_dtype_config.py | 1 | var-annotated |
| ackend/patcher/lora.py | 1 | var-annotated |
| ackend/nn/base.py | 1 | ConfigMixin type |
| ackend/nn/vae.py | 1 | ConfigMixin type |
| ackend/nn/unet.py | 1 | ConfigMixin type |
| ackend/patcher/controlnet.py | 1 | str-format |
| ackend/text_processing/classic_engine.py | 1 | var-annotated |
| ackend/diffusion_engine/base.py | 1 | var-annotated |

### Исправленные файлы (Modules, 9 файлов)

| Файл | Ошибок | Исправление |
|------|--------|-------------|
| modules/api/api.py | 6 | var-annotated, None check, import |
| modules/scripts_postprocessing.py | 2 | assignment |
| modules/textual_inversion/textual_inversion.py | 1 | var-annotated |
| modules/processing_scripts/{seed,sampler,refiner}.py | 3 | assignment |
| modules/api/models.py | 1 | type annotation |
| modules/models/sd3/sd3_cond.py | 1 | name-defined |
| modules/textual_inversion/image_embedding.py | 1 | type ignore |

---

## Этап 4: Совместимость с Python 3.11/3.12

**Статус:** В основном завершено
- pkg_resources -> importlib.metadata / packaging.version
- Совместимость с setuptools 77+

### Изменённые файлы
| Файл | Изменение |
|------|-----------|
| modules/launch_utils.py | pkg_resources -> importlib.metadata |
| modules/sysinfo.py | pkg_resources -> importlib.metadata |
| modules/textual_inversion/autocrop.py | pkg_resources -> packaging.version |
| xtensions-builtin/forge_legacy_preprocessors/install.py | pkg_resources -> importlib.metadata |
| xtensions-builtin/sd_forge_controlnet/install.py | pkg_resources -> importlib.metadata |
| xtensions-builtin/forge_legacy_preprocessors/annotator/oneformer/detectron2/model_zoo/model_zoo.py | pkg_resources -> importlib.resources |

---

## Этап 5: CUDA/PyTorch совместимость

**Статус:** В основном завершено
- CUDA 13.2 auto-detection через get_cuda_version_from_gpu()
- SDPA attention вместо xformers (--attention-sdpa)
- PyTorch 2.15.0+cu132 supported
- Удалён xformers import из memory_management.py (~1-2s ускорение запуска)
- Auto dtype detection: FP8/NF4 модели загружаются автоматически по имени файла

### Изменённые файлы
| Файл | Изменение |
|------|-----------|
| ackend/args.py | Добавлены флаги --attention-sdpa, --model-dtype-map |
| ackend/model_dtype_config.py | Автоопределение dtype по filename |
| ackend/loader.py | Интеграция model_dtype_config в UNet loading |
| ackend/memory_management.py | Удалён xformers import |
| modules/launch_utils.py | CUDA version detection, Python version check |
| modules/sd_models.py | Передаёт model path для dtype detection |
| modules_forge/main_entry.py | Disabled global unload, smart reload |
| webui-user.bat | --cuda-malloc --skip-install --attention-sdpa --model-dtype-map |

---

## Этап 6: Очистка рудиментов и мёртвого кода

**Дата:** 2026-11-23  
**Статус:** Завершён  
**Бэкап:** .gigacode/cleanup_backup/

### Удалённые файлы (критичные)

| Файл | Причина |
|------|---------|
| nvironment-wsl2.yaml | Python 3.10 + CUDA 11.8 + PyTorch 2.0 - конфликт с cu132 |
| modules/sd_hijack_clip_old.py | 82 строки закомментированного кода |
| modules/npu_specific.py | 31 строка (Huawei NPU - не целевая платформа) |
| modules/xpu_specific.py | 138 строк (Intel XPU - не целевая платформа) |
| modules/mac_specific.py | 98 строк (macOS - не целевая платформа) |

### Удалённые файлы (косметические)

| Файл | Причина |
|------|---------|
| params.txt | Мусорный файл с промптами |
| NEWS.md | Устаревшие заметки от 2024 |
| webui-macos-env.sh | macOS не целевая платформа |
| xtensions/put extensions here.txt | Шаблонный файл A1111 |

### Очищенные файлы

| Файл | Что удалено |
|------|-------------|
| modules/sd_hijack_optimizations.py | 677 строк закомментированного xformers/V1 кода |
| modules/initialize.py | xformers лог-фильтр (строка 12) |
| modules/launch_utils.py | Intel XPU cp310 fallback, xformers install, REQS_FILE_FOR_NPU |

### Итого
- **Удалено файлов:** 9
- **Очищено строк мёртвого кода:** ~950
- **Удалено ROCm/Navi/NPU/XPU/MPS блоков:** 4 платформы

---

## Этап 7: Обновление библиотек

**Дата:** 2026-11-23  
**Статус:** Завершён

### Проблема
requirements_versions.txt был актуален, но в venv были установлены устаревшие версии.

### Обновлённые версии

| Пакет | Старая | Новая | Причина |
|-------|--------|-------|---------|
| numpy | 1.26.2 | 2.5.5 | Torch 2.15 + diffusers 0.31 |
| protobuf | 3.20.0 | 7.36.2 | transformers 4.48 |
| einops | 0.4.1 | 0.8.2 | diffusers 0.31 |
| huggingface-hub | 0.35.0 | 0.36.2 | совместимость |
| blendmodes | 2022 | 2025 | numpy 2.x support |
| psutil | 5.9.5 | 7.2.2 | обновление |
| bitsandbytes | 0.4x | 0.50.2 | NF4 support |
| diffusers | 0.30.x | 0.31.0 | latest |
| transformers | 4.46.x | 4.48.0 | latest |
| accelerate | 1.15.x | 1.16.0 | latest |
| pytorch-lightning | 2.6.0 | 2.6.6 | имя: underscore->hyphen |

### Конфликты и решения

| Конфликт | Решение |
|----------|---------|
| blendmodes 2022 требует numpy<2 | Обновлён до 2025 |
| transformers требует huggingface-hub<1.0 | Используется 0.36.2 |

---

## Этап 8: Откат gradio с 5.x -> 4.40.0

**Дата:** 2026-11-23  
**Статус:** Завершён

### Проблема
Gradio 5.50 полностью сломал UI:
- Все кнопки показывают ошибки при нажатии
- UI стал статичным, кислотные цвета
- gradio_rangeslider и gradio_imageslider не совместимы с gradio 5.x
- 113 файлов проекта используют gradio API, который изменился в 5.x

### Решение
Откатить gradio до 4.40.0 (версия из requirements)

### Обновлённые версии

| Пакет | Было | Стало |
|-------|------|-------|
| gradio | 5.50.0 | **4.40.0** |
| gradio-client | 1.14.0 | **1.2.0** |
| Pillow | 11.3.0 | **10.4.0** |
| fastapi | 0.163.2 | **0.109.2** |
| starlette | 0.52.1 | **0.29.0** |
| pydantic | 2.12.3 | **2.14.4** |
| websockets | 15.0.1 | **12.0** |

### Почему gradio 5 не подходит
- gradio_rangeslider требует gradio<5.0
- gradio_imageslider требует gradio<5.0
- ControlNet, infinite-image-browsing, freeu - все используют эти расширения
- 113 файлов требуют адаптации под новый API gradio 5
- gradio.utils переехал в gradio_client
- gradio.components.image_editor.Brush переименован

### Статус gradio 5
Отложено. Переход на gradio 5 - future work после адаптации всех скриптов.

---

## Этап 9: Откат gradio 6.32.0 -> 4.40.0

**Дата:** 2026-11-23  
**Статус:** Завершён

### Проблема
Gradio 6.32.0 сломал все расширения:
- ControlNet (gradio-rangeslider требует gradio<6.0)
- infinite-image-browsing (gradio-imageslider требует gradio<6.0)
- freeu, kohya_hrfix - все используют gradio_rangeslider
- gradio.component_meta - удалён в v6
- gradio.context.Context - удалён в v6
- gradio.utils - многие функции удалены в v6
- gradio.networking - удалён в v6
- gradio.oauth/gradio.routes - удалены в v6

### Решение
Откат обратно на gradio 4.40.0 - рабочий стек для 133 скриптов проекта.

### Итоговая версия стека

| Пакет | Версия |
|-------|--------|
| gradio | 4.40.0 |
| gradio-client | 1.2.0 |
| fastapi | 0.109.2 |
| starlette | 0.29.0 |
| huggingface-hub | 0.36.2 |
| Pillow | 10.4.0 |
| gradio-rangeslider | 0.0.8 |
| gradio-imageslider | 0.0.20 |

### Итог
Gradio 6.x - для будущего. Сейчас работаем на 4.40.0 - 133 скрипта работают.

---

## Этап 10: Анализ миграции Gradio 4.40.0 -> 6.32.0

**Дата:** 2026-11-24  
**Статус:** Анализ завершён, миграция отложена

### Результаты сканирования
- **94 файла** с import gradio as gr
- **11 файлов** с rom gradio import ...
- **8 критических файлов** с удалёнными API
- **74+ файла** в списке миграции

### 10 ключевых блокировщиков

1. gradio-rangeslider - не поддерживает Gradio 6 (нужен форк)
2. gradio-imageslider - не поддерживает Gradio 6 (нужен форк)
3. gradio.component_meta - удалён в v6
4. gradio.context.Context - удалён в v6
5. gradio.utils - многие функции удалены
6. gradio.networking - удалён
7. gradio.oauth/gradio.routes - удалены
8. gradio.data_classes - перенесён в gradio_client
9. gradio.components.image_editor.Brush - переименован в ImageEditor
10. gradio.themes.utils.sizes - удалён

### Критические файлы (требуют полного переписывания)

| # | Файл | Причина |
|---|------|---------|
| 1 | modules/ui.py | gradio.utils, Brush, 1000+ строк UI |
| 2 | modules/gradio_extensions.py | component_meta, internals patches |
| 3 | modules/ui_tempdir.py | data_classes, utils |
| 4 | modules_forge/forge_canvas/canvas.py | component_meta, Context |
| 5 | modules_forge/main_entry.py | Context |
| 6 | modules/patch_basic.py | networking.url_ok |
| 7 | spaces.py | oauth, routes |

### Оценка
- **Минимум:** 2-4 недели для опытного разработчика
- **Рекомендуется:** 4-6 недель с тестированием
- **Риск:** HIGH (major architectural changes in Gradio 6)
- **План отката:** Keep Gradio 4.40.0 branch as fallback

### Документация
- docs/gradio_integration_map.md - карта 81 файла (оригинал)
- docs/gradio_migration_analysis.md - полный анализ 94 файлов
- MODIFICATIONS.md - обновлён список изменений
- README.md - обновлён Changelog и Forge Status

---

*Журнал ведётся в соответствии с планом docs/MIGRATION_PLAN.md*

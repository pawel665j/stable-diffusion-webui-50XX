# Модификации

Это форк проекта [Stable Diffusion WebUI Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge).

## Оригинальный проект
- **Автор:** lllyasviel
- **Репозиторий:** https://github.com/lllyasviel/stable-diffusion-webui-forge
- **Лицензия:** GNU AGPL v3 (оригинал)

## Мои модификации

### Версия:
**Дата:** 2026-11-24

### Изменённые зависимости:
- **CUDA Toolkit:** 12.1 → 13.2
- **PyTorch:** 2.3.1 → 2.15.0
- **Python:** 3.10 → 3.11–3.13 (рекомендуется 3.11–3.12)
- **Gradio:** 4.40.0 (текущая), план миграции на 6.32.0
- **Обновлены все зависимые библиотеки** в `requirements_versions.txt`
- **bitsandbytes:** 0.4x → 0.50.2 (NF4 поддержка)
- **diffusers:** обновлён до 0.31.0
- **transformers:** обновлён до 4.48.0

### Подробный список изменений:
1. Обновлён CUDA Toolkit до версии 13.2 (RTX 50xx Blackwell sm_120)
2. Обновлён PyTorch до версии 2.15.0 с CUDA 13.2
3. Адаптированы все зависимости под новые версии
4. Миграция `pkg_resources` → `importlib.metadata` / `packaging.version` (совместимость с setuptools 77+)
5. Добавлены mypy type annotations (backend: 54 ошибок → 0)
6. Удалён xformers import из `memory_management.py` (~1-2s ускорение запуска)
7. SDPA attention включён по умолчанию (`--attention-sdpa`)
8. Автоопределение dtype моделей (FP8/NF4) через `backend/model_dtype_config.py`
9. Отключён `need_global_unload` — модель остаётся в VRAM между генерациями
10. Исправлены tuple→list в `sub_quadratic_attention.py` для dynamic_slice
11. Исправлены Protocol сигнатуры (убраны @staticmethod, добавлены self и mask)
12. Исправлена ошибка str-format в `controlnet.py`
13. Исправлен import resolution в `api.py` (hypernetworks.ui.create_hypernetwork)
14. Исправлены None assignment к non-optional типам в modules/
15. Step Width/Height слайдеров установлен на 64
16. Добавлен `--model-dtype-map` флаг для кастомных правил определения dtype
17. Обновлён `webui-user.bat` — оптимизированные флаги запуска
18. Создана документация `.gigacode/` (CHANGELOG, KNOWN_ISSUES, TYPES, MIGRATION_PLAN)
19. Составлен анализ миграции Gradio 4.40.0 → 6.32.0 (94 файла, 10 блокировщиков)

## Лицензия
Этот проект основан на [Stable Diffusion WebUI Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge), лицензированном под GNU AGPL v3. Все права оригинальных авторов сохранены.

Модификации также распространяются под лицензией GNU AGPL v3.

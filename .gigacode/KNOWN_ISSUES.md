# Known Issues — Stable Diffusion WebUI Forge

> Нерешённые проблемы проекта. Обновляется по мере работы над миграцией.

---

## Критические

| # | Описание | Файл | Статус | Комментарии |
|---|----------|------|--------|-------------|
| K01 | `pkg_resources` может быть удалён в setuptools 78+ | modules/textual_inversion/autocrop.py, install.py | ✅ Исправлен | Заменён на `importlib.metadata` / `packaging.version` |
| K02 | xformers конфликтует с CUDA 13.2 | modules/memory_management.py | ✅ Исправлен | xformers удалён, SDPA включён по умолчанию |
| K03 | `TextConditionalModel` закомментирован в sd_hijack_clip.py | modules/sd_hijack_clip.py:30 | 🔴 Открыт | `Sd3ClipLG` в sd3_cond.py не имеет базового класса |
| K04 | `Git.CatFileContentStream` не определён | modules/gitpython_hack.py:26 | 🔴 Открыт | Зависит от версии gitpython |
| K05 | `process_before_every_sampling` определён дважды | modules/scripts.py:848,888 | 🔴 Открыт | Дублирование метода |

## Типовые ошибки mypy (отключены в mypy.ini)

| # | Категория | Кол-во файлов | Статус |
|---|----------|---------------|--------|
| M01 | `var-annotated` (empty dict/list) | ~15 | ⏸ Отключено в mypy.ini |
| M02 | `assignment` (None → non-optional) | ~20 | ⏸ Отключено в mypy.ini |
| M03 | `attr-defined` (динамические атрибуты) | ~10 | ⏸ Отключено в mypy.ini |
| M04 | `arg-type` (несоответствие аргументов) | ~8 | ⏸ Отключено в mypy.ini |
| M05 | `name-defined` (циклические импорты) | 2 | 🔴 Открыт |
| M06 | `misc` (общие ошибки типов) | 5 | ⏸ Отключено в mypy.ini |

## Совместимость

| # | Описание | Статус | Комментарии |
|---|----------|--------|-------------|
| C01 | Surface tablet pressure support | 🔴 Broken | pending fix (с июля 2024) |
| C02 | OFT LoRAs | 🔴 Broken | pending fix (с сентября 2024) |
| C03 | ControlNet Union | ⏸ Not implemented | pending implementation |
| C04 | ControlNet Flux | ⏸ Not implemented | pending implementation |

## Производительность

| # | Описание | Статус | Комментарии |
|---|----------|--------|-------------|
| P01 | PCIe 4.0 x8 bottleneck на 5060 Ti | ℹ️ Known | Model reload ~5-12s via PCIe |
| P02 | DDR4 2400 RAM — медленные CPU↔GPU transfer | ℹ️ Known | Ожидается улучшение с DDR5 |

---

## Статус-код

| Код | Значение |
|-----|----------|
| ✅ | Исправлено |
| 🔴 | Открыта / Требует исправления |
| ⏸ | Отложено / Отключено в mypy.ini |
| ℹ️ | Информационно (не баг) |

---

*Файл ведётся в соответствии с планом `.gigacode/docs/MIGRATION_PLAN.md`, разделы 1 и 6*

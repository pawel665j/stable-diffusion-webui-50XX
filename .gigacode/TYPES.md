# Types — Руководство по аннотациям типов

> Примеры и правила аннотаций типов для проекта Stable Diffusion WebUI Forge.

---

## Правила

1. **Всегда аннотируйте empty dicts и lists** — mypy не может вывести тип.
2. **Используйте `typeshed`-совместимые типы** из `typing` и `typing_extensions`.
3. **Protocol** — используйте единый источник (`typing_extensions` для py3.10-3.11, `typing` для py3.12+).
4. **Optional** — используйте `X | None` для py3.10+.
5. **Type aliases** — выносите сложные типы в отдельные алиасы.

---

## Примеры

### var-annotated (empty dict/list)

```python
# ❌ Плохо
extra_weight_calculators = {}
current_loaded_models = []

# ✅ Хорошо
extra_weight_calculators: dict[type, list[str]] = {}
current_loaded_models: list[ModelType] = []
```

### assignment (None → non-optional)

```python
# ❌ Плохо
class Script:
    some_value: int = None  # type: int, assigned None

# ✅ Хорошо
class Script:
    some_value: int | None = None
    # ИЛИ
    some_value: int = 0
```

### arg-type (tuple → list)

```python
# ❌ Плохо
def dynamic_slice(data: list[int], start: tuple[int, int, int], stop: tuple[int, int, int]):
    ...

# ✅ Хорошо
def dynamic_slice(data: list[int], start: list[int], stop: list[int]):
    ...

# При вызове с tuple — конвертируйте
dynamic_slice(data, list((1, 2, 3)), list((4, 5, 6)))
```

### operator (`in` с Optional)

```python
# ❌ Плохо
values: list[int] | None = None
if 5 in values:  # TypeError if values is None
    ...

# ✅ Хорошо
values: list[int] | None = None
if values is not None and 5 in values:
    ...
```

### Protocol

```python
# ✅ Хорошо — единый импорт
from typing_extensions import Protocol, runtime_checkable

@runtime_checkable
class SummarizeChunk(Protocol):
    def __call__(self, data: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        ...
```

### Type Aliases

```python
from typing import TypeAlias

ModelPath: TypeAlias = str
DeviceType: TypeAlias = str | torch.device
OptionalTuple: TypeAlias = tuple[int, int] | None
```

---

## Часто используемые типы проекта

| Тип | Описание |
|-----|----------|
| `torch.Tensor` | Тензор PyTorch |
| `torch.device` | Устройство (CPU/GPU) |
| `str | None` | Опциональная строка |
| `list[torch.nn.Module]` | Список модулей |
| `dict[str, Any]` | Словарь с произвольными значениями |
| `Callable[..., Any]` | Произвольная callable |
| `Literal["txt2img", "img2img"]` | Строковый литерал |

---

## Настройки mypy для проекта

```ini
[mypy]
strict_optional = True
ignore_missing_imports = True
disable_error_code = import-not-found,import-untyped
```

---

*Файл ведётся в соответствии с планом `.gigacode/docs/MIGRATION_PLAN.md`, раздел 7*

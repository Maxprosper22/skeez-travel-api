from typing import Optional, List, Dict, TypeVar, Any
from typing_extensions import Self  # For Python <3.11; use `typing.Self` in Python 3.11+

# Type variable for generic list items
T = TypeVar("T")

# Custom list class with fixed maximum length
class SlotList(list[T]):
    def __init__(self, slots: list[T] = None, max_length: int = None):
        if max_length is None:
            raise ValueError("max_length must be specified")
        self.max_length = max_length
        slots = slots or []
        if len(slots) > max_length:
            raise ValueError(
                f"Initial items length ({len(slots)}) exceeds max_length ({max_length})"
            )
        super().__init__(slots)

    def append(self, slot: T) -> None:
        if len(self) >= self.max_length:
            raise ValueError(
                f"Cannot append: list length ({len(self)}) would exceed max_length ({self.max_length})"
            )
        super().append(slot)

    def extend(self, slots: list[T]) -> None:
        if len(self) + len(slots) > self.max_length:
            raise ValueError(
                f"Cannot extend: resulting length ({len(self) + len(slots)}) would exceed max_length ({self.max_length})"
            )
        super().extend(slots)

    def insert(self, index: int, slot: T) -> None:
        if len(self) >= self.max_length:
            raise ValueError(
                f"Cannot insert: list length ({len(self)}) would exceed max_length ({self.max_length})"
            )
        super().insert(index, slot)

    def __setitem__(self, index: int | slice, value: Any) -> None:
        # Allow replacing items (no length change) but prevent adding new ones
        if isinstance(index, slice) and len(range(*index.indices(len(self)))) < len(value):
            if len(self) >= self.max_length:
                raise ValueError(
                    f"Cannot set slice: list length ({len(self)}) would exceed max_length ({self.max_length})"
                )
        super().__setitem__(index, value)

    # Optional: Custom representation for clarity
    def __repr__(self) -> str:
        return f"FixedLengthList({super().__repr__()}, max_length={self.max_length})"

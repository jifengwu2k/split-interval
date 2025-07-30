# `split-interval`

A Python function that splits left-closed, right-open intervals into parts relative to a reference interval.

## Functionality

Given two **left-closed, right-open** intervals (reference and target), the function divides the **target** interval into three optional parts:

1. Left portion (before reference)
2. Intersection portion (overlapping with reference)
3. Right portion (after reference)

## Usage

```python
from operator import lt
from typing import Optional, Tuple, TypeVar, Callable

T = TypeVar('T')
Interval = Tuple[T, T]
Comparator = Callable[[T, T], bool]


def split_interval(reference: Interval, target: Interval, comparator: Comparator = lt) -> Tuple[
    Optional[Interval], Optional[Interval], Optional[Interval]]:
    ...
```

### Parameters

- `reference`: Tuple representing the reference interval `[start, end)`
- `target`: Tuple representing the target interval to be split `[start, end)`
- `comparator`: Comparison function defining the ordering (default: `operator.lt`)

### Returns

A tuple of three optional intervals:

1. Left portion (`None` if it doesn't exist)
2. Intersection portion (`None` if it doesn't exist)
3. Right portion (`None` if it doesn't exist)

## Examples

```python
from split_interval import split_interval

# Basic usage
assert split_interval(reference=(5, 10), target=(3, 4)) == ((3, 4), None, None)
assert split_interval(reference=(5, 10), target=(3, 5)) == ((3, 5), None, None)
assert split_interval(reference=(5, 10), target=(3, 6)) == ((3, 5), (5, 6), None)
assert split_interval(reference=(5, 10), target=(3, 10)) == ((3, 5), (5, 10), None)
assert split_interval(reference=(5, 10), target=(3, 11)) == ((3, 5), (5, 10), (10, 11))

assert split_interval(reference=(5, 10), target=(5, 6)) == (None, (5, 6), None)
assert split_interval(reference=(5, 10), target=(5, 10)) == (None, (5, 10), None)
assert split_interval(reference=(5, 10), target=(5, 11)) == (None, (5, 10), (10, 11))
assert split_interval(reference=(5, 10), target=(6, 7)) == (None, (6, 7), None)
assert split_interval(reference=(5, 10), target=(6, 10)) == (None, (6, 10), None)
assert split_interval(reference=(5, 10), target=(6, 11)) == (None, (6, 10), (10, 11))

assert split_interval(reference=(5, 10), target=(10, 11)) == (None, None, (10, 11))
assert split_interval(reference=(5, 10), target=(11, 12)) == (None, None, (11, 12))

# Empty targets
assert split_interval(reference=(5, 10), target=(3, 2)) == ((3, 3), None, None)
assert split_interval(reference=(5, 10), target=(5, 4)) == (None, (5, 5), None)
assert split_interval(reference=(5, 10), target=(10, 9)) == (None, None, (10, 10))

# Works with any comparable type
assert split_interval(reference=('b', 'e'), target=('a', 'e')) == (('a', 'b'), ('b', 'e'), None)

# Use a comparator to redefine `<`
greater_than = lambda a, b: a > b

assert split_interval(reference=(10, 5), target=(4, 3), comparator=greater_than) == (None, None, (4, 3))
assert split_interval(reference=(10, 5), target=(5, 3), comparator=greater_than) == (None, None, (5, 3))
assert split_interval(reference=(10, 5), target=(6, 3), comparator=greater_than) == (None, (6, 5), (5, 3))
assert split_interval(reference=(10, 5), target=(10, 3), comparator=greater_than) == (None, (10, 5), (5, 3))
assert split_interval(reference=(10, 5), target=(11, 3), comparator=greater_than) == ((11, 10), (10, 5), (5, 3))

assert split_interval(reference=(10, 5), target=(10, 5), comparator=greater_than) == (None, (10, 5), None)
assert split_interval(reference=(10, 5), target=(11, 5), comparator=greater_than) == ((11, 10), (10, 5), None)

assert split_interval(reference=(10, 5), target=(11, 10), comparator=greater_than) == ((11, 10), None, None)
```

## Notes

- The comparator should implement strict ordering (like < rather than <=)
- Empty target intervals (`not start < end` with default comparator) will be converted to `[start, start)` (still empty)
- Empty reference intervals (`not start < end` with default comparator) will raise ValueError

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).
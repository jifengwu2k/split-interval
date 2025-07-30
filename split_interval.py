# Copyright (c) 2025 Jifeng Wu
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
from operator import lt
from typing import Optional, Tuple, TypeVar, Callable

T = TypeVar('T')
Interval = Tuple[T, T]
Comparator = Callable[[T, T], bool]


def split_interval(reference, target, comparator=lt):
    # type: (Interval, Interval, Comparator) -> Tuple[Optional[Interval], Optional[Interval], Optional[Interval]]
    """Splits a left-closed, right-open target interval into parts relative to a reference interval.

    Given two left-closed, right-open intervals (reference and target), divides the target
    interval into three optional parts: the portion before the reference, the intersecting
    portion, and the portion after the reference.

    Args:
        reference: A tuple representing the reference interval [start, end).
        target: A tuple representing the target interval to be split [start, end).
        comparator: A comparison function that defines the interval ordering.
            Defaults to operator.lt (less than).

    Returns:
        A tuple of three optional intervals:
        - left: Portion of target interval strictly before reference (None if none exists)
        - intersection: Overlapping portion between target and reference (None if disjoint)
        - right: Portion of target interval strictly after reference (None if none exists)

    Raises:
        ValueError: If either interval is empty (`not (start < end)` when using default comparator)

    Note:
        The comparator function should implement a strict ordering (like `<` rather than `<=`).
    """
    reference_start, reference_stop = reference
    target_start, target_stop = target

    if not comparator(reference_start, reference_stop):
        raise ValueError('reference interval is empty')

    if not comparator(target_start, target_stop):
        target_stop = target_start

    # At this point, comparator(target_start, target_stop) or target_start == target_stop

    has_left = False
    has_intersection = False
    has_right = False

    left_stop_is_target_stop = False
    intersection_start_is_target_start = False
    intersection_stop_is_target_stop = False
    right_start_is_target_start = False

    if comparator(target_start, reference_start):
        has_left = True

        if comparator(reference_stop, target_stop):
            has_intersection = True
            has_right = True
        elif comparator(reference_start, target_stop):
            has_intersection = True
            intersection_stop_is_target_stop = True
        else:
            left_stop_is_target_stop = True
    elif comparator(target_start, reference_stop):
        has_intersection = True
        intersection_start_is_target_start = True

        if comparator(reference_stop, target_stop):
            has_right = True
        else:
            intersection_stop_is_target_stop = True
    else:
        has_right = True

        right_start_is_target_start = True

    if has_left:
        if left_stop_is_target_stop:
            left_stop = target_stop
        else:
            left_stop = reference_start

        left = (target_start, left_stop)
    else:
        left = None

    if has_intersection:
        if intersection_start_is_target_start:
            intersection_start = target_start
        else:
            intersection_start = reference_start

        if intersection_stop_is_target_stop:
            intersection_stop = target_stop
        else:
            intersection_stop = reference_stop

        intersection = (intersection_start, intersection_stop)
    else:
        intersection = None

    if has_right:
        if right_start_is_target_start:
            right_start = target_start
        else:
            right_start = reference_stop

        right = (right_start, target_stop)
    else:
        right = None

    return left, intersection, right

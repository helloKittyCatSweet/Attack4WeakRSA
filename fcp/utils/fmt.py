"""
Formatting utilities for display and output
"""

from typing import List, Dict, Any


def human_readable_int(n: int) -> str:
    """
    Format integer with underscores for readability.

    Args:
        n: Integer to format

    Returns:
        Formatted string with underscores as thousand separators

    Example:
        >>> human_readable_int(1234567)
        '1_234_567'
    """
    return f"{n:,}".replace(",", "_")


def format_timing_statistics(timings: List[float]) -> Dict[str, Any]:
    """
    Calculate timing statistics from a list of times in milliseconds.

    Args:
        timings: List of timing measurements in milliseconds

    Returns:
        Dictionary with keys: 'average', 'best', 'worst', 'count'
        Empty dict if timings is empty

    Example:
        >>> format_timing_statistics([1.0, 2.0, 3.0])
        {'average': 2.0, 'best': 1.0, 'worst': 3.0, 'count': 3}
    """
    if not timings:
        return {}

    return {
        'average': sum(timings) / len(timings),
        'best': min(timings),
        'worst': max(timings),
        'count': len(timings)
    }


def print_timing_stats(stats: Dict[str, Any]) -> None:
    """
    Print formatted timing statistics.

    Args:
        stats: Statistics dictionary from format_timing_statistics()

    Example:
        >>> stats = {'average': 2.5, 'best': 1.0, 'worst': 4.0, 'count': 3}
        >>> print_timing_stats(stats)
        Timing over 3 runs:
          Average: 2.50 ms
          Best:    1.00 ms
          Worst:   4.00 ms
    """
    if not stats:
        return

    print(f"Timing over {stats['count']} runs:")
    print(f"  Average: {stats['average']:.2f} ms")
    print(f"  Best:    {stats['best']:.2f} ms")
    print(f"  Worst:   {stats['worst']:.2f} ms")


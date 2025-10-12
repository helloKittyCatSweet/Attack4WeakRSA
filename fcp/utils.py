"""
Utility functions for formatting and display
"""

def human_readable_int(n):
    """Format integer with underscores for readability"""
    return f"{n:,}".replace(",", "_")

def format_timing_statistics(timings):
    """Calculate timing statistics from a list of times in milliseconds"""
    if not timings:
        return {}

    return {
        'average': sum(timings) / len(timings),
        'best': min(timings),
        'worst': max(timings),
        'count': len(timings)
    }

def print_timing_stats(stats):
    """Print formatted timing statistics"""
    if not stats:
        return

    print(f"Timing over {stats['count']} runs:")
    print(f"  Average: {stats['average']:.2f} ms")
    print(f"  Best:    {stats['best']:.2f} ms")
    print(f"  Worst:   {stats['worst']:.2f} ms")

def validate_parameters(bits, max_gap, safe_params):
    """Validate that parameters are within safe demonstration ranges"""
    if bits < safe_params['min_bits']:
        print(f"Warning: bits too small, using minimum {safe_params['min_bits']}")
        return False
    if bits > safe_params['max_bits']:
        print(f"Warning: bits very large, may take long time")
    if max_gap > safe_params['max_gap_limit']:
        print(f"Warning: max_gap very large, may take long time")
    return True
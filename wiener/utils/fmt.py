"""
Formatting utilities

Helper functions for formatting output.
"""


def format_time(seconds: float) -> str:
    """
    Format time in human-readable format
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted string (e.g., "1.234 ms", "2.345 s")
    """
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.3f} μs"
    elif seconds < 1:
        return f"{seconds * 1000:.3f} ms"
    elif seconds < 60:
        return f"{seconds:.3f} s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"


def format_number(n: int, use_scientific: bool = True) -> str:
    """
    Format large number
    
    Args:
        n: Number to format
        use_scientific: Use scientific notation for large numbers
        
    Returns:
        Formatted string
    """
    if use_scientific and n > 1e6:
        return f"{n:.2e}"
    else:
        return f"{n:,}"


def format_bits(n: int) -> str:
    """
    Format number with bit length
    
    Args:
        n: Number
        
    Returns:
        Formatted string (e.g., "12345 (14 bits)")
    """
    return f"{n} ({n.bit_length()} bits)"


def format_percentage(value: float, total: float) -> str:
    """
    Format percentage
    
    Args:
        value: Numerator
        total: Denominator
        
    Returns:
        Formatted string (e.g., "75.0%")
    """
    if total == 0:
        return "N/A"
    return f"{(value / total) * 100:.1f}%"


def format_ratio(a: float, b: float) -> str:
    """
    Format ratio
    
    Args:
        a: First value
        b: Second value
        
    Returns:
        Formatted string (e.g., "2.5x")
    """
    if b == 0:
        return "N/A"
    return f"{a / b:.2f}x"


def pretty_table(headers: list, rows: list, col_widths: list = None) -> str:
    """
    Create a pretty table
    
    Args:
        headers: List of column headers
        rows: List of rows (each row is a list of values)
        col_widths: Optional list of column widths
        
    Returns:
        Formatted table string
    """
    if not col_widths:
        # Auto-calculate column widths
        col_widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Add padding
    col_widths = [w + 2 for w in col_widths]
    
    # Build table
    lines = []
    
    # Header
    header_line = "  " + "".join(f"{str(h):<{w}}" for h, w in zip(headers, col_widths))
    lines.append(header_line)
    lines.append("  " + "-" * sum(col_widths))
    
    # Rows
    for row in rows:
        row_line = "  " + "".join(f"{str(cell):<{w}}" for cell, w in zip(row, col_widths))
        lines.append(row_line)
    
    return "\n".join(lines)


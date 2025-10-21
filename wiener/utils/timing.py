"""
Timing utilities

Decorators and functions for measuring execution time.
"""

import time
import functools
from typing import Callable, Any, Tuple


def timed(func: Callable) -> Callable:
    """
    Decorator to measure function execution time
    
    Returns function result and elapsed time in seconds.
    Does NOT print - caller decides what to do with timing info.
    
    Usage:
        @timed
        def my_function(x):
            return x * 2
        
        result, elapsed = my_function(5)
        print(f"Result: {result}, Time: {elapsed:.3f}s")
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[Any, float]:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed
    return wrapper


def measure_time(func: Callable, *args, **kwargs) -> Tuple[Any, float]:
    """
    Measure execution time of a function call
    
    Args:
        func: Function to call
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func
        
    Returns:
        (result, elapsed_time): Function result and time in seconds
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


class Timer:
    """Context manager for timing code blocks"""
    
    def __init__(self):
        self.start_time = None
        self.elapsed = None
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start_time
    
    def get_elapsed(self) -> float:
        """Get elapsed time in seconds"""
        return self.elapsed if self.elapsed is not None else 0.0
    
    def get_elapsed_ms(self) -> float:
        """Get elapsed time in milliseconds"""
        return self.get_elapsed() * 1000


"""
Runner module for Wiener Attack demonstrations

Handles all user I/O and interactions.
"""

from .demo import run_single_attack, run_comparison, run_demonstration
from .visualizer import print_attack_result, print_comparison_table, print_boundary_comparison

__all__ = [
    'run_single_attack',
    'run_comparison',
    'run_demonstration',
    'print_attack_result',
    'print_comparison_table',
    'print_boundary_comparison',
]


"""
Wiener Attack and Improvements

Implementation of Wiener attack and its improvements:
- Original Wiener Attack (1990)
- Bunder-Tonien Attack (2017)
- New Boundary Attack (2023)
"""

from .core import (
    WienerAttack,
    BunderTonienAttack,
    NewBoundaryAttack,
    WeakRSAGenerator,
    ContinuedFraction,
)

from .runner import (
    run_single_attack,
    run_comparison,
    run_demonstration,
)

__version__ = '2.0.0'

__all__ = [
    'WienerAttack',
    'BunderTonienAttack',
    'NewBoundaryAttack',
    'WeakRSAGenerator',
    'ContinuedFraction',
    'run_single_attack',
    'run_comparison',
    'run_demonstration',
]


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmark module for RSA Partial Key Exposure Attack

Runs batch tests and collects statistics.
"""

from typing import List, Dict
from dataclasses import dataclass, field
import time

# Handle both direct and module execution
try:
    from config import RSAConfig, ExperimentConfig
    from demo.main_demo import run_single_attack
except ImportError:
    from ..config import RSAConfig, ExperimentConfig
    from .main_demo import run_single_attack


@dataclass
class BenchmarkConfig:
    """
    Configuration for benchmark
    
    Attributes:
        num_trials: Number of trials per configuration
        bit_lengths: List of bit lengths to test
        deltas: List of exposure ratios to test
        exposure_types: List of exposure types to test
    """
    num_trials: int = 5
    bit_lengths: List[int] = field(default_factory=lambda: [16, 18, 20])
    deltas: List[float] = field(default_factory=lambda: [0.6, 0.7, 0.8])
    exposure_types: List[str] = field(default_factory=lambda: ["MSB"])


@dataclass
class BenchmarkResult:
    """
    Result of benchmark
    
    Attributes:
        config_name: Configuration description
        num_trials: Number of trials
        num_success: Number of successful attacks
        success_rate: Success rate (0-1)
        avg_time: Average time per attack (seconds)
        min_time: Minimum time
        max_time: Maximum time
    """
    config_name: str
    num_trials: int
    num_success: int
    success_rate: float
    avg_time: float
    min_time: float
    max_time: float


def run_benchmark(config: BenchmarkConfig = None) -> List[BenchmarkResult]:
    """
    Run benchmark with given configuration

    Args:
        config: Benchmark configuration (uses default if None)

    Returns:
        List of BenchmarkResult for each configuration tested
    """
    if config is None:
        config = BenchmarkConfig()

    print("=" * 80)
    print("RSA Partial Key Exposure Attack - Benchmark")
    print("=" * 80)
    print(f"Trials per configuration: {config.num_trials}")
    print(f"Bit lengths: {config.bit_lengths}")
    print(f"Deltas: {config.deltas}")
    print(f"Exposure types: {config.exposure_types}")
    print("=" * 80)
    
    results = []

    # Test all combinations
    for bit_length in config.bit_lengths:
        for delta in config.deltas:
            for exp_type in config.exposure_types:
                config_name = f"{bit_length}-bit, δ={delta:.1f}, {exp_type}"

                print(f"\n[*] Testing: {config_name}")

                # Setup configurations
                rsa_config = RSAConfig(bit_length=bit_length, r=2, s=1)
                exp_config = ExperimentConfig(
                    delta=delta,
                    exposure_type=exp_type,
                    m=2 if bit_length <= 18 else 3,
                    t=1 if bit_length <= 18 else 2
                )

                # Run trials
                successes = 0
                times = []

                for trial in range(config.num_trials):
                    print(f"    Trial {trial + 1}/{config.num_trials}...", end=" ")

                    start_time = time.time()
                    success = run_single_attack(rsa_config, exp_config, verbose=False)
                    elapsed = time.time() - start_time

                    times.append(elapsed)
                    if success:
                        successes += 1
                        print(f"✓ ({elapsed:.3f}s)")
                    else:
                        print(f"✗ ({elapsed:.3f}s)")

                # Calculate statistics
                success_rate = successes / config.num_trials
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)

                result = BenchmarkResult(
                    config_name=config_name,
                    num_trials=config.num_trials,
                    num_success=successes,
                    success_rate=success_rate,
                    avg_time=avg_time,
                    min_time=min_time,
                    max_time=max_time
                )

                results.append(result)

                print(f"    Success rate: {successes}/{config.num_trials} ({success_rate*100:.1f}%)")
                print(f"    Avg time: {avg_time:.3f}s (min: {min_time:.3f}s, max: {max_time:.3f}s)")
    
    # Print summary
    print_benchmark_summary(results)
    
    return results


def print_benchmark_summary(results: List[BenchmarkResult]):
    """
    Print formatted benchmark summary

    Args:
        results: List of benchmark results
    """
    print("\n" + "=" * 80)
    print("Benchmark Summary")
    print("=" * 80)

    # Table header
    print(f"{'Configuration':<30} {'Success Rate':<15} {'Avg Time':<15}")
    print("-" * 80)

    # Table rows
    for result in results:
        success_str = f"{result.num_success}/{result.num_trials} ({result.success_rate*100:.1f}%)"
        time_str = f"{result.avg_time:.3f}s"
        print(f"{result.config_name:<30} {success_str:<15} {time_str:<15}")

    print("=" * 80)

    # Overall statistics
    total_trials = sum(r.num_trials for r in results)
    total_success = sum(r.num_success for r in results)
    overall_rate = total_success / total_trials if total_trials > 0 else 0

    print(f"\nOverall Success Rate: {total_success}/{total_trials} ({overall_rate*100:.1f}%)")
    print("=" * 80)


if __name__ == "__main__":
    # Run benchmark with default config
    run_benchmark()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLL lattice reduction algorithm implementation
"""

import math
from typing import List, Tuple


class ImprovedLLL:
    """Improved LLL lattice reduction algorithm"""

    def __init__(self, delta: float = 0.99):  # Use higher delta for better success rate
        self.delta = delta

    def gram_schmidt(self, B: List[List[int]]) -> Tuple[List[List[float]], List[List[float]]]:
        """Gram-Schmidt orthogonalization"""
        m = len(B)
        n = len(B[0])

        B_star = [[0.0] * n for _ in range(m)]
        mu = [[0.0] * m for _ in range(m)]

        for i in range(m):
            # Copy current vector
            v = [float(x) for x in B[i]]

            for j in range(i):
                # Calculate projection coefficients
                dot_product = sum(B[i][k] * B_star[j][k] for k in range(n))
                norm_sq = sum(B_star[j][k] * B_star[j][k] for k in range(n))

                if norm_sq != 0:
                    mu[i][j] = dot_product / norm_sq
                else:
                    mu[i][j] = 0.0

                # Subtract projection
                for k in range(n):
                    v[k] -= mu[i][j] * B_star[j][k]

            B_star[i] = v

        return B_star, mu

    def reduce(self, B: List[List[int]]) -> List[List[int]]:
        """Perform LLL reduction"""
        m = len(B)
        if m <= 1:
            return B

        B_reduced = [row[:] for row in B]  # Copy matrix
        B_star, mu = self.gram_schmidt(B_reduced)

        k = 1
        while k < m:
            # Size-reduce
            for j in range(k - 1, -1, -1):
                if abs(mu[k][j]) > 0.5:
                    q = round(mu[k][j])
                    for i in range(len(B_reduced[0])):
                        B_reduced[k][i] -= q * B_reduced[j][i]

                    # Update mu
                    B_star, mu = self.gram_schmidt(B_reduced)

            # Lovasz condition
            norm_B_star_k_minus_1 = sum(x * x for x in B_star[k - 1])
            norm_B_star_k = sum(x * x for x in B_star[k])

            if norm_B_star_k >= (self.delta - mu[k][k - 1] ** 2) * norm_B_star_k_minus_1:
                k += 1
            else:
                # Swap rows
                B_reduced[k - 1], B_reduced[k] = B_reduced[k], B_reduced[k - 1]
                B_star, mu = self.gram_schmidt(B_reduced)
                k = max(k - 1, 1)

        return B_reduced

    def get_shortest_vector(self, lattice: List[List[int]]) -> List[int]:
        """Get the shortest vector from reduced lattice"""
        reduced = self.reduce(lattice)

        # Find vector with smallest norm
        shortest_idx = 0
        shortest_norm = float('inf')

        for i, vector in enumerate(reduced):
            norm = math.sqrt(sum(x * x for x in vector))
            if norm < shortest_norm and norm > 0:  # Avoid zero vector
                shortest_norm = norm
                shortest_idx = i

        return reduced[shortest_idx]
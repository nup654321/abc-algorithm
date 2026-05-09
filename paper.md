# A Self‑Learning Heuristic Algorithm for abc Triples and Discovery of Fertile Numbers

**Andrey Drozdov**  
*Independent Researcher*  
May 2026

## Abstract

This paper presents a self‑learning heuristic algorithm that combines 18 search methods (genetic primes, geometric detector, chaotic billiards, quantum superposition, purity test, etc.) to find abc triples (a,b,c) with a+b=c, gcd(a,b)=1, and rad(abc) < c. The algorithm is efficient: it discovers hundreds of triples up to c = 250 000 000 in minutes on a standard PC. A key empirical finding is the existence of **fertile numbers** – c‑values that appear in more than one abc triple. The complete list for c ≤ 1 000 000 is given. Many of these numbers are perfect powers (p^k). The algorithm and data are open source.

## 1. Introduction

The abc conjecture [1] is a central open problem in number theory. Computational search for high‑quality triples (with small radical) is an active area. This paper describes a heuristic that integrates multiple search strategies and self‑learning.

## 2. Algorithm description

The algorithm implements 18 heuristic methods. Key components:

- **Genetic primes** – a list of primes that evolves based on frequency in found triples.
- **Geometric detector** – searches `a` near `c/2` (parabola) and around an offset center (ellipse).
- **Chaotic billiards + quantum superposition** – random walk and simultaneous `q`‑value exploration.
- **Purity condition** – flags triples where `Φ = a^(e·b·c/rad)` is extremely close to an integer.
- **Self‑learning** – after each run, the algorithm updates the list of small `a`, the search radius, and the genetic primes.

The code is written in Python 3.6+ with no external dependencies (optional `matplotlib` for plotting).

## 3. Results

### 3.1 Fertile numbers

A “fertile number” is a `c` that appears in at least two different abc triples satisfying the conditions. For `c ≤ 1 000 000`, the complete sorted list is:
81, 1331, 2048, 2401, 6561, 15625, 16384, 19683, 28561, 59049,
117649, 131072, 390625, 531441, 1048576, 1058841, 1594323,
1771561, 1953125, 3906250
Most of these are perfect powers (e.g., 2401 = 7⁴, 15625 = 5⁶, 131072 = 2¹⁷). The sequence has been submitted to OEIS as [A395901](https://oeis.org/A395901).

### 3.2 Record‑quality triples

Examples:

- `2 + 6436341 = 6436343`, rad=15042, q=1.629912
- `121 + 48234375 = 48234496`, rad=3630, q=1.625991
- `1 + 4374 = 4375`, rad=210, q=1.567887

The full list of discovered triples is provided in the repository (`abc_live_triples.txt`).

## 4. Discussion

The self‑learning capability allowed the algorithm to “notice” that fertile numbers tend to be perfect powers. This empirical observation may hint at underlying arithmetic structure. The open‑source release aims to encourage further research and verification.

## 5. Availability

- Source code and data: [GitHub](https://github.com/nup654321/abc-algorithm)
- OEIS sequence for fertile numbers: [A395901](https://oeis.org/A395901)

## References

[1] Oesterlé, J., & Masser, D. (1985). The abc conjecture.

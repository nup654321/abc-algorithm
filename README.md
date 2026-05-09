# Algorithm for Searching abc Triples with Self‑Learning Heuristics: A Scientific Workflow

**Author:** Andrey Drozdov  
**OEIS sequences (discovered by this algorithm):** [A395901](https://oeis.org/A395901) (fertile c), [A395816](https://oeis.org/A395816) (c with q>1.2), [A395858](https://oeis.org/A395858) (pure c)  
**License:** MIT  

## Abstract

This repository presents a heuristic algorithm for searching abc triples (a,b,c) with a+b=c, gcd(a,b)=1, and rad(a*b*c) < c. The algorithm integrates **18 heuristic methods**, grouped into four super‑methods (A, B, C, D), and uses **self‑learning** to adapt its parameters. It discovers hundreds of triples up to c = 250 000 000 in minutes on a standard PC. As a by‑product, it revealed **fertile numbers** (c‑values appearing in more than one triple) and record‑quality triples (e.g., 2+6436341=6436343, q=1.629912). The code is open‑source, fully documented, and includes an interactive command‑line interface.

## 1. Introduction

The abc conjecture is a central open problem in number theory. Computational search for triples with small radical (rad(abc) < c) is essential for empirical testing. This paper describes a self‑learning heuristic that efficiently finds such triples using a combination of 18 methods. The algorithm automatically improves its parameters (list of small a, search radius, genetic primes) based on discovered triples.

## 2. The 18 heuristic methods

The algorithm implements 18 methods, organised into four **super‑methods**:

### Super‑method A: Genetic resonance (methods 1,3,11,12,16)

- **Method 1 – Deformation p³/q** – for a prime `p` and integer `q`, generate `c = p^k` (k=2..5) and `a = floor(c/q)`, `b = c-a`.  
- **Method 3 – Continued fractions for log₂3** – generate `c = |2^m ± 3^n|`.  
- **Method 11 – Small a list** – iterate `a` from a fixed list (evolves via self‑learning).  
- **Method 12 – Genetic resonance** – same as method 1 but using genetic primes.  
- **Method 16 – Quantum superposition** – simultaneously explore many `q` values for deformation.  

**Purpose:** Generate candidate `c` as powers, sums/differences of powers, and test small `a`.

### Super‑method B: Geometric detector (methods 5,6,10,13,14)

- **Method 5 – Parabola** – search `a` near `c/2` (center ± radius, step 50).  
- **Method 6 – Ellipse** – shift centre by offset ~ log(rad(c))/log(c) and search.  
- **Method 10 – Complex deformation** – rotate a point (p,0) by angles π/6, π/4, π/3, round to integers for `a` and `b`.  
- **Method 13 – Intersection** – combination of parabola and ellipse.  
- **Method 14 – Sieve** – fast pruning: reject if `rad(a)*rad(c) > c` or `rad(a) > c^0.6`.  

**Purpose:** Search `a` in geometrically significant regions close to `c/2` or shifted.

### Super‑method C: Chaotic billiards and quantum superposition (methods 15,16)

- **Method 15 – Chaotic billiards** – random walk of `a` between 1 and `c/2` with reflections.  
- **Method 16 – Quantum superposition** – for `c` close to a perfect power, try many `q` in `p³/q`.  

**Purpose:** Explore non‑deterministic regions, find triples missed by deterministic searches.

### Super‑method D: Exact small‑a search (method 17)

- **Method 17 – Exact small‑a** – iterate over all `a` from the `SMALL_A_LIST` for every candidate `c`.  

**Purpose:** Ensure completeness for small `a`, which often yield high‑quality triples.

### Additional methods (2,4,7,8,9,18)

- **Method 2 – Purity theory** – compute `Φ = a^(e·b·c/rad(abc))` and check if `|Φ - round(Φ)| < 1e-7`.  
- **Method 4 – Resonance diagnostic** – internal diagnostic, not used for searching.  
- **Method 7 – Smooth numbers** – generate numbers with prime divisors ≤ 199.  
- **Method 8 – c selection** – keep only `c` with `rad(c) < c^θ` (θ=0.45).  
- **Method 9 – Logarithmic forms** – for small primes p1,p2, set `c = max(p1^n, p2^m)`, `a = |p1^n - p2^m|`.  
- **Method 18 – Super‑method A (wrapper)** – combines methods 1,3,11,12,16.

## 3. Self‑learning mechanism

After each run, the algorithm analyses all discovered triples and updates:

- **Small‑a list** – adds any `a ≤ 2000` that appears in a triple with quality `q > 1.4`.  
- **Search radius** – sets radius = 95th percentile of distances `|a - c/2|` (capped between 3000 and 20000).  
- **Genetic primes** – recomputes prime weights based on frequency of primes in `a,b,c` weighted by `(q - 1.2 + 0.5)`, keeps top 15.

The updated parameters are saved to `abc_model.json` and used in subsequent runs.

## 4. Running the algorithm

### Requirements

- Python 3.6 or higher.
- No external libraries required (optional: `matplotlib` for plotting).

### Installation

```bash
git clone https://github.com/nup654321/abc-algorithm.git
cd abc-algorithm
Basic usage
python abc_triple_modes.py
This starts an interactive menu. Then you can enter commands (see below).

Interactive commands
Command	Description
run	Standard search using active super‑methods (A, B, D by default).
fast	Fast search – only small a from the SMALL_A_LIST.
full	Exhaustive search – for each c generated from powers of primes, test every a from 1 to c/2 (slow, but no misses).
super A/B/C/D	Toggle a super‑method on/off.
set limit N	Set LIMIT_C (max c, default 250 000 000).
set smooth N	Set LIMIT_SMOOTH (max for smooth numbers, default 30 000 000).
set quality N	Minimum quality q (default 1.20).
set threshold N	Threshold for rad(c) < c^threshold (default 0.45).
set radius N	Search radius for parabola/ellipse (default 5000).
set small "a1,a2,…"	Set the list of small a for fast mode and method D.
set full_max_c N	Max c for full mode (default 10 000 000).
stats	Show statistics of found triples (count, max/average q, top 5).
fertile	Show fertile numbers (c with multiple triples) from current run.
pure	Show pure triples (marked ✨) from current run.
methods	Show per‑method counts.
model	Show current learned model (genetic primes, optimal radius, small‑a list).
optimize	Automatically disable super‑methods that found zero triples.
save	Save current configuration and model to files.
clear	Clear all found triples (start fresh).
quit	Exit the program.
Example session
> set limit 500000000
> set smooth 500000000
> set small "1,2,3,5,7,11,13"
> fast
> stats
> fertile
> save
> quit
5. Results
5.1 Fertile numbers (OEIS A395901)
The algorithm discovered that certain c appear in more than one abc triple. Below is the complete list for c ≤ 1 000 000 (computed without quality filtering, only rad(abc) < c and gcd(a,b)=1):
81, 1331, 2048, 2401, 6561, 15625, 16384, 19683, 28561, 59049,
117649, 131072, 390625, 531441, 1048576, 1058841, 1594323,
1771561, 1953125, 3906250
Many are perfect powers (e.g., 2401 = 7^4, 15625 = 5^6, 131072 = 2^17, 390625 = 5^8). This sequence has been submitted to OEIS as A395901.

5.2 Record‑quality triples
The algorithm reproduced known record triples and discovered several with extremely high quality. Examples:

Triple	rad(abc)	quality q
2 + 6436341 = 6436343	15042	1.629912
121 + 48234375 = 48234496	3630	1.625991
1 + 4374 = 4375	210	1.567887
... (full list in abc_live_triples.txt)	...	...
5.3 Pure triples (purity condition)
Triples marked with ✨ satisfy the purity condition |Φ - round(Φ)| < 1e-7. Many of these have a=1 and also appear in the fertile list. See abc_pure_triples.txt.

6. Output files
File	Content
abc_live_triples.txt	All discovered triples (timestamp, a+b=c, q, rad, purity marker ✨).
abc_backup.txt	Backup copy.
abc_fertile_c.txt	Fertile numbers (c with ≥2 triples) from the current run.
abc_pure_triples.txt	Pure triples (✨) from the current run.
abc_model.json	Learned parameters (small‑a list, genetic primes, optimal radius).
7. Discussion
The self‑learning capability allowed the algorithm to “notice” that fertile numbers tend to be perfect powers. This observation suggests a potential arithmetic structure. The code is open‑source to facilitate verification and further research.

8. Citation
If you use this algorithm or its results in your research, please cite:
@software{Drozdov2026_abc,
  author = {Drozdov, Andrey},
  title = {Self‑learning heuristic for abc triples},
  year = {2026},
  url = {https://github.com/nup654321/abc-algorithm},
  note = {Includes discovery of fertile numbers (OEIS A395901)}
}

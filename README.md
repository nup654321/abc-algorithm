# Algorithm for Searching abc Triples with Self‑Learning Heuristics

**Author:** Andrey Drozdov  
**OEIS sequences (discovered by this algorithm):** [A395901](https://oeis.org/A395901) (fertile c), [A395816](https://oeis.org/A395816) (c with q>1.2), [A395858](https://oeis.org/A395858) (pure c)  
**License:** MIT  

## Abstract

This repository contains a **self‑learning heuristic algorithm whose primary purpose is to find abc triples** (a,b,c) with a+b=c, gcd(a,b)=1, and rad(a*b*c) < c. The algorithm integrates 18 search methods (genetic primes, geometric detectors, chaotic billiards, quantum superposition, purity test, etc.) and uses self‑learning to improve its parameters over time.

The algorithm has discovered hundreds of triples up to c = 250 000 000, including record‑quality examples (e.g., 2+6436341=6436343, q=1.629912). As a by‑product, it also revealed **fertile numbers** – c‑values that appear in more than one abc triple – and other structural observations.

## Table of Contents

- [Algorithm description](#algorithm-description)
- [Main results](#main-results)
- [Running the algorithm](#running-the-algorithm)
- [Commands reference](#commands-reference)
- [Output files](#output-files)
- [Citation](#citation)
- [License](#license)

## Algorithm description

The algorithm is designed to efficiently search for abc triples by combining multiple heuristic strategies. Its core components are:

1. **Genetic primes** – a list of primes that evolves based on frequency in found triples, used to generate candidate c.
2. **Geometric detector** – searches a in the vicinity of c/2 (parabola) and around an offset center (ellipse).
3. **Chaotic billiards + quantum superposition** – random walk and simultaneous q‑value exploration to find non‑obvious triples.
4. **Purity condition** – a novel heuristic that flags triples with special structure (not required for the main goal, but helps validation).
5. **Self‑learning** – after each run, the algorithm updates parameters (small‑a list, search radius, genetic primes) to improve future searches.

The code is written in Python 3.6+ and uses only standard libraries. No external dependencies are required (except optional `matplotlib` for plotting).
## Main results

### Fertile numbers (OEIS A395901)

The following numbers c (c ≤ 1 000 000) appear in at least two different abc triples with rad(abc) < c and gcd(a,b)=1:
81, 1331, 2048, 2401, 6561, 15625, 16384, 19683, 28561, 59049,
117649, 131072, 390625, 531441, 1048576, 1058841, 1594323,
1771561, 1953125, 3906250

Many are perfect powers: e.g., 2401 = 7⁴, 15625 = 5⁶, 131072 = 2¹⁷, 390625 = 5⁸.

### Record‑quality triples

| Triple | rad(abc) | quality q |
|--------|----------|-----------|
| 2 + 6436341 = 6436343 | 15042 | 1.629912 |
| 121 + 48234375 = 48234496 | 3630 | 1.625991 |
| 1 + 4374 = 4375 | 210 | 1.567887 |
| ... (see `triples_examples.txt`) | ... | ... |

All discovered triples are stored in `abc_live_triples.txt` (generated when you run the algorithm).

## Running the algorithm

### Requirements

- Python 3.6 or higher
- No external libraries needed (basic installation is sufficient)

### Quick start

```bash
git clone https://github.com/nup654321/abc-algorithm.git
cd abc-algorithm
python abc_triple_modes.py
Then enter commands at the > prompt.

Commands reference
Command	Description
run	Standard search (all active super‑methods A, B, D by default)
fast	Fast search – only small a from the small list
full	Exhaustive search (all a for c generated from powers of primes)
super A/B/C/D	Enable/disable specific super‑method
set limit N	Upper bound for c (default 250 000 000)
set smooth N	Upper bound for smooth numbers (default 30 000 000)
set quality N	Minimum quality q (default 1.20)
set threshold N	Filter: rad(c) < c^threshold (default 0.45)
set radius N	Search radius for parabola/ellipse (default 5000)
set small "a1,a2,…"	List of small a (default 1,2,3,5,7,11,13)
set full_max_c N	Max c for full mode (default 10 000 000)
stats	Show triple statistics
fertile	Show fertile numbers found so far
pure	Show pure triples (satisfying purity condition)
methods	Show per‑method statistics
model	Display learned model
optimize	Automatically disable super‑methods that found zero triples
save	Save configuration and model
clear	Clear all found triples
quit	Exit
Output files
File	Content
abc_live_triples.txt	All discovered triples (timestamp, a+b=c, q, rad, purity marker ✨)
abc_backup.txt	Backup copy
abc_fertile_c.txt	Fertile numbers found during the current run
abc_pure_triples.txt	Pure triples
abc_model.json	Learned parameters (small‑a list, genetic primes, optimal radius)
Citation
If you use this algorithm or its results in your research, please cite:
@software{Drozdov2026_abc,
  author = {Drozdov, Andrey},
  title = {Self‑learning heuristic for abc triples},
  year = {2026},
  url = {https://github.com/nup654321/abc-algorithm},
  note = {Includes discovery of fertile numbers (OEIS A395901)}
}

# ABC-Algorithm

Self‑learning heuristic search for abc triples.  
Discoverer of OEIS sequence **[A395816](https://oeis.org/A395816)** (c‑values with quality > 1.2).

## Algorithm

The code combines several search strategies:
- **Genetic primes** – the set of “genetic” primes evolves based on factors of found triples.
- **Geometric detector** – searches for `a` near `c/2` (parabola) and around an ellipse‑shifted centre.
- **Chaotic billiards** – random walk exploring the search space.
- **Quantum superposition** – explores different `q` for the deformation `p³/q`.
- **Purity theory** – a heuristic that marks triples with a special condition (✨).

## Commands and default values

| Command | Description | Default |
|---------|-------------|---------|
| `set limit N` | Upper bound for `c` | 250 000 000 |
| `set smooth N` | Upper bound for smooth numbers | 50 000 000 |
| `set quality N` | Minimum quality `q = log(c)/log(rad(abc))` | 1.20 |
| `set threshold N` | Candidate filter: `rad(c) < c^threshold` | 0.45 |
| `set radius N` | Search radius for parabola / ellipse | 5000 |
| `set workers N` | Number of parallel threads | CPU count |
| `set small "a1,a2,…"` | List of small `a` for `fast` mode and method D | 1,2,3,5 |
| `set full_max_c N` | Maximum `c` for `full` mode | 10 000 000 |
| `set full_genetic "p1,p2,…"` | Primes used to generate `c` in `full` mode | 2,3,5,7,11,13 |

### Super‑methods (toggle with `super A`, `super B`, `super C`, `super D`)

| Method | Name | Description |
|--------|------|-------------|
| A | Genetic resonance | Generates `c` from powers, products, sums/differences of genetic primes; tests small `a`. |
| B | Geometric detector | Searches `a` near `c/2` (parabola) and around ellipse‑shifted centre. |
| C | Chaotic & quantum | Random walk (billiard) + superposition of `q` for `p³/q`. |
| D | Exact small‑`a` | Iterates over the `small` list for every candidate `c`. |

### How super‑methods work (detailed)

- **Method A (Genetic resonance)**  
  Generates candidate `c` as: powers of genetic primes (`p^e`), products of two powers (`p1^e1 * p2^e2`), sums and absolute differences of powers. For each `c`, it tests `a` from a small fixed list (1,2,3,5,7,11,13,17,19,23) plus `a=1` separately.

- **Method B (Geometric detector)**  
  For a given `c`, it computes `center = c//2` and tests `a = center ± k*step` within radius `PREDICTION_RADIUS` (parabola). Also, if `rad(c)` is small, it shifts the centre by an offset dependent on `log(rad(c))/log(c)` and tests an ellipse‑shaped neighbourhood.

- **Method C (Chaotic billiard + quantum superposition)**  
  Performs a random walk from a random starting `a`, reflecting at boundaries `[1, c//2]`. Additionally, for `c` close to a perfect power `p^e`, it tries `a = floor(p^e / q)` for many `q` (superposition).

- **Method D (Exact small‑a)**  
  Simply iterates over the user‑supplied `small` list (or default `[1,2,3,5]`) for every candidate `c` from the smooth‑number sieve.

### Information and actions

| Command | Effect |
|---------|--------|
| `stats` | Show number of triples, max/average quality, top 5 triples. |
| `fertile` | Show numbers `c` that appear in more than one triple. |
| `pure` | Show pure triples (marked `✨`). |
| `methods` | Show per‑method statistics (methods 1‑17). |
| `model` | Display the learned model (genetic primes, optimal radius). |
| `optimize` | Automatically disable super‑methods that found zero triples. |
| `save` | Save current configuration and learned model. |
| `clear` | Clear all found triples. |
| `run` | Standard search (all active super‑methods). |
| `fast` | Fast search: **only** small `a` from the `small` list, no other methods. |
| `full` | Exhaustive search: for `c` generated from `full_genetic` primes, test **every** `a` from 1 to `c/2`. Slow but no misses. |
| `quit` | Exit the program. |

## Output files

| File | Content |
|------|---------|
| `abc_live_triples.txt` | All discovered triples with timestamp, quality, purity marker. |
| `abc_backup.txt` | Backup copy of the triples. |
| `abc_fertile_c.txt` | List of fertile `c` (multiple triples). |
| `abc_pure_triples.txt` | Triples flagged as pure (✨). |
| `abc_model.json` | Learned model (genetic primes, optimal radius, etc.). |

## License

MIT License – see `LICENSE` file.

## Author

**Andrey Drozdov** – [A395816](https://oeis.org/A395816)
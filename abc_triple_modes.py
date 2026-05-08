#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ABC-МЕГА-АЛГОРИТМ: run (обычный), fast (только малые a), full (полный перебор a)
"""

import math, time, os, sys, gc, json, threading, random, pickle
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

print("=" * 100)
print("🔥 ABC-ТРИ РЕЖИМА: run | fast | full 🔥")
print("=" * 100)

# ==================== КЭШ РАДИКАЛОВ ====================
RAD_CACHE_FILE = "radical_cache_ultimate.pkl"
rad_cache = {}

def get_rad(n):
    if n in rad_cache:
        return rad_cache[n]
    original = n
    res = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            res *= d
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        res *= n
    rad_cache[original] = res
    return res

def load_rad_cache():
    global rad_cache
    if os.path.exists(RAD_CACHE_FILE):
        try:
            with open(RAD_CACHE_FILE, 'rb') as f:
                rad_cache = pickle.load(f)
            print(f"Кэш радикалов загружен ({len(rad_cache)} чисел)")
        except:
            print("Ошибка загрузки кэша")

def save_rad_cache():
    with open(RAD_CACHE_FILE, 'wb') as f:
        pickle.dump(rad_cache, f)
    print(f"Кэш радикалов сохранён ({len(rad_cache)} чисел)")

# ==================== КЛАСС КОНФИГУРАЦИИ ====================
class Config:
    LIMIT_C = 250_000_000
    LIMIT_SMOOTH = 50_000_000
    MIN_QUALITY = 1.20
    NUM_WORKERS = os.cpu_count() or 8
    PREDICTION_RADIUS = 5000
    ELLIPSE_RADIUS = 5000
    THRESHOLD = 0.45
    E = math.e
    
    BILLIARD_STEPS = 50_000
    SUPERPOSITION_Q_MAX = 100
    METHOD_B_STEP = 50
    
    SMALL_A_LIST = [1, 2, 3, 5, 7, 11, 13]  # для режима fast
    
    # Параметры для режима full
    FULL_MAX_C = 10_000_000
    FULL_GENETIC_PRIMES = [2, 3, 5, 7, 11, 13]
    
    LIVE_FILE = "abc_live_triples.txt"
    BACKUP_FILE = "abc_backup.txt"
    MODEL_FILE = "abc_model.json"
    CONFIG_FILE = "abc_config.json"
    FERTILE_FILE = "abc_fertile_c.txt"
    PURE_FILE = "abc_pure_triples.txt"
    
    GENETIC_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    ACTIVE_SUPER = ['A', 'B', 'C', 'D']
    
    SUPER_STATS = {
        'A': {'name': 'Генетический резонанс', 'found': 0, 'time': 0.0},
        'B': {'name': 'Геометрический детектор', 'found': 0, 'time': 0.0},
        'C': {'name': 'Квантово-хаотический', 'found': 0, 'time': 0.0},
        'D': {'name': 'Точный перебор a', 'found': 0, 'time': 0.0},
    }
    
    METHODS_STATS = {}
    for m, n in {
        1:"Деформация p³/q", 2:"Теория чистоты Φ", 3:"Цепные дроби",
        4:"Резонансная C", 5:"Парабола", 6:"Эллипс",
        7:"Гладкие числа", 8:"Отбор c", 9:"Логарифмические формы",
        10:"Комплексная деформация", 11:"Малые a", 12:"Генетический",
        13:"Пересечение", 14:"Решето", 15:"Бильярд", 16:"Квантовая суперпозиция",
        17:"Точный перебор a"
    }.items():
        METHODS_STATS[m] = {"name": n, "found": 0}
    
    fertile_c = defaultdict(list)
    pure_triples = []
    
    model = {
        'genetic_primes': GENETIC_PRIMES.copy(),
        'prime_weights': {},
        'optimal_radius': PREDICTION_RADIUS,
        'hot_zones': [],
        'learned_patterns': []
    }
    
    @classmethod
    def show(cls):
        print(f"\n📊 ТЕКУЩИЕ НАСТРОЙКИ")
        print("=" * 60)
        print(f"   LIMIT_C = {cls.LIMIT_C:,}")
        print(f"   LIMIT_SMOOTH = {cls.LIMIT_SMOOTH:,}")
        print(f"   MIN_QUALITY = {cls.MIN_QUALITY}")
        print(f"   THRESHOLD = {cls.THRESHOLD}")
        print(f"   NUM_WORKERS = {cls.NUM_WORKERS}")
        print(f"\n🧬 Режим fast: SMALL_A_LIST = {cls.SMALL_A_LIST}")
        print(f"📌 Режим full: FULL_MAX_C = {cls.FULL_MAX_C:,}, FULL_GENETIC_PRIMES = {cls.FULL_GENETIC_PRIMES}")
        print("=" * 60)
    
    @classmethod
    def save_config(cls):
        cfg = {
            'limit_c': cls.LIMIT_C, 'limit_smooth': cls.LIMIT_SMOOTH,
            'min_quality': cls.MIN_QUALITY, 'threshold': cls.THRESHOLD,
            'num_workers': cls.NUM_WORKERS,
            'active_super': cls.ACTIVE_SUPER, 'small_a_list': cls.SMALL_A_LIST,
            'full_max_c': cls.FULL_MAX_C, 'full_genetic_primes': cls.FULL_GENETIC_PRIMES
        }
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(cfg, f, indent=2)
    
    @classmethod
    def load_config(cls):
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    cfg = json.load(f)
                    cls.LIMIT_C = cfg.get('limit_c', cls.LIMIT_C)
                    cls.LIMIT_SMOOTH = cfg.get('limit_smooth', cls.LIMIT_SMOOTH)
                    cls.MIN_QUALITY = cfg.get('min_quality', cls.MIN_QUALITY)
                    cls.THRESHOLD = cfg.get('threshold', cls.THRESHOLD)
                    cls.NUM_WORKERS = cfg.get('num_workers', cls.NUM_WORKERS)
                    cls.ACTIVE_SUPER = cfg.get('active_super', cls.ACTIVE_SUPER)
                    cls.SMALL_A_LIST = cfg.get('small_a_list', cls.SMALL_A_LIST)
                    cls.FULL_MAX_C = cfg.get('full_max_c', cls.FULL_MAX_C)
                    cls.FULL_GENETIC_PRIMES = cfg.get('full_genetic_primes', cls.FULL_GENETIC_PRIMES)
            except: pass
    
    @classmethod
    def save_model(cls):
        with open(cls.MODEL_FILE, 'w') as f:
            json.dump(cls.model, f, indent=2)
    
    @classmethod
    def load_model(cls):
        if os.path.exists(cls.MODEL_FILE):
            try:
                with open(cls.MODEL_FILE, 'r') as f:
                    loaded = json.load(f)
                    cls.model.update(loaded)
                    cls.GENETIC_PRIMES = cls.model.get('genetic_primes', cls.GENETIC_PRIMES)
                    cls.PREDICTION_RADIUS = cls.model.get('optimal_radius', cls.PREDICTION_RADIUS)
            except: pass

# Глобальные данные для обычного режима
smooth_list = []
candidates = []
KNOWN = set()
_saved_triples_set = set()
_save_buffer = []
_save_lock = threading.Lock()

def save_triple(prefix, r):
    global _saved_triples_set
    a, b, c, q, rad_abc, known, pure = r
    key = (a, b, c)
    if key in _saved_triples_set:
        return
    _saved_triples_set.add(key)
    
    Config.fertile_c[c].append((a, b, q))
    if pure:
        Config.pure_triples.append(r)
    
    star = "⭐" if not known else " "
    pure_mark = "✨" if pure else " "
    line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | [{prefix}] {a}+{b}={c} | q={q:.10f} | rad={rad_abc} | {star}{pure_mark}\n"
    print(f"\n🎯 [{prefix}] {a}+{b}={c} | q={q:.6f} | {star}{pure_mark}")
    
    with _save_lock:
        _save_buffer.append(line)
        if len(_save_buffer) >= 50:
            with open(Config.LIVE_FILE, 'a', encoding='utf-8') as f:
                f.writelines(_save_buffer)
                f.flush()
            with open(Config.BACKUP_FILE, 'a', encoding='utf-8') as f:
                f.writelines(_save_buffer)
                f.flush()
            _save_buffer.clear()

def get_quality(a, b, c):
    ra = get_rad(a)
    rb = get_rad(b)
    rc = get_rad(c)
    r = ra * rb * rc
    if r >= c or r == 0:
        return 0.0, r
    return math.log(c) / math.log(r), r

def purity_test(a, b, c, rad_abc):
    if a <= 0 or rad_abc == 0:
        return False
    try:
        exp_val = Config.E * b * c / rad_abc
        log_phi = exp_val * math.log(a)
        frac = log_phi - math.floor(log_phi)
        return min(frac, 1 - frac) < 1e-7
    except:
        return False

def check_triple(a, b, c):
    if a >= b or a + b != c: return None
    if math.gcd(a, b) != 1: return None
    if math.gcd(a, c) != 1 or math.gcd(b, c) != 1: return None
    q, r_abc = get_quality(a, b, c)
    if q < Config.MIN_QUALITY: return None
    known = tuple(sorted((a, b, c))) in KNOWN
    pure = purity_test(a, b, c, r_abc)
    Config.METHODS_STATS[2]['found'] += 1
    return (a, b, c, q, r_abc, known, pure)

def try_triple(a, b, c, method_id=0):
    if a >= Config.LIMIT_C or b >= Config.LIMIT_C or c >= Config.LIMIT_C:
        return None
    if a >= b or a + b != c: return None
    if (a & 1) == 0 and (b & 1) == 0: return None
    if math.gcd(a, b) != 1: return None
    if method_id and method_id in Config.METHODS_STATS:
        Config.METHODS_STATS[method_id]['found'] += 1
    return check_triple(a, b, c)

# === Обычные функции для run ===
def generate_smooth():
    global smooth_list
    primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,
              73,79,83,89,97,101,103,107,109,113,127,131,137,139,149]
    s = {1}
    lim = min(Config.LIMIT_SMOOTH, Config.LIMIT_C)
    for p in primes:
        new_entries = set()
        for x in s:
            cur = x * p
            while cur <= lim:
                new_entries.add(cur)
                cur *= p
        s.update(new_entries)
        if len(s) > 8_000_000:
            s = set(list(s)[:6_000_000])
            gc.collect()
    smooth_list = sorted(s)[1:]
    print(f"Гладких чисел: {len(smooth_list):,}")

def load_known_triples():
    global KNOWN
    KNOWN = set()
    for n in range(2, 60):
        try:
            c = 2 ** n
            if c <= Config.LIMIT_C:
                KNOWN.add(tuple(sorted((1, c - 1, c))))
        except:
            pass

def select_candidates():
    global candidates
    cand = []
    lim = min(Config.LIMIT_SMOOTH, Config.LIMIT_C)
    for c in smooth_list:
        if 100 < c <= lim and get_rad(c) < c ** Config.THRESHOLD:
            cand.append(c)
    candidates = sorted(set(cand))
    print(f"✅ Кандидатов: {len(candidates):,}")

# === Обычные супер-методы (A, B, C, D) без изменений ===
def method_A_search():
    results = []
    genetic_primes = Config.GENETIC_PRIMES[:30]
    q_values = list(range(2, 101))
    exponents = list(range(2, 11))
    
    print(f"   A: Генетический перебор...")
    for p in genetic_primes:
        for q in q_values:
            if q >= p and p > 13:
                continue
            for exp in exponents:
                try:
                    c = p ** exp
                except OverflowError:
                    continue
                if c > Config.LIMIT_C or c <= 0:
                    continue
                a = c // q
                if a > 0 and a < c:
                    b = c - a
                    if a > b:
                        a, b = b, a
                    r = try_triple(a, b, c, method_id=12)
                    if r:
                        results.append(r)
                        save_triple("A", r)
    
    print(f"   A: Перебор {len(candidates):,} кандидатов...")
    for i, c in enumerate(candidates):
        if i % 10000 == 0 and i > 0:
            print(f"   A: обработано {i}/{len(candidates)}...")
        r = try_triple(1, c-1, c, method_id=11)
        if r:
            results.append(r)
            save_triple("A", r)
        for a in [1,2,3,5,7,11,13,17,19,23]:
            if a >= c:
                break
            r = try_triple(a, c-a, c, method_id=11)
            if r:
                results.append(r)
                save_triple("A", r)
    return results

def method_B_fast(c, rad_c):
    results = []
    center = c // 2
    step = Config.METHOD_B_STEP
    
    for da in range(-Config.PREDICTION_RADIUS, Config.PREDICTION_RADIUS + 1, step):
        a = center + da
        if a <= 1 or a >= c:
            continue
        b = c - a
        if b <= a:
            continue
        r = try_triple(a, b, c, method_id=5)
        if r:
            results.append(r)
            save_triple("B", r)
    
    if rad_c < c ** 0.4:
        try:
            offset = int(math.log(rad_c) / math.log(c) * 1000) if rad_c > 1 else 0
        except:
            offset = 0
        ell_center = max(1, min(c - 1, center + offset))
        for da in range(-Config.ELLIPSE_RADIUS // 2, Config.ELLIPSE_RADIUS // 2 + 1, step):
            a = ell_center + da
            if a <= 1 or a >= c:
                continue
            b = c - a
            if b <= a:
                continue
            r = try_triple(a, b, c, method_id=6)
            if r:
                results.append(r)
                save_triple("B", r)
    return results

class ChaoticBilliard:
    def __init__(self, a_min, a_max):
        self.a_min = a_min
        self.a_max = a_max
        self.pos = random.randint(a_min, a_max)
        self.vel = random.choice([-1, 1])
    def next(self):
        step = random.randint(10, 50)
        new_pos = self.pos + self.vel * step
        if new_pos < self.a_min:
            new_pos = self.a_min + (self.a_min - new_pos)
            self.vel = -self.vel
        if new_pos > self.a_max:
            new_pos = self.a_max - (new_pos - self.a_max)
            self.vel = -self.vel
        self.pos = max(self.a_min, min(self.a_max, new_pos))
        return int(self.pos)

def method_C_fast(c, rad_c):
    results = []
    max_a = c // 2
    
    billiard = ChaoticBilliard(1, max_a)
    for _ in range(Config.BILLIARD_STEPS):
        a = billiard.next()
        b = c - a
        if b <= a:
            continue
        r = try_triple(a, b, c, method_id=15)
        if r:
            results.append(r)
            save_triple("C", r)
    
    for p in [2,3,5,7,11,13,17,19]:
        for exp in range(2, 8):
            try:
                c_cand = p ** exp
            except OverflowError:
                continue
            if c_cand > Config.LIMIT_C:
                continue
            if abs(c_cand - c) < 50000:
                for q in range(2, Config.SUPERPOSITION_Q_MAX):
                    a = c_cand // q
                    if a == 0:
                        continue
                    b = c_cand - a
                    if a > b:
                        a, b = b, a
                    r = try_triple(a, b, c_cand, method_id=16)
                    if r:
                        results.append(r)
                        save_triple("C", r)
    return results

def method_D_search():
    results = []
    a_list = Config.SMALL_A_LIST
    print(f"   D: Точный перебор a = {a_list} для всех {len(candidates):,} кандидатов c...")
    for i, c in enumerate(candidates):
        if i % 10000 == 0 and i > 0:
            print(f"   D: обработано {i}/{len(candidates)}...")
        for a in a_list:
            if a >= c:
                continue
            b = c - a
            if b <= a:
                continue
            if (a & 1) == 0 and (b & 1) == 0:
                continue
            if math.gcd(a, b) != 1:
                continue
            r = try_triple(a, b, c, method_id=17)
            if r:
                results.append(r)
                save_triple("D", r)
    return results

# === НОВЫЙ РЕЖИМ FAST (только метод A с малыми a) ===
def fast_mode():
    """Режим fast: только метод A, a из фиксированного списка, c - кандидаты из гладких чисел."""
    print("\n⚡ РЕЖИМ FAST (малые a, без степеней)")
    print(f"   LIMIT_C = {Config.LIMIT_C:,}")
    print(f"   Малые a = {Config.SMALL_A_LIST}")
    
    # Готовим кандидатов c
    generate_smooth()
    load_known_triples()
    select_candidates()
    
    Config.fertile_c.clear()
    Config.pure_triples.clear()
    global _saved_triples_set
    _saved_triples_set.clear()
    
    with open(Config.LIVE_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n=== РЕЖИМ FAST {datetime.now()} ===\n")
    
    total = 0
    start = time.time()
    
    # Перебираем всех кандидатов c, для каждого проверяем только малые a
    for i, c in enumerate(candidates):
        if i % 10000 == 0 and i > 0:
            print(f"   Обработано {i}/{len(candidates)} c, найдено {total} троек")
        
        for a in Config.SMALL_A_LIST:
            if a >= c:
                continue
            b = c - a
            if b <= a:
                continue
            if (a & 1) == 0 and (b & 1) == 0:
                continue
            if math.gcd(a, b) != 1:
                continue
            r = try_triple(a, b, c, method_id=11)  # 11 = малые a
            if r:
                save_triple("FAST", r)
                total += 1
    
    elapsed = time.time() - start
    print(f"\n✅ РЕЖИМ FAST завершён. Найдено {total} троек за {elapsed:.2f} сек.")
    print(f"   Результаты в {Config.LIVE_FILE}")

# === РЕЖИМ FULL (полный перебор всех a для c из степеней) ===
def full_generate_c(limit, primes):
    cset = set()
    # степени
    for p in primes:
        v = p
        for e in range(2, 25):
            v *= p
            if v > limit:
                break
            cset.add(v)
    # произведения
    g = primes[:15]
    for i, p1 in enumerate(g):
        for p2 in g[i:]:
            for e1 in range(2, 12):
                v1 = p1 ** e1
                if v1 > limit: break
                for e2 in range(2, 12):
                    v2 = p2 ** e2
                    if v2 > limit: break
                    prod = v1 * v2
                    if prod <= limit:
                        cset.add(prod)
    # суммы/разности
    for p1 in g:
        for p2 in g:
            for e1 in range(1, 20):
                v1 = p1 ** e1
                if v1 > limit: break
                for e2 in range(1, 20):
                    v2 = p2 ** e2
                    if v2 > limit: break
                    s = v1 + v2
                    if s <= limit:
                        cset.add(s)
                    d = abs(v1 - v2)
                    if 0 < d <= limit:
                        cset.add(d)
    return sorted(cset)

def full_mode():
    """Режим full: полный перебор всех a для c из степеней простых."""
    print("\n🔍 РЕЖИМ FULL (полный перебор всех a для c из степеней)")
    print(f"   FULL_MAX_C = {Config.FULL_MAX_C:,}")
    print(f"   Генетические простые = {Config.FULL_GENETIC_PRIMES}")
    print("   ⚠️  ВНИМАНИЕ: полный перебор a для каждого c может быть очень медленным!")
    
    if Config.FULL_MAX_C > 100_000_000:
        print("   ⚠️  FULL_MAX_C > 100 млн. Это займёт часы или дни. Продолжить? (y/n)")
        if input().strip().lower() != 'y':
            return
    
    c_list = full_generate_c(Config.FULL_MAX_C, Config.FULL_GENETIC_PRIMES)
    print(f"   Сгенерировано c: {len(c_list):,}")
    
    Config.fertile_c.clear()
    Config.pure_triples.clear()
    global _saved_triples_set
    _saved_triples_set.clear()
    
    with open(Config.LIVE_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n=== РЕЖИМ FULL {datetime.now()} ===\n")
    
    total = 0
    start = time.time()
    
    for idx, c in enumerate(c_list):
        if idx % 1000 == 0:
            print(f"   Обработано {idx}/{len(c_list)} c, найдено {total} троек")
        max_a = c // 2
        # Полный перебор a от 1 до max_a (можно ускорить, пропуская чётные пары)
        for a in range(1, max_a + 1):
            b = c - a
            if b <= a:
                continue
            if (a & 1) == 0 and (b & 1) == 0:
                continue
            if math.gcd(a, b) != 1:
                continue
            q, _ = get_quality(a, b, c)
            if q < Config.MIN_QUALITY:
                continue
            r = check_triple(a, b, c)
            if r:
                save_triple("FULL", r)
                total += 1
    
    elapsed = time.time() - start
    print(f"\n✅ РЕЖИМ FULL завершён. Найдено {total} троек за {elapsed:.2f} сек.")
    print(f"   Результаты в {Config.LIVE_FILE}")

# === ОБЫЧНЫЙ РЕЖИМ RUN (без изменений) ===
def run_search():
    global _saved_triples_set
    search_start = time.time()
    _saved_triples_set.clear()
    Config.fertile_c.clear()
    Config.pure_triples.clear()
    
    with open(Config.LIVE_FILE, 'w', encoding='utf-8') as f:
        f.write(f"ABC-тройки (quality >= {Config.MIN_QUALITY})\n")
        f.write(f"Запуск: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
    
    for k in Config.SUPER_STATS:
        Config.SUPER_STATS[k]['found'] = 0
        Config.SUPER_STATS[k]['time'] = 0.0
    for m in Config.METHODS_STATS:
        Config.METHODS_STATS[m]['found'] = 0
    
    generate_smooth()
    load_known_triples()
    select_candidates()
    
    all_triples = []
    found_set = set()
    lock = threading.Lock()
    
    print(f"\n🚀 ЗАПУСК ОБЫЧНОГО ПОИСКА (run)")
    print(f"   Кандидатов: {len(candidates):,}")
    print(f"   Активные: {Config.ACTIVE_SUPER}\n")
    
    # Метод A
    if 'A' in Config.ACTIVE_SUPER:
        print("🔬 Супер-метод A...")
        t0 = time.time()
        a_results = method_A_search()
        Config.SUPER_STATS['A']['time'] = time.time() - t0
        Config.SUPER_STATS['A']['found'] = len(a_results)
        with lock:
            for r in a_results:
                if r[:3] not in found_set:
                    found_set.add(r[:3])
                    all_triples.append(r)
        print(f"   ✅ {len(a_results)} троек за {Config.SUPER_STATS['A']['time']:.2f}с")
    
    # Метод B
    if 'B' in Config.ACTIVE_SUPER:
        print("\n🔬 Супер-метод B...")
        t0 = time.time()
        b_count = 0
        def is_good_c(c):
            temp = c
            for p in Config.GENETIC_PRIMES[:7]:
                while temp % p == 0:
                    temp //= p
            return temp == 1
        with ThreadPoolExecutor(max_workers=Config.NUM_WORKERS) as executor:
            futures = {}
            for c in candidates:
                rad_c = get_rad(c)
                if is_good_c(c) and rad_c * rad_c < c * 2:
                    futures[executor.submit(lambda x: (x, method_B_fast(x, rad_c)), c)] = c
            for future in as_completed(futures):
                try:
                    b_results = future.result()[1]
                    b_count += len(b_results)
                    with lock:
                        for r in b_results:
                            if r[:3] not in found_set:
                                found_set.add(r[:3])
                                all_triples.append(r)
                except: pass
        Config.SUPER_STATS['B']['time'] = time.time() - t0
        Config.SUPER_STATS['B']['found'] = b_count
        print(f"   ✅ {b_count} троек за {Config.SUPER_STATS['B']['time']:.2f}с")
    
    # Метод C
    if 'C' in Config.ACTIVE_SUPER:
        print("\n🔬 Супер-метод C...")
        t0 = time.time()
        c_count = 0
        with ThreadPoolExecutor(max_workers=Config.NUM_WORKERS) as executor:
            futures = {}
            for c in candidates[:10000]:
                rad_c = get_rad(c)
                if rad_c * rad_c < c * 2:
                    futures[executor.submit(lambda x: (x, method_C_fast(x, rad_c)), c)] = c
            for future in as_completed(futures):
                try:
                    c_results = future.result()[1]
                    c_count += len(c_results)
                    with lock:
                        for r in c_results:
                            if r[:3] not in found_set:
                                found_set.add(r[:3])
                                all_triples.append(r)
                except: pass
        Config.SUPER_STATS['C']['time'] = time.time() - t0
        Config.SUPER_STATS['C']['found'] = c_count
        print(f"   ✅ {c_count} троек за {Config.SUPER_STATS['C']['time']:.2f}с")
    
    # Метод D
    if 'D' in Config.ACTIVE_SUPER:
        print("\n🔬 Супер-метод D...")
        t0 = time.time()
        d_results = method_D_search()
        Config.SUPER_STATS['D']['time'] = time.time() - t0
        Config.SUPER_STATS['D']['found'] = len(d_results)
        with lock:
            for r in d_results:
                if r[:3] not in found_set:
                    found_set.add(r[:3])
                    all_triples.append(r)
        print(f"   ✅ {len(d_results)} троек за {Config.SUPER_STATS['D']['time']:.2f}с")
    
    search_time = time.time() - search_start
    
    # Самообучение
    if all_triples:
        print("\n🧠 САМООБУЧЕНИЕ")
        prime_counter = Counter()
        for r in all_triples:
            a,b,c,q,_,_,_ = r
            weight = max(0.1, q - Config.MIN_QUALITY + 0.5)
            for val in (a,b,c):
                tmp = val
                for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]:
                    if tmp % p == 0:
                        prime_counter[p] += weight
                        while tmp % p == 0: tmp //= p
        if prime_counter:
            top_primes = [p for p,_ in prime_counter.most_common(15)]
            Config.GENETIC_PRIMES = top_primes
            Config.model['genetic_primes'] = top_primes
            print(f"   ✅ Новый генетический код: {top_primes[:10]}...")
        
        a_counter = Counter()
        for r in all_triples:
            a = r[0]
            if a <= 2000:
                a_counter[a] += 1
        new_a = [a for a,cnt in a_counter.most_common(30) if a not in Config.SMALL_A_LIST]
        if new_a:
            Config.SMALL_A_LIST.extend(new_a)
            Config.SMALL_A_LIST = sorted(set(Config.SMALL_A_LIST))[:100]
            Config.model['small_a_list'] = Config.SMALL_A_LIST
            print(f"   ✅ Добавлено малых a: {new_a[:10]}...")
        
        distances = [abs(r[0] - r[2]//2) for r in all_triples]
        if distances:
            distances.sort()
            p95 = distances[int(len(distances)*0.95)]
            new_radius = max(3000, min(20000, p95+500))
            Config.PREDICTION_RADIUS = new_radius
            Config.model['optimal_radius'] = new_radius
            print(f"   ✅ Оптимальный радиус: {new_radius}")
        Config.save_model()
    
    with open(Config.FERTILE_FILE, 'w', encoding='utf-8') as f:
        for c, pairs in sorted(Config.fertile_c.items()):
            if len(set(pairs)) >= 2:
                f.write(f"{c}: {len(set(pairs))} троек\n")
    with open(Config.PURE_FILE, 'w', encoding='utf-8') as f:
        for r in Config.pure_triples:
            a,b,c,q,ra,_,_ = r
            f.write(f"{a} + {b} = {c} | q={q:.10f} | rad={ra}\n")
    
    fertile_count = sum(1 for pairs in Config.fertile_c.values() if len(set(pairs)) >= 2)
    
    print(f"\n📊 ФИНАЛЬНЫЙ ОТЧЁТ (run)")
    print(f"   Время: {search_time:.2f} сек ({search_time/60:.2f} мин)")
    print(f"   Найдено троек: {len(all_triples)}")
    print(f"   Чистых: {len(Config.pure_triples)}")
    print(f"   Плодородных c: {fertile_count}")
    print(f"\n⏱️ ТАЙМИНГ СУПЕР-МЕТОДОВ:")
    for k,v in Config.SUPER_STATS.items():
        if k in Config.ACTIVE_SUPER:
            print(f"   {k}: {v['name']:25} -> {v['found']:3} троек, {v['time']:.2f}с")
    print(f"\n💾 Результаты: {Config.LIVE_FILE}")

# === ИНТЕРАКТИВНОЕ МЕНЮ ===
def interactive():
    print("\n📟 МЕНЮ КОМАНД")
    print("="*70)
    print("  run        - обычный поиск (все супер-методы, самообучение)")
    print("  fast       - быстрый поиск: только малые a из списка, кандидаты c")
    print("  full       - полный перебор всех a для c из степеней (медленно, точно)")
    print("")
    print("  ПАРАМЕТРЫ:")
    print("    show                        - показать настройки")
    print("    set limit <число>           - LIMIT_C (для run и fast)")
    print("    set smooth <число>          - LIMIT_SMOOTH")
    print("    set quality <число>         - MIN_QUALITY")
    print("    set threshold <число>       - THRESHOLD (отбор c)")
    print("    set workers <число>         - NUM_WORKERS")
    print("    set small \"1,2,3,5,7\"     - список a для fast")
    print("    set full_max_c <число>      - макс. c для full")
    print("    set full_genetic \"2,3,5\"   - простые для full")
    print("")
    print("  УПРАВЛЕНИЕ СУПЕР-МЕТОДАМИ (для run):")
    print("    super A / B / C / D         - включить/выключить")
    print("")
    print("  СТАТИСТИКА:")
    print("    methods, fertile, pure, optimize")
    print("")
    print("  ДРУГОЕ:")
    print("    save, quit")
    print("="*70)
    
    while True:
        cmd = input("\n> ").strip().lower()
        if cmd == 'quit' or cmd == 'exit':
            break
        elif cmd == 'run':
            run_search()
        elif cmd == 'fast':
            fast_mode()
        elif cmd == 'full':
            full_mode()
        elif cmd == 'show':
            Config.show()
        elif cmd.startswith('set small'):
            parts = cmd.split('"')
            if len(parts) >= 2:
                try:
                    Config.SMALL_A_LIST = [int(x.strip()) for x in parts[1].split(',')]
                    print(f"✅ Список a для fast: {Config.SMALL_A_LIST}")
                except: print("Ошибка")
            else: print("Формат: set small \"1,2,3\"")
        elif cmd.startswith('set full_max_c'):
            parts = cmd.split()
            if len(parts) == 3:
                try:
                    Config.FULL_MAX_C = int(parts[2])
                    print(f"✅ FULL_MAX_C = {Config.FULL_MAX_C:,}")
                except: print("Ошибка")
            else: print("Формат: set full_max_c 10000000")
        elif cmd.startswith('set full_genetic'):
            parts = cmd.split('"')
            if len(parts) >= 2:
                try:
                    Config.FULL_GENETIC_PRIMES = [int(x.strip()) for x in parts[1].split(',')]
                    print(f"✅ FULL_GENETIC_PRIMES = {Config.FULL_GENETIC_PRIMES}")
                except: print("Ошибка")
            else: print("Формат: set full_genetic \"2,3,5\"")
        elif cmd.startswith('set '):
            parts = cmd.split()
            if len(parts) == 3:
                param, val = parts[1], parts[2]
                try:
                    if '.' in val: val = float(val)
                    else: val = int(val)
                    if param == 'limit': Config.LIMIT_C = val
                    elif param == 'smooth': Config.LIMIT_SMOOTH = int(val)
                    elif param == 'quality': Config.MIN_QUALITY = val
                    elif param == 'threshold': Config.THRESHOLD = val
                    elif param == 'workers': Config.NUM_WORKERS = int(val)
                    else: print("Неизвестный параметр"); continue
                    print(f"✅ {param} = {val}")
                except: print("Ошибка")
            else: print("Формат: set параметр значение")
        elif cmd.startswith('super '):
            parts = cmd.split()
            if len(parts) == 2:
                s = parts[1].upper()
                if s in Config.ACTIVE_SUPER:
                    Config.ACTIVE_SUPER.remove(s)
                    print(f"✅ {s} выключен")
                else:
                    Config.ACTIVE_SUPER.append(s)
                    Config.ACTIVE_SUPER.sort()
                    print(f"✅ {s} включён")
        elif cmd == 'methods':
            print("\n📊 СТАТИСТИКА МЕТОДОВ (1-17):")
            for m in sorted(Config.METHODS_STATS.keys()):
                if Config.METHODS_STATS[m]['found'] > 0:
                    print(f"   {m:2}: {Config.METHODS_STATS[m]['name']:25} -> {Config.METHODS_STATS[m]['found']:3}")
        elif cmd == 'fertile':
            if Config.fertile_c:
                print("\n🌱 ПЛОДОРОДНЫЕ C:")
                for c, pairs in sorted(Config.fertile_c.items()):
                    unique = set(pairs)
                    if len(unique) >= 2:
                        print(f"   c={c} ({len(unique)} троек):", *[f"{a}+{b}={c}" for a,b,q in unique])
            else: print("Нет плодородных c")
        elif cmd == 'pure':
            if Config.pure_triples:
                print("\n✨ ЧИСТЫЕ ТРОЙКИ:")
                for r in Config.pure_triples[:20]:
                    a,b,c,q,_,_,_ = r
                    print(f"   {a}+{b}={c}  q={q:.6f}")
            else: print("Нет чистых троек")
        elif cmd == 'optimize':
            to_del = [s for s in ['A','B','C','D'] if s in Config.ACTIVE_SUPER and Config.SUPER_STATS[s]['found']==0]
            if to_del:
                for s in to_del: Config.ACTIVE_SUPER.remove(s)
                print(f"Отключены: {to_del}")
            else: print("Нечего отключать")
        elif cmd == 'save':
            Config.save_config()
            Config.save_model()
            save_rad_cache()
            print("Сохранено")
        else:
            print("Неизвестная команда")

if __name__ == "__main__":
    load_rad_cache()
    Config.load_config()
    Config.load_model()
    interactive()

# Analysis: Data Structures, Algorithms & Complexity

## Data Structure Mapping

| Feature | Data Structure | Time Complexity | Space Complexity | Rationale |
|---------|---------------|-----------------|------------------|-----------|
| Request storage & lookup by ID | Dictionary (`dict`) | O(1) avg | O(n) | Direct key-value access; ideal for unique ID lookups |
| Duplicate ID prevention | Set (`set`) | O(1) avg | O(n) | Constant-time membership test; prevents collisions |
| Request processing order | Queue (`deque`) | O(1) popleft/append | O(n) | FIFO semantics; `deque` optimized for both ends |
| Undo last change | Stack (`list`) | O(1) append/pop | O(n) | LIFO semantics; `list.append/pop()` are O(1) |
| Search by ID | Dictionary lookup | O(1) avg | O(1) | Direct hash table access |
| Search by name | Linear scan | O(n) | O(k) results | No index on name; must check all values |
| Sort by date/priority/status | Built-in `sorted()` (Timsort) | O(n log n) | O(n) | Highly optimized, stable, adaptive |
| Manual sort (comparison) | Insertion sort | O(n²) | O(1) extra | Simple implementation for educational comparison |
| Reply display | Recursion | O(n) | O(n) stack | Natural for sequential/threaded display |

---

## Search Comparison

### `search_by_id` — Dictionary Lookup
```python
def search_by_id(system, request_id):
    return system.requests.get(request_id)
```
- **Time**: O(1) average case (hash table)
- **Space**: O(1)
- **Best for**: Exact-match lookups by unique key
- **Trade-off**: Requires maintaining the dictionary; only works for ID

### `search_by_name` — Linear Scan
```python
def search_by_name(system, name):
    matches = []
    for request in system.requests.values():
        if request.customer_name.lower() == name.lower():
            matches.append(request)
    return matches
```
- **Time**: O(n) where n = total requests
- **Space**: O(k) where k = matching requests
- **Best for**: Non-unique fields, partial/fuzzy matching
- **Trade-off**: Scans entire dataset; slow for large n

**Comparison**: Dictionary lookup is ~1000x faster at n=10,000. Linear scan is simpler but doesn't scale. In production, add a secondary index (name → list of IDs) for O(1) name search.

---

## Sort Comparison

### Built-in `sorted()` — Timsort
```python
def sort_requests(system, by="date"):
    requests = list(system.requests.values())
    if by == "date":
        return sorted(requests, key=lambda r: r.date_received)
    # ... priority, status
```
- **Time**: O(n log n) worst/average; O(n) best (already sorted)
- **Space**: O(n) for output list
- **Properties**: Stable, adaptive, highly optimized in C

### Manual Insertion Sort
```python
def insertion_sort_requests(system, by="date"):
    requests = list(system.requests.values())
    for i in range(1, len(requests)):
        current = requests[i]
        j = i - 1
        while j >= 0 and key_func(requests[j]) > key_func(current):
            requests[j + 1] = requests[j]
            j -= 1
        requests[j + 1] = current
    return requests
```
- **Time**: O(n²) worst/average; O(n) best (already sorted)
- **Space**: O(1) extra (in-place on list copy)
- **Properties**: Stable, simple, good for small n or nearly-sorted data

**Comparison**: At n=100, Timsort ~100x faster. At n=1000, ~1000x faster. Insertion sort only competitive for n < ~50 or nearly-sorted data. Both produce identical results (verified in tests).

---

## Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| Add request | O(1) | O(1) |
| Check duplicate | O(1) | O(1) |
| Process next (queue) | O(1) | O(1) |
| Mark urgent | O(1) | O(1) |
| Undo | O(1) | O(1) |
| Search by ID | O(1) | O(1) |
| Search by name | O(n) | O(k) |
| Sort (built-in) | O(n log n) | O(n) |
| Sort (insertion) | O(n²) | O(1) |
| Display replies | O(n) | O(n) |

---

## Limitations & Improvements

### Current Limitations
1. **No persistence** — Data lost on program exit; no database/file storage
2. **Linear name search** — O(n) doesn't scale; needs secondary index for production
3. **No concurrency** — Not thread-safe; `deque`/`dict`/`list` need locks for multi-threaded use
4. **No request updates** — Only add, process, mark urgent, undo; no edit/delete
5. **No pagination** — All requests loaded in memory; problematic for large datasets
6. **No authentication/authorization** — Any code can access all requests
7. **Recursion depth limit** — `display_replies` hits Python recursion limit (~1000) for very long threads
8. **Fixed priority/status values** — No validation; typos create new categories

### Suggested Improvements
1. **Add SQLite/PostgreSQL persistence** with SQLAlchemy
2. **Secondary index**: `name_to_ids: dict[str, set[str]]` for O(1) name search
3. **Thread safety**: Add `threading.RLock` for all mutating operations
4. **Request modification**: `update_request(request_id, **fields)` with history tracking
5. **Pagination**: `list_requests(page, page_size)` with cursor-based iteration
6. **Input validation**: Enum for priority/status; Pydantic models
7. **Iterative reply display**: Replace recursion with loop to avoid stack overflow
8. **CLI/Web API**: Add `argparse` CLI or FastAPI endpoints
9. **Logging & metrics**: Structured logging for audit trail
10. **Tests**: Add property-based tests (Hypothesis), integration tests

---

## Complexity Analysis Notes

- **Dictionary/Set**: Average O(1) assumes good hash distribution; worst case O(n) with collisions
- **Deque**: `popleft()` and `append()` are O(1) unlike list `pop(0)` which is O(n)
- **Timsort**: Python's built-in sort is adaptive — runs at O(n) on already-sorted or reverse-sorted data
- **Recursion**: Each call adds a stack frame; Python default limit ~1000 frames. Use `sys.setrecursionlimit()` or iterative approach for deep trees.
- **Space**: Most operations are O(1) auxiliary; sorting requires O(n) output; recursion requires O(n) stack
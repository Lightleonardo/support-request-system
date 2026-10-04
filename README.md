# Support Request System

A Python customer support request system demonstrating core data structures and algorithms.

## Features

- **Dictionary** for O(1) request lookup by ID
- **Set** for preventing duplicate request IDs
- **Queue (deque)** for FIFO request processing
- **Stack** for undo functionality
- **Search** by ID (O(1)) and customer name (O(n))
- **Sort** by date, priority, status using built-in Timsort and manual insertion sort
- **Recursive** reply/follow-up display

## Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install package in development mode
pip install -e .

# Or run without installing (set PYTHONPATH)
PYTHONPATH=. python data/sample_requests.py
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_manager.py -v
python -m pytest tests/test_search.py -v
python -m pytest tests/test_sorting.py -v
python -m pytest tests/test_replies.py -v
```

## Running the Demo

```bash
# With package installed
python data/sample_requests.py

# Without installing (set PYTHONPATH)
PYTHONPATH=. python data/sample_requests.py
```

## Project Structure

```
support-request-system/
├── support_system/
│   ├── __init__.py
│   ├── models.py        # Request dataclass
│   ├── manager.py       # SupportSystem with queue, undo stack
│   ├── search.py        # search_by_id, search_by_name
│   ├── sorting.py       # sort_requests, insertion_sort_requests
│   └── replies.py       # Recursive reply display
├── data/
│   └── sample_requests.py  # Demo with realistic sample data
├── tests/
│   ├── test_manager.py
│   ├── test_search.py
│   ├── test_sorting.py
│   └── test_replies.py
├── ANALYSIS.md          # Data structure table, complexity analysis
├── pyproject.toml
└── README.md
```

## Usage Example

```python
from support_system.manager import SupportSystem
from support_system.models import Request
from support_system.search import search_by_id, search_by_name
from support_system.sorting import sort_requests
from support_system.replies import display_replies
from datetime import date

system = SupportSystem()

# Add requests
req = Request("REQ001", "Ada Obi", "ada@example.com", "Login issue", date.today())
system.add_request(req)

# Process in FIFO order
processed = system.process_next()

# Mark urgent
system.mark_urgent("REQ001")

# Undo last change
system.undo()

# Search
found = search_by_id(system, "REQ001")
results = search_by_name(system, "Ada Obi")

# Sort
sorted_by_date = sort_requests(system, by="date")
sorted_by_priority = sort_requests(system, by="priority")

# Display replies recursively
req.replies = ["Reply 1", "Reply 2", "Reply 3"]
for line in display_replies(req.replies):
    print(line)
```

## Data Structures Used

| Feature | Data Structure | Why |
|---------|---------------|-----|
| Request storage | Dictionary | O(1) lookup by ID |
| Duplicate prevention | Set | O(1) membership test |
| Request processing | Queue (deque) | FIFO order |
| Undo functionality | Stack (list) | LIFO for last change |
| Reply display | Recursion | Natural for nested/follow-up replies |

See [ANALYSIS.md](ANALYSIS.md) for detailed complexity analysis and comparison.
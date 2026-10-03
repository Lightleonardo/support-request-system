"""Sorting functions for the support request system."""

from support_system.models import Request


def sort_requests(system, by="date"):
    """
    Sort requests using Python's built-in sorted() (Timsort).
    Time complexity: O(n log n)
    Space complexity: O(n)
    """
    requests = list(system.requests.values())
    
    if by == "date":
        return sorted(requests, key=lambda r: r.date_received)
    elif by == "priority":
        # high > normal > low
        priority_order = {"high": 0, "normal": 1, "low": 2}
        return sorted(requests, key=lambda r: priority_order.get(r.priority, 1))
    elif by == "status":
        # open > processing > closed
        status_order = {"open": 0, "processing": 1, "closed": 2}
        return sorted(requests, key=lambda r: status_order.get(r.status, 0))
    else:
        raise ValueError(f"Unknown sort key: {by}")


def insertion_sort_requests(system, by="date"):
    """
    Manual insertion sort for comparison with built-in sorted().
    Time complexity: O(n^2)
    Space complexity: O(1) in-place, O(n) for the list copy
    """
    requests = list(system.requests.values())
    
    if by == "date":
        key_func = lambda r: r.date_received
    elif by == "priority":
        priority_order = {"high": 0, "normal": 1, "low": 2}
        key_func = lambda r: priority_order.get(r.priority, 1)
    elif by == "status":
        status_order = {"open": 0, "processing": 1, "closed": 2}
        key_func = lambda r: status_order.get(r.status, 0)
    else:
        raise ValueError(f"Unknown sort key: {by}")
    
    # Insertion sort
    for i in range(1, len(requests)):
        current = requests[i]
        current_key = key_func(current)
        j = i - 1
        while j >= 0 and key_func(requests[j]) > current_key:
            requests[j + 1] = requests[j]
            j -= 1
        requests[j + 1] = current
    
    return requests
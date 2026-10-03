"""Search functions for the support request system."""

from support_system.models import Request


def search_by_id(system, request_id):
    """
    Search for a request by ID using dictionary lookup.
    Time complexity: O(1)
    Space complexity: O(1)
    """
    return system.requests.get(request_id)


def search_by_name(system, name):
    """
    Search for requests by customer name using linear scan.
    Time complexity: O(n) where n = number of requests
    Space complexity: O(k) where k = number of matches
    """
    matches = []
    for request in system.requests.values():
        # Case-insensitive comparison for flexible name matching
        if request.customer_name.lower() == name.lower():
            matches.append(request)
    return matches
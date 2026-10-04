from collections import deque
from datetime import date


class SupportSystem:
    """Receives, organises, and processes customer support requests."""

    def __init__(self):
        self.requests = {}
        self.seen_ids = set()
        self.queue = deque()
        self.history = []

    def add_request(self, request):
        """Add a new request, rejecting duplicate IDs."""
        if request.request_id in self.seen_ids:
            raise ValueError("Request ID already exists")
        self.requests[request.request_id] = request
        self.seen_ids.add(request.request_id)
        self.queue.append(request.request_id)
        return request

    def process_next(self):
        """Process the oldest request in the queue (FIFO)."""
        if not self.queue:
            return None
        request_id = self.queue.popleft()
        request = self.requests.get(request_id)
        if request:
            old_status = request.status
            request.status = "processing"
            self.history.append(("status", request_id, old_status))
        return request

    def mark_urgent(self, request_id):
        """Mark a request as high priority."""
        request = self.requests.get(request_id)
        if request:
            old_priority = request.priority
            request.priority = "high"
            self.history.append(("priority", request_id, old_priority))
        return request

    def undo(self):
        """Undo the most recent change to a request."""
        if not self.history:
            return None
        field, request_id, old_value = self.history.pop()
        request = self.requests.get(request_id)
        if request:
            setattr(request, field, old_value)
        return (field, request_id, old_value)

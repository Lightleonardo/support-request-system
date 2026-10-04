"""Sample data to demonstrate the support request system."""

from support_system.manager import SupportSystem
from support_system.models import Request
from support_system.search import search_by_id, search_by_name
from support_system.sorting import sort_requests, insertion_sort_requests
from support_system.replies import display_replies, display_replies_indented
from datetime import date, timedelta


def create_sample_system():
    """Create a SupportSystem populated with realistic sample requests."""
    system = SupportSystem()
    today = date.today()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)
    three_days_ago = today - timedelta(days=3)

    # Request 1: Normal priority, open
    r1 = Request(
        request_id="REQ001",
        customer_name="Ada Obi",
        customer_email="ada@example.com",
        subject="Cannot log into account",
        date_received=three_days_ago,
        status="open",
        priority="normal",
    )
    r1.replies = [
        "Thanks for reporting this issue.",
        "We've reset your password. Please check your email.",
        "Let us know if you can now log in.",
    ]

    # Request 2: High priority, processing
    r2 = Request(
        request_id="REQ002",
        customer_name="Bob Smith",
        customer_email="bob@example.com",
        subject="Billing discrepancy - charged twice",
        date_received=two_days_ago,
        status="processing",
        priority="high",
    )
    r2.replies = [
        "We've identified the duplicate charge.",
        "Refund has been initiated (5-7 business days).",
    ]

    # Request 3: Normal priority, closed
    r3 = Request(
        request_id="REQ003",
        customer_name="Carol Jones",
        customer_email="carol@example.com",
        subject="Feature request: Dark mode",
        date_received=yesterday,
        status="closed",
        priority="normal",
    )
    r3.replies = ["Thanks for the suggestion!", "Dark mode is on our roadmap for Q2."]

    # Request 4: Another from Ada Obi (tests search by name)
    r4 = Request(
        request_id="REQ004",
        customer_name="Ada Obi",
        customer_email="ada@example.com",
        subject="Follow-up: Still can't log in",
        date_received=today,
        status="open",
        priority="high",
    )
    r4.replies = ["Escalating to senior support team."]

    # Request 5: Low priority
    r5 = Request(
        request_id="REQ005",
        customer_name="David Kim",
        customer_email="david@example.com",
        subject="General inquiry about pricing",
        date_received=today,
        status="open",
        priority="low",
    )
    r5.replies = ["Our sales team will contact you within 24 hours."]

    # Add all requests
    for req in [r1, r2, r3, r4, r5]:
        system.add_request(req)

    return system


def demo():
    """Run a full demonstration of the system."""
    today = date.today()
    print("=" * 60)
    print("SUPPORT REQUEST SYSTEM - DEMO")
    print("=" * 60)

    system = create_sample_system()

    # Show all requests
    print("\n--- ALL REQUESTS ---")
    for req in system.requests.values():
        print(
            f"  {req.request_id} | {req.customer_name} | {req.subject} | {req.status} | {req.priority}"
        )

    # Demonstrate queue processing
    print("\n--- QUEUE PROCESSING (FIFO) ---")
    # Create fresh system to show queue order
    demo_system = SupportSystem()
    for req in [
        system.requests["REQ001"],
        system.requests["REQ002"],
        system.requests["REQ003"],
    ]:
        demo_system.add_request(req)

    print("  Processing order:")
    while True:
        processed = demo_system.process_next()
        if processed is None:
            break
        print(f"    Processed: {processed.request_id} ({processed.subject})")

    # Demonstrate search
    print("\n--- SEARCH BY ID (O(1)) ---")
    result = search_by_id(system, "REQ002")
    print(f"  Found: {result.request_id} - {result.subject}")

    print("\n--- SEARCH BY NAME (O(n)) ---")
    results = search_by_name(system, "Ada Obi")
    print(f"  Found {len(results)} requests for 'Ada Obi':")
    for r in results:
        print(f"    {r.request_id} - {r.subject}")

    # Demonstrate sorting
    print("\n--- SORT BY DATE (built-in sorted) ---")
    sorted_by_date = sort_requests(system, by="date")
    for r in sorted_by_date:
        print(f"  {r.date_received} | {r.request_id} | {r.subject}")

    print("\n--- SORT BY PRIORITY (both methods agree) ---")
    builtin_priority = sort_requests(system, by="priority")
    manual_priority = insertion_sort_requests(system, by="priority")
    for b, m in zip(builtin_priority, manual_priority):
        match = "OK" if b.request_id == m.request_id else "FAIL"
        print(f"  {match} {b.request_id} | {b.priority} | {b.subject}")

    print("\n--- SORT BY STATUS ---")
    sorted_by_status = sort_requests(system, by="status")
    for r in sorted_by_status:
        print(f"  {r.status} | {r.request_id} | {r.subject}")

    # Demonstrate undo
    print("\n--- UNDO STACK ---")
    undo_system = SupportSystem()
    test_req = Request("REQ999", "Test User", "test@example.com", "Test", today)
    undo_system.add_request(test_req)
    print(f"  Initial priority: {undo_system.requests['REQ999'].priority}")
    undo_system.mark_urgent("REQ999")
    print(f"  After mark_urgent: {undo_system.requests['REQ999'].priority}")
    undone = undo_system.undo()
    print(f"  Undone: {undone}")
    print(f"  After undo: {undo_system.requests['REQ999'].priority}")

    # Demonstrate recursive replies
    print("\n--- RECURSIVE REPLY DISPLAY ---")
    print("  Flat view:")
    for line in display_replies(system.requests["REQ001"].replies):
        print(f"    {line}")

    print("\n  Threaded/indented view:")
    for line in display_replies_indented(system.requests["REQ001"].replies):
        print(f"    {line}")

    # Demonstrate duplicate rejection
    print("\n--- DUPLICATE ID REJECTION ---")
    try:
        dup = Request("REQ001", "Someone", "x@example.com", "Duplicate", today)
        system.add_request(dup)
    except ValueError as e:
        print(f"  Correctly rejected: {e}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    demo()

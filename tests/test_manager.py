import pytest
from support_system.manager import SupportSystem
from support_system.models import Request
from datetime import date


def test_add_request():
    system = SupportSystem()
    r1 = Request("REQ001", "Ada Obi", "ada@example.com", "Can't log in", date.today())
    system.add_request(r1)
    assert "REQ001" in system.requests


def test_duplicate_id_rejected():
    system = SupportSystem()
    r1 = Request("REQ001", "Ada Obi", "ada@example.com", "Can't log in", date.today())
    system.add_request(r1)
    r2 = Request("REQ001", "Someone Else", "x@example.com", "Billing issue", date.today())
    with pytest.raises(ValueError):
        system.add_request(r2)


def test_queue_order():
    system = SupportSystem()
    r1 = Request("REQ001", "Ada Obi", "ada@example.com", "Can't log in", date.today())
    r2 = Request("REQ002", "Bob Smith", "bob@example.com", "Billing issue", date.today())
    system.add_request(r1)
    system.add_request(r2)
    
    # Process in FIFO order
    processed1 = system.process_next()
    assert processed1.request_id == "REQ001"
    assert processed1.status == "processing"
    
    processed2 = system.process_next()
    assert processed2.request_id == "REQ002"
    assert processed2.status == "processing"
    
    # Queue empty
    assert system.process_next() is None


def test_mark_urgent():
    system = SupportSystem()
    r1 = Request("REQ001", "Ada Obi", "ada@example.com", "Can't log in", date.today())
    system.add_request(r1)
    
    system.mark_urgent("REQ001")
    assert system.requests["REQ001"].priority == "high"


def test_undo_mark_urgent():
    system = SupportSystem()
    r1 = Request("REQ001", "Ada Obi", "ada@example.com", "Can't log in", date.today())
    system.add_request(r1)
    
    system.mark_urgent("REQ001")
    assert system.requests["REQ001"].priority == "high"
    
    # Undo should restore to "normal"
    undone = system.undo()
    assert undone == ("priority", "REQ001", "normal")
    assert system.requests["REQ001"].priority == "normal"


def test_undo_process_next():
    system = SupportSystem()
    r1 = Request("REQ001", "Ada Obi", "ada@example.com", "Can't log in", date.today())
    system.add_request(r1)
    
    system.process_next()
    assert system.requests["REQ001"].status == "processing"
    
    # Undo should restore to "open"
    undone = system.undo()
    assert undone == ("status", "REQ001", "open")
    assert system.requests["REQ001"].status == "open"


def test_undo_empty_history():
    system = SupportSystem()
    assert system.undo() is None

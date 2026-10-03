from dataclasses import dataclass, field
from datetime import date


@dataclass
class Request:
    """A single customer support request."""

    request_id: str
    customer_name: str
    customer_email: str
    subject: str
    date_received: date
    status: str = "open"#status and priority have defaults, so callers don't have to specify them for a normal new request.
    priority: str = "normal"
    replies: list = field(default_factory=list) #replies uses field(default_factory=list) rather than replies=[]

    
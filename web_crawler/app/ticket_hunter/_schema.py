__all__ = [
    "ContactsSchema",
]

from datetime import datetime
from pydantic import BaseModel

class RequestsSchema:
    class ticket_hunter(BaseModel):
        """
        ticket criterea form received from client.
        """

        endDate: datetime
        startDate: datetime
        departure: str
        arrival: str
        adult: int


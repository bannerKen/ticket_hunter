__all__ = [
    "Ticket_hunterSchema",
    "Direction"
]

from datetime import date
from pydantic import BaseModel
from enum import Enum

class TicketHunterSchema:
    class RequestForm(BaseModel):
        """
        ticket criterea form received from client.
        """

        endDate: date
        startDate: date
        departure: str
        arrival: str
        adult: int

class Direction(Enum):
    GO = 'go'
    BACK = 'back'
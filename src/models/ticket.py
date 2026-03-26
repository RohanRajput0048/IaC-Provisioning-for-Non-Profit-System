from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UrgencyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TicketStatus(str, Enum):
    OPEN = "open"
    AUTO_RESOLVED = "auto-resolved"

class Ticket(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: Optional[str] = Field(None, description="Extracted name of the person")
    email_or_contact: Optional[str] = Field(None, description="Extracted email or contact number")
    date: Optional[str] = Field(None, description="Any specific date mentioned")
    amount: Optional[str] = Field(None, description="Donation or transaction amount")
    urgency: UrgencyLevel = Field(..., description="High, medium, or low urgency")
    status: str = Field(default="open", description="Ticket status")
    resolution_days: int = Field(..., description="SLA for ticket resolution")
    original_message: str = Field(...)
    draft_response: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Optional
from src.utils.config import GEMINI_API_KEY
from src.agents.prompts import CLASSIFICATION_EXTRACTION_PROMPT
from src.models.ticket import Ticket, UrgencyLevel, TicketStatus
import json

class ExtractInfoSchema(BaseModel):
    urgency: UrgencyLevel = Field(description="urgency of the message: high, medium, or low")
    resolution_days: int = Field(description="number of days to resolve based on urgency")
    id: Optional[str] = Field(None, description="ticket id or reference number if given")
    date: Optional[str] = Field(None, description="date mentioned in the message")
    amount: Optional[str] = Field(None, description="donation amount or transaction amount")
    name: Optional[str] = Field(None, description="name of the person")
    email_or_contact: Optional[str] = Field(None, description="email or contact number")
    draft_response: str = Field(description="draft response to the user")

class TriageAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=GEMINI_API_KEY,
            temperature=0.2
        )
        self.prompt = PromptTemplate(
            template=CLASSIFICATION_EXTRACTION_PROMPT,
            input_variables=["message"]
        )
        # Using structured output for reliable json enforcement
        self.chain = self.prompt | self.llm.with_structured_output(ExtractInfoSchema)

    def process_message(self, message: str) -> Ticket:
        """
        Process the incoming message, extract info, determine urgency
        and create a structured Ticket object (without an ID initially, as MongoDB provides that).
        """
        response: ExtractInfoSchema = self.chain.invoke({"message": message})
        status = TicketStatus.AUTO_RESOLVED if response.urgency == UrgencyLevel.LOW else TicketStatus.OPEN

        ticket = Ticket(
            date=response.date,
            amount=response.amount,
            name=response.name,
            email_or_contact=response.email_or_contact,
            urgency=response.urgency,
            resolution_days=response.resolution_days,
            status=status,
            original_message=message,
            draft_response=response.draft_response
        )
        return ticket

triage_agent = TriageAgent()

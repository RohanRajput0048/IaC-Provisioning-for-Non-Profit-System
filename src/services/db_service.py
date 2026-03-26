from pymongo import MongoClient
from src.utils.config import MONGO_URL, DATABASE_NAME
from src.models.ticket import Ticket
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.client = None
        self.db = None
        self.tickets_collection = None

    def _init_db(self):
        if self.client is None:
            try:
                self.client = MongoClient(MONGO_URL)
                self.db = self.client[DATABASE_NAME]
                self.tickets_collection = self.db.get_collection("tickets")
                logger.info("Successfully connected to MongoDB.")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise

    def save_ticket(self, ticket: Ticket) -> str:
        self._init_db()
        """Save a ticket to the database and return its inserted ID."""
        try:
            ticket_dict = ticket.dict(by_alias=True, exclude_none=True)
            result = self.tickets_collection.insert_one(ticket_dict)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving ticket: {e}")
            raise

    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        self._init_db()
        from bson.objectid import ObjectId
        try:
            document = self.tickets_collection.find_one({"_id": ObjectId(ticket_id)})
            if document:
                document["id"] = str(document["_id"])
                return Ticket(**document)
            return None
        except Exception as e:
            logger.error(f"Error retrieving ticket: {e}")
            return None

db_service = DatabaseService()

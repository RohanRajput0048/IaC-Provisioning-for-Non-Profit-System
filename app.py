from flask import Flask, request, jsonify
import logging

from src.agents.triage_agent import triage_agent
from src.services.db_service import db_service

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/")
def home():
    return "Non-Profit Triage Agent API is running 🚀"


@app.route("/triage", methods=["POST"])
def triage():
    try:
        data = request.get_json()
        message = data.get("message")

        if not message:
            return jsonify({"error": "Message is required"}), 400

        # Process message
        ticket = triage_agent.process_message(message)

        # Save to DB
        ticket_id = db_service.save_ticket(ticket)

        response = {
            "ticket_id": ticket_id,
            "urgency": ticket.urgency,
            "status": ticket.status,
            "resolution_days": ticket.resolution_days,
            "name": ticket.name,
            "date": ticket.date,
            "amount": ticket.amount,
            "contact": ticket.email_or_contact,
            "draft_response": ticket.draft_response
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
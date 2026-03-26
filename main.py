import sys
import logging

from src.agents.triage_agent import triage_agent
from src.services.db_service import db_service

logging.basicConfig(level=logging.INFO)

def main():
    print("====================================================")
    print("      Non-Profit Triage Agent - Interactive Testing ")
    print("====================================================")
    print("Type 'exit' or 'quit' to stop.")
    
    while True:
        try:
            message = input("\nEnter donor/beneficiary message: ")
            if message.lower() in ['exit', 'quit']:
                break
            if not message.strip():
                continue
                
            print("\n[Agent Status]: Processing message...")
            # Call Langchain agent
            ticket = triage_agent.process_message(message)
            
            print("\n--- Triage Result ---")
            
            print("[Agent Status]: Saving Ticket to Database...")
            ticket_id = db_service.save_ticket(ticket)
            
            print(f"[*] Ticket ID       : {ticket_id}")
            print(f"[*] Urgency         : {ticket.urgency.upper()}")
            print(f"[*] Status          : {ticket.status.upper()}")
            print(f"[*] Resolution Time : {ticket.resolution_days} days")
            print(f"[*] Extracted Name  : {ticket.name}")
            print(f"[*] Extracted Date  : {ticket.date}")
            print(f"[*] Extracted Amt   : {ticket.amount}")
            print(f"[*] Extracted Cont  : {ticket.email_or_contact}")
            
            print("\n[*] Draft Response:")
            print(ticket.draft_response)
            print("---------------------")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n[!] Error processing message: {e}")

if __name__ == "__main__":
    main()

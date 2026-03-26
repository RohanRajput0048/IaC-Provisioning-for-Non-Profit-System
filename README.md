# Non-Profit Triage AI Agent 🤖

An intelligent, production-grade triage agent designed for Non-Profit organizations to automate their initial response workflows. Built with a modern python tech-stack, this system processes incoming text queries from donors and beneficiaries, analyzes intent and urgency, extracts structured data, and securely logs everything to a database.

## 🚀 Features

*   **Intelligent AI Triage:** Uses Google's Gemini LLM (via LangChain) to instantly analyze incoming messages.
*   **Automated Urgency Detection:** Automatically flags messages as High, Medium, or Low urgency (e.g., failed donations vs. general feedback) and assigns appropriate resolution service-level agreements (SLAs).
*   **Named Entity Recognition (NER):** Extracts critical data points directly from unstructured text, including Names, Contact Information (Emails/Phone numbers), Dates, and Donation Amounts.
*   **Drafted Responses:** Automatically generates context-aware, empathetic draft responses that support teams can use to accelerate resolution times.
*   **Secure Authentication:** Built-in Streamlit UI login system utilizing `bcrypt` password hashing.
*   **Cloud Database Integration:** Fully integrated with MongoDB Atlas (via synchronous `pymongo`) for permanent, scalable ticket and user storage.
*   **Modern UI:** Features a sleek, responsive frontend built entirely in Streamlit with custom CSS.

## 🛠️ Technology Stack

*   **Frontend UI:** Streamlit
*   **LLM Integration:** LangChain (`langchain-google-genai`), Gemini 1.5 Flash
*   **Data Validation:** Pydantic
*   **Database:** MongoDB Atlas (`pymongo`)
*   **Security:** `bcrypt` (Password Hashing)
*   **Language:** Python 3.x

## ⚙️ Installation & Setup

1. **Clone the Repository** and navigate to the project folder.
2. **Install the Requirements:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Setup:** Create a `.env` file in the root directory with the following variables:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   MONGO_URL=your_mongodb_atlas_connection_string
   DATABASE_NAME=triage_db
   ```
4. **Run the Application:**
   Launch the Streamlit frontend UI:
   ```bash
   python -m streamlit run src\frontend\app.py
   ```
   *(Alternatively, run `python main.py` for a terminal-only CLI testing experience).*

## 📖 Usage

1. Open the Streamlit URL provided in your terminal (usually `http://localhost:8501`).
2. Create an account via the **Sign Up** tab.
3. Log in to access the secure Agent UI.
4. Type an unstructured message in the chat box (e.g., *"Hi, I tried donating $50 yesterday but the site crashed! Please help, my email is test@test.com"*).
5. Watch the AI parse the data, assign an urgency ticket, and draft a response in real-time!

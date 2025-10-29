from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from chatbot.rag import RAGSystem
import google.generativeai as genai
import os
from datetime import datetime
from chatbot.models import ChatRequest, ChatResponse
import mysql.connector   # ✅ added
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# -------------------------------
# 1. Initialize FastAPI app
# -------------------------------
app = FastAPI(title="Luvetha Tech AI Chatbot")

# Allow frontend requests (React, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # optionally restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# 2. Configure Gemini API
# -------------------------------
google_api_key = os.getenv("GOOGLE_API_KEY")
if google_api_key:
    os.environ["GOOGLE_API_KEY"] = google_api_key
else:
    print("Warning: GOOGLE_API_KEY not found in environment variables")

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB2_NAME")

# -------------------------------
# 3. Configure MySQL Database
# -------------------------------
db_config = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,  # ✅ change this
    "database": DB_NAME       # ✅ create this in MySQL
}

# connect at startup
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# create table if not exists
def create_chat_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(100),
            user_message TEXT,
            bot_reply TEXT,
            timestamp DATETIME
        )
    """)
    conn.commit()
    conn.close()

# -------------------------------
# 4. Initialize RAG system
# -------------------------------
rag: RAGSystem | None = None

@app.on_event("startup")
async def startup_event():
    global rag
    print("⚙️ Starting up app and loading RAG system...")
    rag = RAGSystem(data_folder="data")  # ✅ initialize your RAGSystem
    create_chat_table()                  # ✅ create table at startup
    print("✅ RAG System and MySQL connected.")


# -------------------------------
# 5. Define /chat route
# -------------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    if rag is None:
        raise HTTPException(status_code=500, detail="RAG system not initialized")

    # Step 1: Retrieve relevant documents using RAG
    context_docs = rag.retrieve(req.message)
    context_text = "\n\n".join(context_docs)

    # Step 2: Construct prompt for Gemini
    prompt = f"""
You are a helpful AI assistant for Luvetha Tech.
Use the following company context if relevant to the question:

{context_text}

User: {req.message}
Answer:
"""

    # Step 3: Call Gemini via official SDK
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        reply = response.text.strip() if response.text else "Sorry, I couldn’t generate a response."
    except Exception as e:
        reply = f"Error generating response: {str(e)}"

    # Step 4: Save to MySQL ✅
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (session_id, user_message, bot_reply, timestamp) VALUES (%s, %s, %s, %s)",
            (req.session_id, req.message, reply, datetime.utcnow())
        )
        conn.commit()
        conn.close()
    except Exception as db_error:
        print(f"⚠️ Database error: {db_error}")

    # Step 5: Return response
    return ChatResponse(
        reply=reply,
        session_id=req.session_id,
        timestamp=datetime.utcnow()
    )
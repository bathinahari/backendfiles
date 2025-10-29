from fastapi import FastAPI
from chatbot.main import app as chatbot_app
from contact_form.main1 import app as contact_form_app

app=FastAPI()
app.mount("/chatbot", chatbot_app)
app.mount("/contact_form", contact_form_app)

@app.get("/")
def read_root():
    return {"message": "Welcome to Luvetha Tech API. Use /chatbot for AI Chatbot and /contact_form for Contact Form."}
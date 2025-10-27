from fastapi import FastAPI, Form
from db import save_contact_form
from twilio.rest import Client
import uvicorn

app = FastAPI()

# Twilio credentials (get these from your Twilio Console)
ACCOUNT_SID = "AC788365d8079e60279c3c60a6e406b936"
AUTH_TOKEN = "ae2cfc8dfa4ee8bcbbe8f2c3cd3a3725"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number
ADMIN_WHATSAPP_NUMBER = "whatsapp:+919493487997"  # Your WhatsApp number

def send_whatsapp_notification(name, email, contact_no, message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    msg_body = f"📩 New Contact Form Submission:\n\n👤 Name: {name}\n📧 Email: {email}\n📞 Contact: {contact_no}\n💬 Message: {message}"
    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=msg_body,
        to=ADMIN_WHATSAPP_NUMBER
    )
    print("✅ WhatsApp notification sent to admin.")


@app.post("/contact")
def contact(
    name: str = Form(...),
    email: str = Form(...),
    contact_no: str = Form(...),
    message: str = Form(...)
):
    # 1️⃣ Save to database
    save_contact_form(name, email, contact_no, message)
    
    # 2️⃣ Send WhatsApp notification
    send_whatsapp_notification(name, email, contact_no, message)
    
    return {"status": "success", "message": "Thank you for contacting us!"}

if __name__ == "__main__":
    
    uvicorn.run(app, host="localhost", port=5000)
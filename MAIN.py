from fastapi import FastAPI
import os
import traceback


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Luvetha Tech API. Use /chatbot for AI Chatbot and /contact_form for Contact Form."}

@app.get("/debug")
def debug_info():
    return {
        "status": "running", 
        "service": "backendfiles-5",
        "endpoints": {
            "root": "GET /",
            "debug": "GET /debug"
        }
    }

# Add these test endpoints to verify mounting
@app.get("/test-mount-chatbot")
def test_chatbot_mount():
    return {"chatbot_mounted": "chatbot_app" in globals()}

@app.get("/test-mount-contact")
def test_contact_mount():
    return {"contact_form_mounted": "contact_form_app" in globals()}

# Global variables to track mounted apps
chatbot_app = None
contact_form_app = None

# Mount apps with comprehensive error handling
print("🚀 Starting application mounting...")

# Mount Chatbot
try:
    print("🔄 Importing chatbot...")
    from chatbot.main import app as chatbot_app_import
    chatbot_app = chatbot_app_import
    app.mount("/chatbot", chatbot_app)
    print("✅ Chatbot mounted successfully at /chatbot")
    
except Exception as e:
    print(f"❌ Failed to mount chatbot: {str(e)}")
    print(f"Chatbot traceback: {traceback.format_exc()}")
    chatbot_app = None

# Mount Contact Form
try:
    print("🔄 Importing contact form...")
    from contact_form.main1 import app as contact_form_app_import
    contact_form_app = contact_form_app_import
    app.mount("/contact_form", contact_form_app)
    print("✅ Contact form mounted successfully at /contact_form")
    
except Exception as e:
    print(f"❌ Failed to mount contact form: {str(e)}")
    print(f"Contact form traceback: {traceback.format_exc()}")
    contact_form_app = None

# Add fallback endpoints that will actually work
@app.get("/chatbot/health")
def chatbot_health():
    if chatbot_app is None:
        return {"status": "unavailable", "error": "Chatbot failed to load during startup"}
    return {"status": "healthy", "service": "chatbot"}

@app.get("/contact_form/health") 
def contact_form_health():
    if contact_form_app is None:
        return {"status": "unavailable", "error": "Contact form failed to load during startup"}
    return {"status": "healthy", "service": "contact_form"}

print("🎉 All mounting attempts completed")
print(f"Chatbot mounted: {chatbot_app is not None}")
print(f"Contact form mounted: {contact_form_app is not None}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("MAIN:app", host="0.0.0.0", port=port, reload=False)

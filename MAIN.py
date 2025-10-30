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
            "debug": "GET /debug",
            "chatbot_health": "GET /chatbot/health",
            "contact_form_health": "GET /contact_form/health"
        }
    }

# Mount apps with comprehensive error handling
print("🚀 Starting application mounting...")

# Mount Chatbot
try:
    print("🔄 Importing chatbot...")
    from chatbot.main import app as chatbot_app
    app.mount("/chatbot", chatbot_app)
    print("✅ Chatbot mounted successfully at /chatbot")
    
    # Add a fallback health check for chatbot
    @app.get("/chatbot/health-fallback")
    def chatbot_health_fallback():
        return {"status": "chatbot fallback health check"}
        
except Exception as e:
    print(f"❌ Failed to mount chatbot: {str(e)}")
    print(f"Chatbot traceback: {traceback.format_exc()}")
    
    @app.get("/chatbot/health")
    def chatbot_fallback():
        return {"status": "unavailable", "error": "Chatbot failed to load"}

# Mount Contact Form
try:
    print("🔄 Importing contact form...")
    from contact_form.main1 import app as contact_form_app
    app.mount("/contact_form", contact_form_app)
    print("✅ Contact form mounted successfully at /contact_form")
    
    # Add a fallback health check for contact form
    @app.get("/contact_form/health-fallback")
    def contact_form_health_fallback():
        return {"status": "contact form fallback health check"}
        
except Exception as e:
    print(f"❌ Failed to mount contact form: {str(e)}")
    print(f"Contact form traceback: {traceback.format_exc()}")
    
    @app.get("/contact_form/health")
    def contact_form_fallback():
        return {"status": "unavailable", "error": "Contact form failed to load"}

print("🎉 All mounting attempts completed")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("MAIN:app", host="0.0.0.0", port=port, reload=False)

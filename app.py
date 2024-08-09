import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from send_email import send_email

app = FastAPI()

class IncomingRequest(BaseModel):
    message: str

class EmailResponse(BaseModel):
    message: str
    status: str

@app.post("/send_email", response_model=EmailResponse)
async def send_email_endpoint(email_request: IncomingRequest):
    try:
        # Use the imported send_email function
        send_email(email_request.message)
        
        # Return a response indicating the email was sent
        return EmailResponse(message="Email sent successfully", status="OK")
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error sending email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
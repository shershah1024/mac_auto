import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Use environment variable for ngrok URL
NGROK_URL = os.environ.get('NGROK_URL')

class IncomingRequest(BaseModel):
    message: str

@app.post("/send_email")
async def send_email_endpoint(email_request: IncomingRequest):
    if not NGROK_URL:
        raise HTTPException(status_code=500, detail="NGROK_URL is not set")
    
    # Forward the request to your local server through ngrok
    ngrok_endpoint = f"{NGROK_URL}/send_email"
    try:
        response = requests.post(ngrok_endpoint, json={"message": email_request.message})
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return {"message": response.json()}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
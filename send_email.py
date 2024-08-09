import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from groq import Groq
import json
from dotenv import load_dotenv
from get_file_paths import get_file_paths
from send_email_with_attachment import send_file_via_mail
from send_email_apple import send_email_apple

load_dotenv()
groq_client = Groq()
MODEL = 'llama3-70b-8192'

app = FastAPI()

class FolderPath(Enum):
    DOWNLOADS = "/Users/shahir/Downloads"
    DELE_A1_AUDIO = '/Users/shahir/Downloads/Dele A1 new audio'

class EmailID(Enum):
    Shahir = "abdul.shahir@gmail.com"
    MIRA = "mira@thesmartlanguage.com"

class IncomingRequest(BaseModel):
    message: str

class EmailResponse(BaseModel):
    message: str
    status: str

def get_folder(message):
    system_message = f"Extract the folder path from the user message. These are the available folders - {[folder.name for folder in FolderPath]}. Output in the json format with a 'folder_name' key."

    messages = [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": message,
        }
    ]

    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=4096,
        response_format = {"type": "json_object"},
    )

    folder = json.loads(response.choices[0].message.content)
    folder_name = folder.get("folder_name")
    
    try:
        folder_path = FolderPath[folder_name].value
        print(f"Selected folder path: {folder_path}")
        return folder_path
    except KeyError:
        print(f"Invalid folder name: {folder_name}")
        return None

def get_file_to_send(message):
    folder_path = get_folder(message)
    if folder_path is None:
        return []
    files_in_the_folder = get_file_paths(folder_path)
    return files_in_the_folder

def send_email(message):
    determine_attachment_messages = [
        {
            "role": "system",
            "content": "Analyze the user's message and determine if it requires sending an email with an attachment. Respond with a JSON object containing a boolean 'requires_attachment'."
        },
        {
            "role": "user",
            "content": message
        }
    ]
    
    attachment_response = groq_client.chat.completions.create(
        model=MODEL,
        messages=determine_attachment_messages,
        max_tokens=100,
        response_format={"type": "json_object"}
    )
    
    attachment_decision = json.loads(attachment_response.choices[0].message.content)
    requires_attachment = attachment_decision.get('requires_attachment', False)
    
    file_paths = get_file_to_send(message) if requires_attachment else []
    
    messages = [
        {
            "role": "system",
            "content": f"You are a function calling LLM that uses the data extracted from the user message to send an email{'with an attachment' if requires_attachment else ''}. {'The files are available in the file list: ' + str(file_paths) if requires_attachment else ''} The available email IDs are: {', '.join([f'{email.name}: {email.value}' for email in EmailID])}. Use the enum name (e.g., Shahir, MIRA) when specifying the recipient."
        },
        {
            "role": "user",
            "content": message,
        }
    ]
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": f"send an email{'with an attachment' if requires_attachment else ''}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recipient": {
                            "type": "string",
                            "enum": [email.name for email in EmailID],
                            "description": "The enum name of the recipient's email ID (e.g., Shahir, MIRA)"
                        },
                        "subject": {
                            "type": "string",
                            "description": "The subject of the email. Write an appropriate subject based on the message"
                        },
                        "email_body": {
                            "type": "string",
                            "description": "The body of the email. You can also create it from the message"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "The path to the attachment (if applicable)"
                        } if requires_attachment else {}
                    },
                    "required": ["recipient", "subject", "email_body"] + (["file_path"] if requires_attachment else [])
                }
            }
        },
    ]

    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )

    response_message = response.choices[0].message
    function_response = ""
    tool_calls = response_message.tool_calls

    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if function_name == "send_email":
                # Convert the enum name to the actual email address
                recipient_email = EmailID[function_args.get("recipient")].value
                
                if requires_attachment:
                    function_response = send_file_via_mail(
                        recipient=recipient_email,
                        subject=function_args.get("subject"),
                        email_body=function_args.get("email_body"),
                        file_path=function_args.get("file_path"),
                    )
                    print(f"The running function is {send_file_via_mail}")
                else:
                    function_response = send_email_apple(
                        receiver=recipient_email,
                        subject=function_args.get("subject"),
                        email_body=function_args.get("email_body")
                    )
                    print(f"The running function is {send_email_apple}")

        print(function_response)
        return function_response

@app.post("/send_email", response_model=EmailResponse)
async def send_email_endpoint(email_request: IncomingRequest):
    try:
        send_email(email_request.message)
        return EmailResponse(message="Email sent successfully", status="OK")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
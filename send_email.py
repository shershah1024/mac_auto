from enum import Enum
from send_email_gmail_compose import send_email_gmail
from mac_or_chrome_whatsapp import send_whatsapp_chat
from groq import Groq
import os, json
from dotenv import load_dotenv
from get_file_paths import get_file_paths
from send_email_with_attachment import send_file_via_mail
from new_gmail_compose import compose_and_send_email
load_dotenv()
groq_client = Groq()
MODEL = 'llama3-70b-8192'

class FolderPath(Enum):
    DOWNLOADS = "/Users/shahir/Downloads"
    DELE_A1_AUDIO = '/Users/shahir/Downloads/Dele A1 new audio'

class EmailID(Enum):
    ABDUL = "abdul.shahir@gmail.com"
    MIRA = "mira@thesmartlanguage.com"

folder_paths = [path.value for path in FolderPath]
email_ids = [email.value for email in EmailID]

example_json = {"folder_path": "/sample_path"}

def get_folder(message):
    system_message = f"Extract the folder path from the user message. These are the available folders - {folder_paths}. Output in the json format"

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

    folder = response.choices[0].message.content
    folder = json.loads(folder)
    folder_path = folder["folder_path"]
    print(folder_path)

    return folder_path

def get_file_to_send(message):
    folder_path = get_folder(message)
    files_in_the_folder = get_file_paths(folder_path)
    return files_in_the_folder

def send_email(message):
    # First, determine if the message requires an attachment
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
            "content": f"You are a function calling LLM that uses the data extracted from the user message to send an email{'with an attachment' if requires_attachment else ''}. {'The files are available in the file list: ' + str(file_paths) if requires_attachment else ''}"
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
                "description": f"send an email{'with an attachment' if requires_attachment else ''} through gmail",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recipient_email": {
                            "type": "string",
                            "description": "The email id of the recipient"
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
                    "required": ["recipient_email", "subject", "email_body"] + (["file_path"] if requires_attachment else [])
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
                if requires_attachment:
                    function_response = send_file_via_mail(
                        recipient_email=function_args.get("recipient_email"),
                        subject=function_args.get("subject"),
                        message_body=function_args.get("email_body"),
                        file_path=function_args.get("file_path"),
                    )
                    print(f"The running function is {send_file_via_mail}")
                else:
                    function_response = compose_and_send_email(
                        receiver_email=function_args.get("recipient_email"),
                        subject=function_args.get("subject"),
                        email_body=function_args.get("email_body")
                    )
                    print(f"The running function is {compose_and_send_email}")

        print(function_response)
        return function_response

# Example usage
message_with_attachment = "I have a file called presentations 1 in my downloads folder. Please send it to abdul.shahir@gmail.com"
message_without_attachment = "Please send an email to mira@thesmartlanguage.com about the upcoming meeting"

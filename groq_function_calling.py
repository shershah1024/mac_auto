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

def send_email_with_attachments(message):
    user_prompt=message
    file_paths = get_file_to_send(message)
    messages=[
            {
                "role": "system",
                "content": f"You are a function calling LLM that uses the data extracted from the user message to find the exact file that need to be sent and sends it as an attachment in email. The files are available in the file list-  {file_paths} "
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "send_file_via_mail",
                "description": "send an email with an attachment",
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
                        "message_body": {
                            "type": "string",
                            "description": "The body of the email. Don't mention that you sending it from a specific folder. Write an email body based on the message"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "The path to the attachment"
                        }
                    },
                    "required": ["recipient_email", "subject", "message_body", "file_path"]
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
    function_response=""
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "send_file_via_mail": send_file_via_mail,
        }

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if function_name=="send_file_via_mail":
                function_response = function_to_call(
                    recipient_email=function_args.get("recipient_email"),
                    subject=function_args.get("subject"),
                    message_body=function_args.get("message_body"),
                    file_path=function_args.get("file_path"),
                )
                print(f"the running function is {send_email_gmail}")

        print(function_response)
        return function_response

def get_folder(message):
    system_message= f"Extract the folder path from the user message. These are the available folders - {folder_paths}. Output in the json format"

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

    folder= response.choices[0].message.content
    folder=json.loads(folder)
    folder_path = folder["folder_path"]
    print(folder_path)

    return folder_path

def get_file_to_send(message):
    folder_path= get_folder(message)
    files_in_the_folder=get_file_paths(folder_path)
    return files_in_the_folder

def send_email(message):
    user_prompt=message

    messages=[
            {
                "role": "system",
                "content": f"You are a function calling LLM that uses the data extracted from the user message to either send an email or send a whatsapp message "
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "compose_and_send_email",
                "description": "send an email through gmail",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "receiver_email": {
                            "type": "string",
                            "description": "The email id of the recipient"
                        },
                        "subject": {
                            "type": "string",
                            "description": "The subject of the email. If it is not mentioned, you can create one"
                        },
                        "email_body": {
                            "type": "string",
                            "description": "The body of the email. You can also create it from the message"
                        }
                    },
                    "required": ["receiver_email", "subject", "email_body"]
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
    function_response=""
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "compose_and_send_email": compose_and_send_email,
            "send_whatsapp_chat":send_whatsapp_chat
        }

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if function_name=="compose_and_send_email":
                function_response = function_to_call(
                    receiver_email=function_args.get("receiver_email"),
                    subject=function_args.get("subject"),
                    email_body=function_args.get("email_body")
                )
                print(f"the running function is {send_email_gmail}")
            if function_name=="send_whatsapp_chat":
                function_response = function_to_call(
                    contact_name=function_args.get("contact_name"),
                    message=function_args.get("message"),
                )
                print(f"The running function is {send_whatsapp_chat}")
        print(function_response)
        return function_response

message= "I have a file called presntations 1 in my downloads folder. Please send it to abdul.shahir@gmail.com"
send_email_with_attachments(message)
from groq import Groq
import os
import json
from dotenv import load_dotenv
from send_email_gmail_compose import send_email_gmail
from mac_or_chrome_whatsapp import send_whatsapp_chat
from chainlit.element import ElementBased
import chainlit as cl


load_dotenv()

client = Groq(api_key = os.getenv('GROQ_API_KEY'))
MODEL = 'llama3-70b-8192'

@cl.on_message
async def run_conversation(user_prompt:cl.Message):
    # Step 1: send the conversation and available functions to the model
    messages=[
        {
            "role": "system",
            "content": "You are a function calling LLM that uses the data extracted from the user message to either send a whatsapp message or send an email"
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
            "name": "send_email_gmail",
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
                        "description": "The body of the email"
                    }
                },
                "required": ["receiver_email", "subject", "email_body"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_whatsapp_chat",
            "description": "send a WhatsApp message to the contact",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_name": {
                        "type": "string",
                        "description": "The name of the contact"
                    },
                    "message": {
                        "type": "string",
                        "description": "The body of the message"
                    }
                },
                "required": ["contact_name", "message"]
            }
        }
    }
]



    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "send_email_gmail": send_email_gmail,
            "send_whatsapp_chat":send_whatsapp_chat
        }  # only one function in this example, but you can have multiple

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if function_name=="send_email_gmail":
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


                await cl.Message(
                    content=f"Received: Success",
                ).send()

            """
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )  # get a new response from the model where it can see the function response
        return second_response.choices[0].message.content
        """
        return "Completed the function successfully"

user_prompt = "Please send a an email to abdul.shahir@maitrise.co.in and tell him that we have to meet at 9 tomorrow"
print(run_conversation(user_prompt))


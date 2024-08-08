from fastapi import FastAPI, Form
import subprocess
import uvicorn



def send_whatsapp_message(contact_name: str, message: str):
    applescript = f'''
    -- Copy the message to the clipboard
    set the clipboard to "{message}"
    tell application "WhatsApp"
        activate
        delay 1  -- Ensure the application has time to respond
        tell application "System Events"
            tell process "WhatsApp"
                set frontmost to true
                delay 1
                -- Use Command + N to open a new chat
                keystroke "n" using command down
                delay 1  -- Allow some time for the new chat window to fully open

                -- Ensure the search field is selected
                keystroke " "  -- Attempt to activate the search field
                keystroke (ASCII character 8)  -- Backspace to clear any unwanted space
                delay 1

                -- Type the contact name into the search field
                keystroke "{contact_name}"
                delay 1
                -- Navigate through the search results and select the first contact
                key code 125  -- Down arrow key to navigate
                delay 1
                keystroke return  -- Open the chat
                delay 1

                -- Type and send the message
                keystroke "X X {message}"

                delay 1
                keystroke return  -- Send the message
            end tell
        end tell
    end tell
    '''
    result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
    return result.stdout, result.stderr


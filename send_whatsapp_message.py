from fastapi import FastAPI, Form
import subprocess
import uvicorn

app = FastAPI()

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
"""
@app.post("/send-message/")
def send_message(contact_name: str = Form(...), message: str = Form(...)):
    stdout, stderr = send_whatsapp_message(contact_name, message)
    return {"stdout": stdout, "stderr": stderr}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

"""
contact_name="Ziggi"
message="""
Amt Sent Rs.800.00
From HDFC Bank A/C *3501
To Mr FAISAL  K
On 18-06
For ambulance
"""
send_whatsapp_message(contact_name,message)
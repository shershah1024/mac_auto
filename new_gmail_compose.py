import subprocess
import time

def run_applescript(script):
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.stderr:
        print("Error:", result.stderr)
    return result.stdout.strip()

def open_gmail():
    script = '''
    tell application "Google Chrome"
        activate
        open location "https://mail.google.com/"
        delay 5  -- Wait for Gmail to load
    end tell
    '''
    run_applescript(script)

def compose_and_send_email(receiver_email, subject, email_body):
    open_gmail()
    script = f'''
    tell application "System Events"
        tell process "Google Chrome"
            set frontmost to true
            delay 2
            keystroke "l" using command down  -- Select address bar
            delay 1
            keystroke "https://mail.google.com/mail/u/0/#inbox?compose=new"
            keystroke return
            delay 3  -- Wait for compose window to open

            -- Type the receiver's email
            keystroke "{receiver_email}"
            keystroke return
            delay 1
            keystroke tab
            keystroke "{subject}"
            keystroke tab
            keystroke "{email_body}"

            -- Send the email
            delay 1
            keystroke return using command down  -- Command + Enter to send email
        end tell
    end tell
    '''
    run_applescript(script)




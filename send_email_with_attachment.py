import subprocess

def send_file_via_mail(recipient, subject, email_body, file_path):
    applescript = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{email_body}" & return & return}}

        tell newMessage
            make new to recipient with properties {{address:"{recipient}"}}
            try
                make new attachment with properties {{file name:"{file_path}"}} at after the last paragraph
            on error errMsg
                log "Failed to attach file: " & errMsg
                return false
            end try
        end tell

        send newMessage
        return true
    end tell
    '''

    try:
        result = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True, check=True)
        if "true" in result.stdout.strip().lower():
            print("Email with attachment sent successfully!")
            return True
        else:
            print("Failed to send email with attachment.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while sending the email with attachment: {e}")
        print(f"AppleScript output: {e.output}")
        return False
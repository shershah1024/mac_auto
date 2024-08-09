import subprocess

def send_email_apple(receiver, subject, email_body):
    print(f"Attempting to send email to: {receiver}")
    
    applescript = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{email_body}"}}
        
        tell newMessage
            make new to recipient with properties {{address:"{receiver}"}}
        end tell
        
        send newMessage
        return true
    end tell
    '''
    
    try:
        print("Executing AppleScript...")
        result = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True, check=True)
        print(f"AppleScript output: {result.stdout}")
        if "true" in result.stdout.strip().lower():
            print("Email sent successfully!")
            return True
        else:
            print("Failed to send email.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while sending the email: {e}")
        print(f"AppleScript error output: {e.stderr}")
        return False
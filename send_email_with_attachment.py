import subprocess
from find_a_file import find_similar_files


def send_file_via_mail(recipient_email, subject, message_body, file_path):

    applescript = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{message_body}" & return & return}}

        tell newMessage
            make new to recipient with properties {{address:"{recipient_email}"}}
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
            print("Email sent successfully!")
            return True
        else:
            print("Failed to send email.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while sending the email: {e}")
        print(f"AppleScript output: {e.output}")
        return False



if __name__ == "__main__":
    recipient = "abdul.shahir@gmail.com"
    subject = "1106 propert tax 2024"
    body = "property tax"
    file_path = "/Users/shahir/Downloads/1106 Property Tax 2024.pdf"

    success = send_file_via_mail(recipient, subject, body, file_path)
    if success:
        print("Email process completed successfully.")
    else:
        print("Email process failed.")


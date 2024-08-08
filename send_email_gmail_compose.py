import subprocess
import time

def run_applescript(script):
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.stderr:
        print("Error:", result.stderr)
    return result.stdout.strip()

def is_element_available(selector):
    script = f'''
    tell application "Google Chrome"
        tell the active tab of its first window
            execute javascript "document.querySelector('{selector}') !== null"
        end tell
    end tell
    '''
    return run_applescript(script) == "true"

def wait_until_element_is_available(selector, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_element_available(selector):
            return True
        time.sleep(0.5)
    return False

def send_email_gmail(receiver_email: str, subject: str, email_body: str):
    applescript_open_gmail = '''
    -- Open Gmail in Chrome
    tell application "Google Chrome"
        activate
        open location "https://mail.google.com/"
    end tell
    '''
    run_applescript(applescript_open_gmail)
    if wait_until_element_is_available(".T-I.T-I-KE.L3", 30):  # Check for the Compose button
        applescript_compose_email = f'''
        tell application "System Events"
            tell process "Google Chrome"
                set frontmost to true

                -- Use Command+L to select the address bar
                keystroke "l" using command down
                delay 1

                -- Navigate to the Compose button using tabs
                repeat 17 times
                    key code 48  -- Tab key
                    delay 0.05  -- Reduced delay to speed up tabbing
                end repeat
                keystroke space  -- Open the Compose window
            end tell
        end tell
        '''
        run_applescript(applescript_compose_email)
        if wait_until_element_is_available(".agP", 30):  # Check if the "To" field is available using its class
            applescript_send_email = f'''
            tell application "System Events"
                tell process "Google Chrome"
                    -- Type the receiver's email
                    keystroke "{receiver_email}"
                    delay 1
                    keystroke tab
                    keystroke tab  -- Move to the subject field
                    delay 0.5

                    -- Type the email subject
                    keystroke "{subject}"
                    delay 1
                    keystroke tab  -- Move to the email body
                    delay 0.5

                    -- Type the email body
                    keystroke "{email_body}"
                    delay 1
                    keystroke tab  -- Move to the Send button
                    delay 0.5
                    keystroke space  -- Send the email
                end tell
            end tell
            '''
            run_applescript(applescript_send_email)
        else:
            print("Failed to detect the email 'To' field.")
    else:
        print("Failed to confirm that Gmail loaded properly.")



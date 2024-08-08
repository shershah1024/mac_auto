import subprocess

def send_message_via_whatsapp_web(contact_name, message):
    script = f'''
    tell application "Google Chrome"
        set commandModifier to {{command down}}

        set whatsappURL to "https://web.whatsapp.com/"
        set found to false

        -- Check if there's an existing WhatsApp tab
        repeat with w from 1 to count of windows
            repeat with t from 1 to count of tabs of window w
                if URL of tab t of window w starts with whatsappURL then
                    set found to true
                    tell window w
                        set active tab index to t
                        set index to 1
                    end tell
                    activate application "Google Chrome"
                    exit repeat
                end if
            end repeat
            if found then
                exit repeat
            end if
        end repeat

        -- If WhatsApp is not open, open it in a new tab
        if not found then
            tell window 1
                make new tab with properties {{URL: whatsappURL}}
            end tell
            delay 5 -- Wait for WhatsApp Web to load
        end if

        -- Interact with the WhatsApp tab
        tell application "System Events"
            delay 1 -- Give time for Chrome to become active
            keystroke "l" using commandModifier -- Focus the address bar
            delay 0.5
            keystroke tab -- Move to the search area
            delay 0.5
            keystroke "{contact_name}" -- Type the contact name
            keystroke return -- Press enter to confirm search
            delay 1 -- Wait for the chat to open
            keystroke "{message}" -- Type the message
            keystroke return -- Press enter to send the message
        end tell
    end tell
    '''
    process = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(input=script.encode('utf-8'))
    return stdout.decode().strip()


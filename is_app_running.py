import subprocess

def is_app_running(app_name):
    script = f'''
    tell application "System Events"
        return (name of processes) contains "{app_name}"
    end tell
    '''
    try:
        proc = subprocess.run(['osascript', '-e', script], text=True, capture_output=True)
        print("True")
        return True
    except Exception as e:
        print(f"Error checking app status: {e}")
        return False

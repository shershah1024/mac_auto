import subprocess
import json
import os


def run_applescript(script):
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.stderr:
        print("Error:", result.stderr)
    return result.stdout.strip()


def list_file_paths(folder_path):
    script = f'''
    set folderPath to "{folder_path}"
    set filePaths to {{}}

    tell application "Finder"
        set allItems to every file of (POSIX file folderPath as alias)
        repeat with anItem in allItems
            if not (name of anItem starts with ".") then
                set end of filePaths to (POSIX path of (anItem as alias))
            end if
        end repeat
    end tell

    set AppleScript's text item delimiters to (ASCII character 10)
    set pathList to filePaths as text
    set AppleScript's text item delimiters to ""

    return pathList
    '''
    result = run_applescript(script)
    return result.split('\n') if result else []


def get_file_paths(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: The path '{folder_path}' is not a valid directory.")
        return []

    try:
        file_paths = list_file_paths(folder_path)
        return [path for path in file_paths if path.strip()]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


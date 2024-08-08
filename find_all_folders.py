import os

def find_all_folders_in_folder(folder_path):
    all_folders = []

    try:
        for entry in os.listdir(folder_path):
            full_path = os.path.join(folder_path, entry)
            if os.path.isdir(full_path):
                all_folders.append((entry, full_path))

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

    print(all_folders)
    return all_folders


find_all_folders_in_folder(folder_path="/Users/shahir/Downloads")
import os

def find_all_files_in_folder(folder_path):
    all_files = []

    try:
        for file in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file)
            if os.path.isfile(full_path):
                all_files.append((file, full_path))

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

    print(all_files)
    return all_files


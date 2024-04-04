import os
import json
import shutil
import argparse

def rename_folders_and_json(folder_path, start_number):
    # Get list of folders
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    folders.sort(key=lambda x: int(x.split('_')[1]), reverse=True)  # Sort folders by the number in descending order
    num_folders = len(folders)

    # Iterate through each folder in reverse order
    for folder_name in folders:
        # Compute the new number
        i = start_number + num_folders - folders.index(folder_name)
        # Compute the new folder name
        new_folder_name = f"AG_{i}"

        # Create a new folder with the new name
        new_folder_path = os.path.join(folder_path, new_folder_name)
        os.makedirs(new_folder_path)

        # Copy contents of the old folder to the new one
        old_folder_path = os.path.join(folder_path, folder_name)
        for item in os.listdir(old_folder_path):
            item_path = os.path.join(old_folder_path, item)
            if os.path.isdir(item_path):
                shutil.copytree(item_path, os.path.join(new_folder_path, item))
            else:
                shutil.copy(item_path, new_folder_path)

        # Rename JSON file
        json_file_path = os.path.join(new_folder_path, f"{folder_name}.json")
        new_json_file_path = os.path.join(new_folder_path, f"{new_folder_name}.json")
        if os.path.exists(json_file_path):
            os.rename(json_file_path, new_json_file_path)

        # Update JSON content
        if os.path.exists(new_json_file_path):
            with open(new_json_file_path, 'r+') as json_file:
                data = json.load(json_file)
                new_data = {f"AG_{i}": v for k, v in data.items()}
                json_file.seek(0)
                json.dump(new_data, json_file, indent=4)
                json_file.truncate()

        # Remove the old folder
        shutil.rmtree(old_folder_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rename folders and JSON files.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing folders named like AG_247 to AG_296')
    parser.add_argument('start_number', type=int, help='The starting number for renaming folders')
    args = parser.parse_args()

    rename_folders_and_json(args.folder_path, args.start_number)


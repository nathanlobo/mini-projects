import os
import shutil
import re

# folder_path = input(r"Enter folder path:")
def rename_files(folder_path):
    search_text = input("Enter text to find:")
    new_text = input("Enter text to replace:")
    move_folder_path = input(r"Path to move file to if filename already exists or Type 'Skip':")
    try:
        # Iterate through all files in the specified directory
        for filename in os.listdir(folder_path):
            # Check if the file name contains the search text
            if search_text in filename:
                # Construct the new file name
                new_filename = filename.replace(search_text, new_text)
                # Get full paths
                old_file = os.path.join(folder_path, filename)
                new_file = os.path.join(folder_path, new_filename)
                try:
                    # Rename the file
                    os.rename(old_file, new_file)
                    print(f'Renamed: {filename} to {new_filename}')
                except OSError as e:
                    if e.winerror == 183:  # Error code for "Cannot create a file when that file already exists"
                        if move_folder_path != "Skip" or "skip":
                            # Rename the file
                            os.rename(old_file, new_file)
                            print(f'Renamed: {filename} to {new_filename}')
                            # Move the file to another location
                            destination = os.path.join(move_folder_path, filename)
                            shutil.move(old_file, destination)
                            print(f'Moved: {filename} to {move_folder_path}')
                        # else:
                        #     print(f'Error renaming {filename}: {e}')               
            else:
                print(f'Skipped: {filename}')
    except Exception as e:
        print(f'Error: {e}')
        # move_folder_path = input(r"Enter different folder path to move duplicates:")

def add_space_before_capital_letters(folder_path):
    for filename in os.listdir(folder_path):
        new_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', filename)
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_name)
        os.rename(old_file, new_file)
        print(f'Renamed: {old_file} -> {new_file}')

def add_space_before_character(folder_path, char):
    for filename in os.listdir(folder_path):
        new_name = filename.replace(char, ' ' + char)
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_name)
        os.rename(old_file, new_file)
        print(f'Renamed: {old_file} -> {new_file}')

char = '-'  # Character to add space before

# rename_files(folder_path)
# add_space_before_capital_letters(folder_path)
# add_space_before_character(folder_path, char)

tempVal = input("Hi there, These are the tasks I can do in a given folder\nEnter 1 to Find & Replace text in a file name of all files\nEnter 2 to Add space before capital letters in a file name of all files\nEnter 3 to Add space before a particular character in a file name of all files\n\tType here:")

folder_path = input(r"Enter folder path:")
if tempVal == '1':
    rename_files(folder_path)
elif tempVal == '2':
    add_space_before_capital_letters(folder_path)
elif tempVal == '3':
    add_space_before_character(folder_path, char)
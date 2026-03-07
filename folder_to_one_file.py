import os
import shutil

def move_all_files(src_folder, dest_folder):
    # Create destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_folder, file)
            # If file with same name exists, rename to avoid overwrite
            if os.path.exists(dest_file):
                base, ext = os.path.splitext(file)
                i = 1
                while os.path.exists(dest_file):
                    dest_file = os.path.join(dest_folder, f"{base}_{i}{ext}")
                    i += 1
            shutil.move(src_file, dest_file)
    print("All files moved successfully.")

move_all_files(r'C:\Users\nathan\HDD\All Audio\Music videos', r'C:\Users\nathan\HDD\All Audio\Music videos')
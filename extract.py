import zipfile
import tarfile
import py7zr
import os

# Extract ZIP
def extract_zip(zip_file_path, extract_to_folder):
    os.makedirs(extract_to_folder, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_folder)
        print(f"ZIP extraction complete. Files stored in: {extract_to_folder}")
        os.remove(zip_file_path)
        print(f"Deleted archive: {zip_file_path}")
    except Exception as e:
        print(f"⚠️ Failed to extract ZIP: {zip_file_path}\nError: {e}")

# Extract TAR
def extract_tar(tar_file_path, extract_to_folder):
    os.makedirs(extract_to_folder, exist_ok=True)
    try:
        with tarfile.open(tar_file_path, 'r') as tar_ref:
            tar_ref.extractall(extract_to_folder)
        print(f"TAR extraction complete. Files stored in: {extract_to_folder}")
        os.remove(tar_file_path)
        print(f"Deleted archive: {tar_file_path}")
    except Exception as e:
        print(f"⚠️ Failed to extract TAR: {tar_file_path}\nError: {e}")

# Extract 7Z
def extract_7z(sevenz_file_path, extract_to_folder):
    os.makedirs(extract_to_folder, exist_ok=True)
    try:
        with py7zr.SevenZipFile(sevenz_file_path, mode='r') as z:
            z.extractall(path=extract_to_folder)
        print(f"7Z extraction complete. Files stored in: {extract_to_folder}")
        os.remove(sevenz_file_path)
        print(f"Deleted archive: {sevenz_file_path}")
    except Exception as e:
        print(f"⚠️ Failed to extract 7Z: {sevenz_file_path}\nError: {e}")

# Auto detect and extract
def auto_extract(archive_path, extract_to_folder):
    ext = os.path.splitext(archive_path)[1].lower()
    if ext == '.zip':
        extract_zip(archive_path, extract_to_folder)
    elif ext in ['.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2']:
        extract_tar(archive_path, extract_to_folder)
    elif ext == '.7z':
        extract_7z(archive_path, extract_to_folder)
    else:
        print(f"⚠️ Unsupported file type: {ext}")

# Scan a folder and extract all supported archives
def extract_all_archives_in_folder(folder_path):
    supported_exts = ['.zip', '.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2', '.7z']
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            for ext in supported_exts:
                if filename.lower().endswith(ext):
                    # Create a subfolder for each archive
                    name_without_ext = os.path.splitext(filename)[0]
                    extract_to = os.path.join(folder_path, name_without_ext + '_extracted')
                    print(f"Extracting {filename} to {extract_to}")
                    auto_extract(file_path, extract_to)
                    break

# Example usage:
folder_to_scan = r'C:\Users\nathan\HDD\New folder'  # Change to your folder
extract_all_archives_in_folder(folder_to_scan)
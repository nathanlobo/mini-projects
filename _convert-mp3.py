import os

# This block handles both MoviePy v1.0 and v2.0+ automatically
try:
    from moviepy import AudioFileClip
except ImportError:
    try:
        from moviepy.editor import AudioFileClip
    except ImportError:
        print("MoviePy is not installed. Run: pip install moviepy")
        exit()

def convert_and_delete(directory_path):
    # Extensions to target
    target_extensions = ('.avi', '.mp4', '.flv', '.m4a', '.mpg')

    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return

    print(f"Scanning '{directory_path}' for files...")

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(target_extensions):
            
            file_path = os.path.join(directory_path, filename)
            output_filename = os.path.splitext(filename)[0] + '.mp3'
            output_path = os.path.join(directory_path, output_filename)

            print(f"Processing: {filename}")

            try:
                # 1. Convert the file
                clip = AudioFileClip(file_path)
                clip.write_audiofile(output_path, logger=None) 
                clip.close() # Crucial to close file before trying to delete it

                # 2. Safety Check & Delete
                if os.path.exists(output_path):
                    print(f" -> Conversion successful. Deleting original: {filename}")
                    os.remove(file_path)
                else:
                    print(f" -> Warning: MP3 file was not created. Keeping original: {filename}")

            except Exception as e:
                print(f" -> FAILED to convert {filename}. Error: {e}")

    print("\n--- Operation Completed ---")

# --- Usage ---
# Replace with your actual folder path
folder_to_convert = r"C:\Users\nathan\Music\christmas @lobo"

convert_and_delete(folder_to_convert)
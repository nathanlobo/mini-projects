import os,sys,subprocess
import random
import tkinter as tk
from tkinter import filedialog
from pygame import mixer

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Lobo Music Player")
        self.root.geometry("400x300")

        mixer.init()

        self.playlist = []
        self.current_index = 0
        self.paused = False
        self.shuffle = False
        self.replay_all = True
        self.replay_current = False

        self.load_button = tk.Button(root, text="Load Folder", command=self.load_folder)
        self.load_button.pack(pady=5)

        self.play_button = tk.Button(root, text="Play", command=self.play_music)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(root, text="Pause/Resume", command=self.pause_resume)
        self.pause_button.pack(pady=5)

        self.next_button = tk.Button(root, text="Next", command=self.next_song)
        self.next_button.pack(pady=5)

        self.prev_button = tk.Button(root, text="Previous", command=self.previous_song)
        self.prev_button.pack(pady=5)

        self.forward_button = tk.Button(root, text=">> Forward 10s", command=self.forward)
        self.forward_button.pack(pady=5)

        self.backward_button = tk.Button(root, text="<< Backward 10s", command=self.backward)
        self.backward_button.pack(pady=5)

        self.shuffle_button = tk.Button(root, text="Shuffle: OFF", command=self.toggle_shuffle)
        self.shuffle_button.pack(pady=5)

        self.replay_current_button = tk.Button(root, text="Replay Current: OFF", command=self.toggle_replay_current)
        self.replay_current_button.pack(pady=5)

        self.replay_all_button = tk.Button(root, text="Replay All: ON", command=self.toggle_replay_all)
        self.replay_all_button.pack(pady=5)

        self.root.after(1000, self.check_music_end)

    def load_folder(self):
        # folder = filedialog.askdirectory()
        folder = r"C:\Users\nathan\Music\Fav"
        if folder:
            self.playlist = [os.path.join(folder, f) for f in os.listdir(folder)
                             if f.lower().endswith(('.mp3', '.wav', '.ogg'))]
            self.current_index = 0
            # print("Playlist loaded:", self.playlist)

    def play_music(self):
        app = MusicPlayer(root)
        app.load_folder()
        if self.paused:
            mixer.music.unpause()
            self.paused = False
            return
        if not self.playlist:
            return
        mixer.music.load(self.playlist[self.current_index])
        mixer.music.play()
        self.paused = False

    def pause_resume(self):
        if not mixer.music.get_busy() and not self.paused:
            return
        if self.paused:
            mixer.music.unpause()
            self.paused = False
        else:
            mixer.music.pause()
            self.paused = True

    def next_song(self):
        if self.shuffle:
            self.current_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_music()

    def previous_song(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_music()

    def forward(self, seconds=30):
        if not self.playlist:
            return

        try:
            pos = mixer.music.get_pos() / 1000.0  # current position in seconds
            new_pos = pos + seconds

            mixer.music.stop()
            mixer.music.load(self.playlist[self.current_index])
            mixer.music.play(start=new_pos)
            self.paused = False
        except Exception as e:
            print("Forward error:", e)

    def backward(self, seconds=30):
        if not self.playlist:
            return

        try:
            pos = mixer.music.get_pos() / 1000.0
            new_pos = max(0, pos - seconds)

            mixer.music.stop()
            mixer.music.load(self.playlist[self.current_index])
            mixer.music.play(start=new_pos)
            self.paused = False
        except Exception as e:
            print("Backward error:", e)


    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        self.shuffle_button.config(text=f"Shuffle: {'ON' if self.shuffle else 'OFF'}")

    def toggle_replay_current(self):
        self.replay_current = not self.replay_current
        self.replay_current_button.config(text=f"Replay Current: {'ON' if self.replay_current else 'OFF'}")

    def toggle_replay_all(self):
        self.replay_all = not self.replay_all
        self.replay_all_button.config(text=f"Replay All: {'ON' if self.replay_all else 'OFF'}")

    def check_music_end(self):
        if not mixer.music.get_busy() and not self.paused:
            if self.replay_current:
                self.play_music()
            elif self.replay_all or self.shuffle:
                self.next_song()
        self.root.after(1000, self.check_music_end)

    @staticmethod
    def restartProgram():
        try:
            python = sys.executable
            script_path = os.path.abspath(sys.argv[0])
            if not os.path.isfile(script_path):
                raise FileNotFoundError(f"Script not found at {script_path}")
            subprocess.call([python, script_path] + sys.argv[1:])
            sys.exit()  # Exit the current script after restart
        except Exception as e:
            print(f"Error restarting the program: {e}")


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = MusicPlayer(root)
        root.mainloop()
    except KeyboardInterrupt:
        app.restartProgram()
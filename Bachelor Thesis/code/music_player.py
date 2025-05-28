#Install dependencies:
#pip install python-vlc tkinter

import tkinter as tk
from tkinter import ttk, filedialog
import vlc
import os
import time
from threading import Thread
from pathlib import Path

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Therapy Music Player")
        self.root.geometry("800x600")
        
        # VLC Initialization
        self.instance = vlc.Instance('--no-xlib')
        self.player = self.instance.media_player_new()
        self.current_media = None
        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.volume = 50
        
        # GUI Setup
        self.create_widgets()
        self.setup_bindings()
        
        # Start progress updater
        self.update_progress()

    def create_widgets(self):
        # Playlist Frame
        playlist_frame = ttk.LabelFrame(self.root, text="Playlist")
        playlist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.playlist_box = tk.Listbox(playlist_frame, selectmode=tk.SINGLE)
        self.playlist_box.pack(fill=tk.BOTH, expand=True)
        
        # Controls Frame
        controls_frame = ttk.Frame(self.root)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.play_btn = ttk.Button(controls_frame, text="Play", command=self.toggle_playback)
        self.stop_btn = ttk.Button(controls_frame, text="Stop", command=self.stop)
        self.prev_btn = ttk.Button(controls_frame, text="Previous", command=self.prev_track)
        self.next_btn = ttk.Button(controls_frame, text="Next", command=self.next_track)
        self.add_btn = ttk.Button(controls_frame, text="Add Folder", command=self.add_folder)
        
        self.play_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        self.add_btn.pack(side=tk.RIGHT, padx=5)
        
        # Progress Slider
        self.progress_slider = ttk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL)
        self.progress_slider.pack(fill=tk.X, padx=10, pady=5)
        
        # Volume Control
        volume_frame = ttk.Frame(self.root)
        volume_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.volume_slider = ttk.Scale(
            volume_frame, from_=0, to=100, 
            orient=tk.HORIZONTAL, command=self.set_volume
        )
        self.volume_slider.set(self.volume)
        self.volume_slider.pack(side=tk.RIGHT, padx=5)
        ttk.Label(volume_frame, text="Volume:").pack(side=tk.RIGHT)

    def setup_bindings(self):
        self.playlist_box.bind("<Double-Button-1>", self.play_selected)
        self.progress_slider.bind("<ButtonPress-1>", self.slider_press)
        self.progress_slider.bind("<ButtonRelease-1>", self.slider_release)

    def add_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.playlist = []
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(('.mp3', '.wav', '.flac', '.m4a')):
                        self.playlist.append(os.path.join(root, file))
            self.update_playlist_display()
            if self.playlist:
                self.current_index = 0
                self.load_track(self.playlist[self.current_index])

    def update_playlist_display(self):
        self.playlist_box.delete(0, tk.END)
        for track in self.playlist:
            self.playlist_box.insert(tk.END, os.path.basename(track))

    def load_track(self, file_path):
        self.current_media = self.instance.media_new(file_path)
        self.player.set_media(self.current_media)
        self.set_volume(self.volume)
        self.player.play()
        self.is_playing = True
        self.update_button_states()

    def toggle_playback(self):
        if self.player.get_media():
            if self.is_playing:
                self.player.pause()
            else:
                self.player.play()
            self.is_playing = not self.is_playing
            self.update_button_states()

    def stop(self):
        self.player.stop()
        self.is_playing = False
        self.update_button_states()

    def next_track(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.load_track(self.playlist[self.current_index])

    def prev_track(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.load_track(self.playlist[self.current_index])

    def play_selected(self, event):
        selection = self.playlist_box.curselection()
        if selection:
            self.current_index = selection[0]
            self.load_track(self.playlist[self.current_index])

    def set_volume(self, value):
        self.volume = float(value)
        self.player.audio_set_volume(int(self.volume))

    def update_progress(self):
        if self.player.get_media():
            media_length = self.player.get_length()
            if media_length > 0:
                current_time = self.player.get_time()
                self.progress_slider.config(to=media_length)
                self.progress_slider.set(current_time)
        self.root.after(500, self.update_progress)

    def slider_press(self, event):
        self.player.pause()

    def slider_release(self, event):
        if self.player.get_media():
            new_time = int(self.progress_slider.get())
            self.player.set_time(new_time)
            self.player.play()

    def update_button_states(self):
        self.play_btn.config(text="Pause" if self.is_playing else "Play")
        self.stop_btn.config(state=tk.NORMAL if self.player.get_media() else tk.DISABLED)
        self.prev_btn.config(state=tk.NORMAL if len(self.playlist) > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if len(self.playlist) > 0 else tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk
from music_player import MusicPlayer
from virtual_therapist import TherapistGUI

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automated Therapy System")
        self.geometry("1200x800")
        self.configure(bg='#f0f0f0')
        
        # Configure notebook for tabbed interface
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Music Player Tab
        self.music_frame = ttk.Frame(self.notebook)
        self.music_player = MusicPlayer(self.music_frame)
        self.music_player.pack(fill=tk.BOTH, expand=True)
        
        # Virtual Therapist Tab
        self.therapist_frame = ttk.Frame(self.notebook)
        self.therapist_gui = TherapistGUI(self.therapist_frame)
        self.therapist_gui.pack(fill=tk.BOTH, expand=True)

        # Add tabs to notebook
        self.notebook.add(self.music_frame, text="Music Therapy")
        self.notebook.add(self.therapist_frame, text="Virtual Therapist")

        # Setup window closing protocol
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Cleanup resources before closing"""
        if hasattr(self.music_player, 'audio_processor'):
            self.music_player.audio_processor.release()
        self.destroy()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

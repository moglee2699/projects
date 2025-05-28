import vlc
import os
import time
from threading import Thread
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

class AudioProcessor:
    def __init__(self):
        self.instance = vlc.Instance('--no-xlib')
        self.player = self.instance.media_player_new()
        self.current_media = None
        self.is_playing = False
        self.volume = 50
        self.duration = 0
        self._progress_thread = None
        self._stop_flag = False

    def load_media(self, file_path):
        """Load audio file into VLC player with error handling"""
        try:
            self.current_media = self.instance.media_new(file_path)
            self.player.set_media(self.current_media)
            self._get_duration(file_path)
            return True
        except Exception as e:
            print(f"Error loading media: {str(e)}")
            return False

    def _get_duration(self, file_path):
        """Get accurate duration using Mutagen as fallback"""
        try:
            if file_path.endswith('.mp3'):
                audio = MP3(file_path)
            elif file_path.endswith('.m4a'):
                audio = MP4(file_path)
            else:
                audio = None
            
            self.duration = audio.info.length if audio else self.player.get_length()/1000
        except Exception:
            self.duration = self.player.get_length()/1000

    def play(self):
        """Start or resume playback"""
        if self.player.get_media():
            self.player.play()
            self.is_playing = True
            self._start_progress_thread()

    def pause(self):
        """Pause playback"""
        if self.player.get_media():
            self.player.pause()
            self.is_playing = False

    def stop(self):
        """Stop playback and reset position"""
        if self.player.get_media():
            self.player.stop()
            self.is_playing = False
            self._stop_progress_thread()

    def set_volume(self, volume):
        """Set playback volume (0-100)"""
        self.volume = max(0, min(100, volume))
        self.player.audio_set_volume(int(self.volume))

    def get_current_time(self):
        """Get current playback position in seconds"""
        return self.player.get_time()/1000 if self.player.get_media() else 0

    def seek(self, position):
        """Seek to specific position in seconds"""
        if self.player.get_media():
            self.player.set_time(int(position * 1000))

    def _start_progress_thread(self):
        """Start thread for tracking playback progress"""
        self._stop_flag = False
        if not self._progress_thread or not self._progress_thread.is_alive():
            self._progress_thread = Thread(target=self._update_progress)
            self._progress_thread.start()

    def _stop_progress_thread(self):
        """Signal progress thread to stop"""
        self._stop_flag = True

    def _update_progress(self):
        """Internal method for tracking playback progress"""
        while not self._stop_flag and self.is_playing:
            time.sleep(0.5)
            if not self.player.is_playing():
                self.is_playing = False
                break

    def release(self):
        """Clean up VLC resources"""
        self.stop()
        self.player.release()
        self.instance.release()

if __name__ == "__main__":
    # Example usage
    processor = AudioProcessor()
    processor.load_media("assets/sounds/nature/rain.mp3")
    processor.play()
    processor.set_volume(75)
    
    try:
        while processor.is_playing:
            print(f"Current Time: {processor.get_current_time():.2f}/{processor.duration:.2f}")
            time.sleep(1)
    except KeyboardInterrupt:
        processor.stop()
        processor.release()

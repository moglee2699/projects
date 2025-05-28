import numpy as np
import soundfile as sf
import os
from pathlib import Path

class SoundGenerator:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.sounds_dir = Path("assets/sounds")
        self.sounds_dir.mkdir(parents=True, exist_ok=True)

    def generate_binaural_beat(self, base_freq, delta_freq, duration, volume=0.5):
        """Generate binaural beat audio file"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        
        left_channel = np.sin(2 * np.pi * base_freq * t)
        right_channel = np.sin(2 * np.pi * (base_freq + delta_freq) * t)
        
        stereo_sound = np.vstack([left_channel, right_channel]).T
        stereo_sound *= volume
        return stereo_sound

    def generate_nature_sound(self, freq_range, duration, volume=0.3):
        """Generate nature-like ambient sound"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        noise = np.random.normal(0, 0.5, len(t))
        
        # Apply bandpass filter
        low = freq_range[0] / (self.sample_rate / 2)
        high = freq_range[1] / (self.sample_rate / 2)
        b, a = signal.butter(4, [low, high], btype='band')
        filtered = signal.lfilter(b, a, noise)
        
        return filtered * volume

    def generate_isochronic_tone(self, freq, beat_freq, duration, volume=0.4):
        """Generate isochronic tone pattern"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        carrier = np.sin(2 * np.pi * freq * t)
        
        # Create amplitude modulation
        modulator = np.sin(np.pi * beat_freq * t)
        modulated = carrier * (1 + modulator) * 0.5
        
        return modulated * volume

    def save_sound(self, sound_array, filename, subtype='PCM_16'):
        """Save generated sound to WAV file"""
        filepath = self.sounds_dir / filename
        sf.write(filepath, sound_array, self.sample_rate, subtype=subtype)
        return filepath

# Example usage
if __name__ == "__main__":
    sg = SoundGenerator()
    
    # Generate alpha wave binaural beat (10Hz difference)
    alpha_beat = sg.generate_binaural_beat(200, 10, duration=600)  # 10 minutes
    sg.save_sound(alpha_beat, "alpha_binaural.wav")
    
    # Generate rain-like nature sound
    rain_sound = sg.generate_nature_sound((1000, 5000), duration=600)
    sg.save_sound(rain_sound, "rain_ambience.wav")
    
    # Generate theta wave isochronic tone
    theta_tone = sg.generate_isochronic_tone(150, 5, duration=600)
    sg.save_sound(theta_tone, "theta_isochronic.wav")

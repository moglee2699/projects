from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk

class ImageManager:
    def __init__(self, theme='light'):
        self.images = {}
        self.theme = theme
        self.image_dir = Path('assets/images')
        self.load_core_images()
        
    def load_core_images(self):
        """Load essential UI images with theme support"""
        image_specs = {
            'play': {'size': (32, 32)},
            'pause': {'size': (32, 32)},
            'stop': {'size': (32, 32)},
            'next': {'size': (24, 24)},
            'previous': {'size': (24, 24)},
            'logo': {'size': (128, 128)}
        }
        
        for img_name, specs in image_specs.items():
            self.load_image(
                name=img_name,
                filename=f"{img_name}_{self.theme}.png",
                size=specs['size']
            )

    def load_image(self, name, filename, size=None):
        """Load and resize an image with anti-aliasing"""
        try:
            img_path = self.image_dir / filename
            pil_img = Image.open(img_path)
            
            if size:
                pil_img = pil_img.resize(size, Image.LANCZOS)
                
            self.images[name] = ImageTk.PhotoImage(pil_img)
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
            # Fallback to default image
            self.images[name] = tk.PhotoImage()

    def get_image(self, name):
        """Retrieve loaded image by name"""
        return self.images.get(name, tk.PhotoImage())

    def set_theme(self, new_theme):
        """Update theme and reload images"""
        if new_theme != self.theme:
            self.theme = new_theme
            self.load_core_images()

# Usage Example
if __name__ == "__main__":
    root = tk.Tk()
    img_manager = ImageManager(theme='light')
    
    # Create toolbar buttons
    toolbar = tk.Frame(root)
    toolbar.pack(pady=10)
    
    buttons = [
        ('previous', 'Previous Track'),
        ('play', 'Play/Pause'),
        ('next', 'Next Track'),
        ('stop', 'Stop')
    ]
    
    for btn_name, tooltip in buttons:
        btn = tk.Button(
            toolbar,
            image=img_manager.get_image(btn_name),
            command=lambda n=btn_name: print(f"{n} clicked")
        )
        btn.pack(side=tk.LEFT, padx=5)
    
    # Display logo
    logo_label = tk.Label(root, image=img_manager.get_image('logo'))
    logo_label.pack(pady=20)
    
    root.mainloop()

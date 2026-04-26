from PIL import Image
import numpy as np
import shutil

def rgb_to_ansi(r, g, b):
    """Convert RGB to ANSI escape code"""
    return f'\x1b[38;2;{r};{g};{b}m'

def get_brightness(r, g, b):
    """Calculate perceived brightness of RGB color"""
    # Using luminance formula
    return 0.299 * r + 0.587 * g + 0.114 * b

def brightness_to_char(brightness):
    """Convert brightness (0-255) to ASCII character"""
    # More density levels for better quality
    # From darkest to lightest
    chars = " .:-=+*#%@█"
    # Alternative block characters for smoother gradients
    # chars = " ░▒▓█"
    
    # Use full blocks with color for maximum detail
    chars = "█"
    
    index = int(brightness / 255 * (len(chars) - 1))
    return chars[index]

def image_to_ascii(image_path, output_path, width=120):
    """Convert image to colored ASCII art using box-drawing characters"""
    
    print(f"Converting {image_path} to ASCII art...")
    
    # Load image
    img = Image.open(image_path)
    
    # Calculate height maintaining aspect ratio
    # Characters are roughly 2:1 (height:width), so adjust
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.5)
    
    print(f"Resizing to {width}x{height}...")
    
    # Resize with high quality
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    img = img.convert('RGB')
    
    # Get pixel data
    pixels = np.array(img)
    
    # Build ASCII art
    ascii_art = []
    
    for y in range(height):
        line_chars = []
        for x in range(width):
            r, g, b = pixels[y, x]
            
            # Get color code
            color_code = rgb_to_ansi(r, g, b)
            
            # Use full block with color for maximum quality
            char = '█'
            
            # Add colored character with reset
            line_chars.append(f"{color_code}{char}\x1b[0m")
        
        ascii_art.append(''.join(line_chars))
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in ascii_art:
            f.write(line + '\n')
    
    print(f"✅ Converted image to ASCII art")
    print(f"   Dimensions: {width} x {height}")
    print(f"   Saved to: {output_path}")
    
    return width, height

if __name__ == "__main__":
    # Backup current portrait
    print("Creating backup of current portrait...")
    shutil.copy("dilpriya_braille.txt", "dilpriya_braille_backup_ascii.txt")
    print("✅ Backup saved to: dilpriya_braille_backup_ascii.txt")
    
    # Convert image - try 120 width for more detail
    print("\n" + "="*60)
    width, height = image_to_ascii("dilpriya-2.jpeg", "dilpriya_braille.txt", width=120)
    
    print("\n" + "="*60)
    print("Image conversion complete!")
    print("Run 'python -m hdm_optimizer --version' to see the result")
    print("To restore Braille version: Copy-Item dilpriya_braille_backup_ascii.txt dilpriya_braille.txt -Force")
    print("="*60)

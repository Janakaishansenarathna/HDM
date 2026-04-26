from PIL import Image
import numpy as np
import shutil

def rgb_to_ansi(r, g, b):
    """Convert RGB to ANSI escape code"""
    return f'\x1b[38;2;{r};{g};{b}m'

def get_brightness(r, g, b):
    """Calculate perceived brightness of RGB color (0-255)"""
    return 0.299 * r + 0.587 * g + 0.114 * b

def brightness_to_char(brightness):
    """Convert brightness to gradient character for more detail"""
    # Progressive density characters from dark to light
    # More levels = more detail in same space
    chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    
    # Alternative: Unicode block elements for smoother gradients
    # chars = " ░▒▓█"
    
    # Best for colored output: Use blocks with varying density
    chars = " .:-=+*#%@█"
    
    index = int(brightness / 255 * (len(chars) - 1))
    return chars[min(index, len(chars) - 1)]

def image_to_gradient_ascii(image_path, output_path, width=120):
    """Convert image to colored gradient ASCII art"""
    
    print(f"Converting {image_path} to gradient ASCII art...")
    
    # Load image
    img = Image.open(image_path)
    
    # Calculate height maintaining aspect ratio
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
            
            # Calculate brightness for character selection
            brightness = get_brightness(r, g, b)
            
            # Select character based on brightness
            char = brightness_to_char(brightness)
            
            # Get color code
            color_code = rgb_to_ansi(r, g, b)
            
            # Add colored character with reset
            line_chars.append(f"{color_code}{char}\x1b[0m")
        
        ascii_art.append(''.join(line_chars))
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in ascii_art:
            f.write(line + '\n')
    
    print(f"✅ Converted image to gradient ASCII art")
    print(f"   Dimensions: {width} x {height}")
    print(f"   Using brightness-based character selection for detail")
    print(f"   Saved to: {output_path}")
    
    return width, height

if __name__ == "__main__":
    # Backup current portrait
    print("Creating backup of current portrait...")
    shutil.copy("dilpriya_braille.txt", "dilpriya_braille_backup_gradient.txt")
    print("✅ Backup saved to: dilpriya_braille_backup_gradient.txt")
    
    # Convert image with gradient characters
    print("\n" + "="*60)
    width, height = image_to_gradient_ascii("dilpriya-2.jpeg", "dilpriya_braille.txt", width=120)
    
    print("\n" + "="*60)
    print("Image conversion complete!")
    print("Gradient characters provide more detail through shading")
    print("Run 'python -m hdm_optimizer --version' to see the result")
    print("To restore previous: Copy-Item dilpriya_braille_backup_gradient.txt dilpriya_braille.txt -Force")
    print("="*60)

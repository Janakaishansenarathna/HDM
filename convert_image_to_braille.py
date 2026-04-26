from PIL import Image
import numpy as np

def rgb_to_ansi(r, g, b):
    """Convert RGB to ANSI escape code"""
    return f'\x1b[38;2;{r};{g};{b}m'

def image_to_braille(image_path, output_path, width=60):
    """Convert image to colored Braille art with enhanced quality"""
    from PIL import ImageEnhance, ImageFilter
    
    # Load image
    img = Image.open(image_path)
    
    # Calculate height to maintain aspect ratio
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.5)  # 0.5 factor for character aspect ratio
    
    # Enhanced quality processing:
    # 1. First upscale if needed for better downsampling
    if img.width < width * 4 or img.height < height * 4:
        upscale = 3
        img = img.resize((img.width * upscale, img.height * upscale), Image.Resampling.LANCZOS)
    
    # 2. Apply subtle sharpening for better detail
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.4)
    
    # 3. Enhance contrast slightly for better color definition
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(1.1)
    
    # 4. Final high-quality resize
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    img = img.convert('RGB')
    
    # Get pixel data
    pixels = np.array(img)
    
    # Braille block character
    braille_char = '⣿'
    
    # Create Braille art with colors
    braille_lines = []
    for y in range(height):
        line_chars = []
        for x in range(width):
            r, g, b = pixels[y, x]
            color_code = rgb_to_ansi(r, g, b)
            line_chars.append(f"{color_code}{braille_char}\x1b[0m")
        braille_lines.append(''.join(line_chars))
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(braille_lines))
    
    print(f"✅ Converted image to Braille art")
    print(f"   Dimensions: {width} x {height}")
    print(f"   Saved to: {output_path}")
    return width, height

if __name__ == "__main__":
    # Backup current portrait
    import shutil
    print("Creating backup of current portrait...")
    shutil.copy("dilpriya_braille.txt", "dilpriya_braille_backup_original.txt")
    print("✅ Backup saved to: dilpriya_braille_backup_original.txt")
    
    # Convert new image
    print("\nConverting dilpriya-2.jpeg to Braille art...")
    width, height = image_to_braille("dilpriya-2.jpeg", "dilpriya_braille.txt", width=60)
    
    print("\n" + "="*60)
    print("Image conversion complete!")
    print("Run 'python -m hdm_optimizer --version' to see the result")
    print("To restore original: Copy-Item dilpriya_braille_backup_original.txt dilpriya_braille.txt -Force")
    print("="*60)

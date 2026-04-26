from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

def rgb_to_ansi(r, g, b):
    """Convert RGB to ANSI escape code"""
    return f'\x1b[38;2;{r};{g};{b}m'

def get_brightness(r, g, b):
    """Calculate perceived brightness using luminance formula"""
    return 0.299 * r + 0.587 * g + 0.114 * b

def brightness_to_block_char(brightness):
    """Convert brightness to block character for more detail"""
    # Unicode block elements from dark to light
    # More levels = more detail and smoother gradients
    chars = " ░▒▓█"
    
    # Alternative: More detailed ASCII blocks
    # chars = " .·:░▒▓█"
    
    index = int(brightness / 255 * (len(chars) - 1))
    return chars[min(index, len(chars) - 1)]

def apply_unsharp_mask(img, radius=2, percent=150, threshold=3):
    """Apply unsharp mask for edge enhancement"""
    blurred = img.filter(ImageFilter.GaussianBlur(radius))
    img_array = np.array(img, dtype=np.float32)
    blurred_array = np.array(blurred, dtype=np.float32)
    
    diff = img_array - blurred_array
    diff = np.where(np.abs(diff) < threshold, 0, diff)
    sharpened = img_array + (diff * percent / 100.0)
    sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
    
    return Image.fromarray(sharpened)

def image_to_artbox_enhanced(image_path, output_path, width=60):
    """Convert image to colored ASCII art using box-drawing characters with maximum quality"""
    
    print(f"Converting {image_path} to enhanced ASCII art box-drawing...")
    
    # Load image
    img = Image.open(image_path)
    
    # Calculate target dimensions
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.5)
    
    print("Step 1/6: Super-resolution upscaling...")
    # Super-sampling: upscale significantly first
    if img.width < width * 5 or img.height < height * 5:
        upscale = 4
        img = img.resize((img.width * upscale, img.height * upscale), Image.Resampling.LANCZOS)
    
    img = img.convert('RGB')
    
    print("Step 2/6: Noise reduction...")
    img = img.filter(ImageFilter.MedianFilter(size=3))
    
    print("Step 3/6: Color and contrast optimization...")
    # Enhance color saturation
    color_enhancer = ImageEnhance.Color(img)
    img = color_enhancer.enhance(1.25)
    
    # Strong contrast for better block definition
    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(1.2)
    
    # Brightness adjustment
    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(1.05)
    
    print("Step 4/6: Edge enhancement...")
    img = apply_unsharp_mask(img, radius=2, percent=200, threshold=2)
    
    print("Step 5/6: High-quality downsampling...")
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    print("Step 6/6: Final sharpening...")
    sharpener = ImageEnhance.Sharpness(img)
    img = sharpener.enhance(1.4)
    
    # Get pixel data
    pixels = np.array(img)
    
    # Create ASCII art with colored blocks
    ascii_lines = []
    for y in range(height):
        line_chars = []
        for x in range(width):
            r, g, b = pixels[y, x]
            
            # Calculate brightness for character selection
            brightness = get_brightness(r, g, b)
            
            # Select block character based on brightness
            char = brightness_to_block_char(brightness)
            
            # Get color code
            color_code = rgb_to_ansi(r, g, b)
            
            # Add colored character with reset
            line_chars.append(f"{color_code}{char}\x1b[0m")
        
        ascii_lines.append(''.join(line_chars))
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ascii_lines))
    
    print(f"✅ Enhanced ASCII art box-drawing conversion complete!")
    print(f"   Dimensions: {width} x {height}")
    print(f"   Style: Block characters (░▒▓█) with full RGB colors")
    print(f"   Saved to: {output_path}")
    return width, height

if __name__ == "__main__":
    import shutil
    
    # Backup current portrait
    print("Creating backup of current portrait...")
    shutil.copy("dilpriya_braille.txt", "dilpriya_braille_backup_artbox.txt")
    print("✅ Backup saved to: dilpriya_braille_backup_artbox.txt")
    
    # Convert with artbox method
    print("\n" + "="*60)
    width, height = image_to_artbox_enhanced("dilpriya-2.jpeg", "dilpriya_braille.txt", width=60)
    
    print("\n" + "="*60)
    print("ASCII Art Box-Drawing conversion complete!")
    print("Method: Block characters based on brightness levels")
    print("Characters used: ░ (light) → ▒ → ▓ → █ (solid)")
    print("Quality enhancements:")
    print("  • 4x super-sampling")
    print("  • Color saturation +25%")
    print("  • High contrast +20%")
    print("  • Custom unsharp mask (200%)")
    print("  • Edge-preserving noise reduction")
    print("\nRun 'python -m hdm_optimizer --version' to see the result")
    print("To restore previous: Copy-Item dilpriya_braille_backup_artbox.txt dilpriya_braille.txt -Force")
    print("="*60)

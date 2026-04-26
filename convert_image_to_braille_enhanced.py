from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

def rgb_to_ansi(r, g, b):
    """Convert RGB to ANSI escape code"""
    return f'\x1b[38;2;{r};{g};{b}m'

def apply_unsharp_mask(img, radius=2, percent=150, threshold=3):
    """Apply unsharp mask for edge enhancement"""
    blurred = img.filter(ImageFilter.GaussianBlur(radius))
    img_array = np.array(img, dtype=np.float32)
    blurred_array = np.array(blurred, dtype=np.float32)
    
    # Calculate difference
    diff = img_array - blurred_array
    
    # Apply threshold
    diff = np.where(np.abs(diff) < threshold, 0, diff)
    
    # Sharpen
    sharpened = img_array + (diff * percent / 100.0)
    sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
    
    return Image.fromarray(sharpened)

def image_to_braille_enhanced(image_path, output_path, width=60):
    """Convert image to colored Braille art with maximum quality enhancement"""
    
    print(f"Converting {image_path} to enhanced Braille art...")
    
    # Load image
    img = Image.open(image_path)
    original_format = img.format
    
    # Calculate target dimensions
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.5)
    
    print("Step 1/6: Initial upscaling...")
    # Super-resolution approach: upscale significantly first
    if img.width < width * 5 or img.height < height * 5:
        upscale = 4
        img = img.resize((img.width * upscale, img.height * upscale), Image.Resampling.LANCZOS)
    
    # Convert to RGB early for consistent processing
    img = img.convert('RGB')
    
    print("Step 2/6: Noise reduction while preserving edges...")
    # Bilateral-like filtering: reduce noise but keep edges
    img = img.filter(ImageFilter.MedianFilter(size=3))
    
    print("Step 3/6: Color and contrast optimization...")
    # Enhance color saturation for more vivid colors
    color_enhancer = ImageEnhance.Color(img)
    img = color_enhancer.enhance(1.2)
    
    # Adaptive contrast enhancement
    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(1.15)
    
    # Brightness adjustment for better visibility
    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(1.05)
    
    print("Step 4/6: Edge enhancement with unsharp mask...")
    # Apply custom unsharp mask for crisp edges
    img = apply_unsharp_mask(img, radius=2, percent=180, threshold=2)
    
    print("Step 5/6: High-quality downsampling...")
    # Final resize with maximum quality
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    print("Step 6/6: Final sharpening pass...")
    # Final subtle sharpening after resize
    sharpener = ImageEnhance.Sharpness(img)
    img = sharpener.enhance(1.3)
    
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
    
    print(f"✅ Enhanced conversion complete!")
    print(f"   Dimensions: {width} x {height}")
    print(f"   Applied: Super-sampling, Edge enhancement, Color optimization")
    print(f"   Saved to: {output_path}")
    return width, height

if __name__ == "__main__":
    import shutil
    
    # Backup current portrait
    print("Creating backup of current portrait...")
    shutil.copy("dilpriya_braille.txt", "dilpriya_braille_backup_enhanced.txt")
    print("✅ Backup saved to: dilpriya_braille_backup_enhanced.txt")
    
    # Convert with maximum enhancement
    print("\n" + "="*60)
    width, height = image_to_braille_enhanced("dilpriya-2.jpeg", "dilpriya_braille.txt", width=60)
    
    print("\n" + "="*60)
    print("Enhanced image conversion complete!")
    print("Quality improvements applied:")
    print("  • 4x upscaling for super-sampling")
    print("  • Noise reduction with edge preservation")
    print("  • Color saturation boost (+20%)")
    print("  • Adaptive contrast enhancement (+15%)")
    print("  • Custom unsharp mask for crisp edges")
    print("  • Multi-pass sharpening")
    print("\nRun 'python -m hdm_optimizer --version' to see the result")
    print("To restore previous: Copy-Item dilpriya_braille_backup_enhanced.txt dilpriya_braille.txt -Force")
    print("="*60)

"""Ultra high-quality ASCII art using Braille characters for maximum resolution."""
from PIL import Image, ImageEnhance, ImageFilter

def rgb_to_ansi(r, g, b):
    """Convert RGB to ANSI 24-bit color code."""
    return f"\033[38;2;{r};{g};{b}m"

def image_to_braille(image_path, width=120):
    """
    Convert image to Braille characters for 4x resolution.
    Each Braille character represents 2x4 pixels = 8 pixels.
    """
    # Braille Unicode: U+2800 to U+28FF
    # Each dot can be on/off based on pixel brightness
    
    # Open and enhance image
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    # Apply heavy enhancement for maximum detail
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(3.0)
    
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    # Calculate height (4x vertical resolution with Braille)
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 4)
    
    # Make height multiple of 4 for Braille blocks
    height = (height // 4) * 4
    
    # Resize with LANCZOS
    img = img.resize((width * 2, height), Image.Resampling.LANCZOS)
    
    # Convert to grayscale for pattern detection
    gray = img.convert('L')
    pixels = list(img.getdata())
    gray_pixels = list(gray.getdata())
    
    # Build Braille ASCII art
    ascii_lines = []
    reset = "\033[0m"
    
    # Braille dot positions
    # 1 4
    # 2 5
    # 3 6
    # 7 8
    
    for row in range(0, height, 4):
        line = ""
        for col in range(0, width * 2, 2):
            # Get 2x4 block of pixels
            dots = []
            colors = []
            
            for dy in range(4):
                for dx in range(2):
                    idx = (row + dy) * (width * 2) + (col + dx)
                    if idx < len(gray_pixels):
                        brightness = gray_pixels[idx]
                        dots.append(1 if brightness > 128 else 0)
                        colors.append(pixels[idx])
                    else:
                        dots.append(0)
                        colors.append((0, 0, 0))
            
            # Calculate Braille character
            # Braille pattern: bits 0-7 map to dots
            braille_base = 0x2800
            if len(dots) >= 8:
                braille = braille_base
                if dots[0]: braille |= 0x01  # dot 1
                if dots[2]: braille |= 0x02  # dot 2
                if dots[4]: braille |= 0x04  # dot 3
                if dots[6]: braille |= 0x08  # dot 7
                if dots[1]: braille |= 0x10  # dot 4
                if dots[3]: braille |= 0x20  # dot 5
                if dots[5]: braille |= 0x40  # dot 6
                if dots[7]: braille |= 0x80  # dot 8
                
                # Use average color of the block
                avg_r = sum(c[0] for c in colors) // len(colors)
                avg_g = sum(c[1] for c in colors) // len(colors)
                avg_b = sum(c[2] for c in colors) // len(colors)
                
                color = rgb_to_ansi(avg_r, avg_g, avg_b)
                line += f"{color}{chr(braille)}{reset}"
            else:
                line += " "
        
        ascii_lines.append(line)
    
    return "\n".join(ascii_lines)

def image_to_tiny_blocks(image_path, width=150):
    """
    Use tiny block characters for super high detail.
    """
    # Tiny blocks: ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█
    blocks = {
        (0, 0, 0, 0): ' ',
        (0, 0, 0, 1): '▗',
        (0, 0, 1, 0): '▖',
        (0, 0, 1, 1): '▄',
        (0, 1, 0, 0): '▝',
        (0, 1, 0, 1): '▐',
        (0, 1, 1, 0): '▞',
        (0, 1, 1, 1): '▟',
        (1, 0, 0, 0): '▘',
        (1, 0, 0, 1): '▚',
        (1, 0, 1, 0): '▌',
        (1, 0, 1, 1): '▙',
        (1, 1, 0, 0): '▀',
        (1, 1, 0, 1): '▜',
        (1, 1, 1, 0): '▛',
        (1, 1, 1, 1): '█',
    }
    
    # Open and enhance
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    # Apply extreme enhancements for ultra clarity
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(4.5)  # Maximum sharpness
    
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)  # Maximum contrast
    
    # Apply multiple edge enhancements
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    img = img.filter(ImageFilter.SHARPEN)
    img = img.filter(ImageFilter.DETAIL)
    
    # Calculate height (2x2 blocks)
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 2)
    height = (height // 2) * 2
    
    # Resize
    img = img.resize((width * 2, height), Image.Resampling.LANCZOS)
    
    gray = img.convert('L')
    pixels = list(img.getdata())
    gray_pixels = list(gray.getdata())
    
    # Build ASCII art
    ascii_lines = []
    reset = "\033[0m"
    
    for row in range(0, height, 2):
        line = ""
        for col in range(0, width * 2, 2):
            # Get 2x2 block
            dots = []
            colors = []
            
            for dy in range(2):
                for dx in range(2):
                    idx = (row + dy) * (width * 2) + (col + dx)
                    if idx < len(gray_pixels):
                        brightness = gray_pixels[idx]
                        dots.append(1 if brightness > 128 else 0)
                        colors.append(pixels[idx])
                    else:
                        dots.append(0)
                        colors.append((0, 0, 0))
            
            # Get block character
            pattern = tuple(dots[:4])
            char = blocks.get(pattern, '█')
            
            # Average color
            avg_r = sum(c[0] for c in colors) // len(colors)
            avg_g = sum(c[1] for c in colors) // len(colors)
            avg_b = sum(c[2] for c in colors) // len(colors)
            
            color = rgb_to_ansi(avg_r, avg_g, avg_b)
            line += f"{color}{char}{reset}"
        
        ascii_lines.append(line)
    
    return "\n".join(ascii_lines)

if __name__ == "__main__":
    print("🎨 Ultra High-Quality ASCII Art Converter\n")
    
    image_path = "dilpriya.jpeg"
    
    print("Choose ultra quality mode:")
    print("1. Braille Characters (4x resolution, 120 chars)")
    print("2. Tiny Blocks (2x2 resolution, 150 chars)")
    print("3. Both (compare quality)")
    print("\nEnter choice (1-3): ", end="")
    
    choice = input().strip()
    
    if choice == "1" or choice == "3":
        print("\n" + "="*80)
        print("🔬 Braille Mode - 4x Resolution (120 characters)")
        print("="*80)
        braille_art = image_to_braille(image_path, width=120)
        print(braille_art)
        
        with open("dilpriya_braille.txt", "w", encoding="utf-8") as f:
            f.write(braille_art)
        
        print("\n✅ Saved to: dilpriya_braille.txt")
    
    if choice == "2" or choice == "3":
        print("\n" + "="*80)
        print("🔬 Tiny Blocks Mode - Ultra Detail (150 characters)")
        print("="*80)
        blocks_art = image_to_tiny_blocks(image_path, width=150)
        print(blocks_art)
        
        with open("dilpriya_ultra.txt", "w", encoding="utf-8") as f:
            f.write(blocks_art)
        
        with open("dilpriya_banner_code.txt", "w", encoding="utf-8") as f:
            f.write(f'    # Ultra Quality - Tiny Blocks (150x{len(blocks_art.splitlines())} chars)\n')
            f.write(f'    ascii_image = f"""\n{blocks_art}\n"""')
        
        print("\n✅ Saved to: dilpriya_ultra.txt")
        print("✅ Banner code updated!")
    
    print("\n🎨 Ultra quality conversion complete!")

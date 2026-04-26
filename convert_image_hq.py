"""High-quality colored ASCII art converter with enhanced details."""
from PIL import Image, ImageEnhance, ImageFilter
import sys

def rgb_to_ansi(r, g, b):
    """Convert RGB to ANSI 24-bit color code."""
    return f"\033[38;2;{r};{g};{b}m"

def enhance_image(img):
    """Enhance image for better ASCII conversion."""
    # Increase sharpness
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)
    
    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)
    
    # Slight edge enhancement
    img = img.filter(ImageFilter.EDGE_ENHANCE)
    
    return img

def image_to_hq_ascii(image_path, width=100):
    """
    Convert image to high-quality colored ASCII art.
    Uses Unicode block characters for maximum detail.
    """
    # Block characters for different fill levels
    blocks = [
        " ",      # 0% filled
        "░",      # 25% filled
        "▒",      # 50% filled
        "▓",      # 75% filled
        "█"       # 100% filled
    ]
    
    # Open and enhance image
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    # Enhance before resizing
    img = enhance_image(img)
    
    # Calculate height maintaining aspect ratio
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.5)  # 0.5 for character aspect ratio
    
    # Resize with high-quality filter
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    # Get pixel data
    pixels = list(img.getdata())
    
    # Build ASCII art
    ascii_lines = []
    reset = "\033[0m"
    
    for row in range(height):
        line = ""
        for col in range(width):
            idx = row * width + col
            if idx < len(pixels):
                r, g, b = pixels[idx]
                
                # Calculate brightness for block character selection
                brightness = (r + g + b) / 3
                block_index = int((brightness / 255) * (len(blocks) - 1))
                char = blocks[block_index]
                
                # Apply color
                color = rgb_to_ansi(r, g, b)
                line += f"{color}{char}{reset}"
            else:
                line += " "
        
        ascii_lines.append(line)
    
    return "\n".join(ascii_lines)

def image_to_ultra_hq_ascii(image_path, width=120):
    """
    Ultra high-quality using half-block characters for 2x vertical resolution.
    """
    block_char = "▀"  # Upper half block
    
    # Open and enhance image
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    # Apply enhancements
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.5)
    
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.4)
    
    # Calculate height (double for half-block pairing)
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 2)
    
    # Make height even
    if height % 2 != 0:
        height += 1
    
    # Resize with LANCZOS (highest quality)
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    # Get pixel data
    pixels = list(img.getdata())
    
    # Build ASCII art with half-blocks
    ascii_lines = []
    reset = "\033[0m"
    
    for row in range(0, height, 2):
        line = ""
        for col in range(width):
            # Upper pixel
            upper_idx = row * width + col
            if upper_idx < len(pixels):
                r1, g1, b1 = pixels[upper_idx]
            else:
                r1, g1, b1 = 0, 0, 0
            
            # Lower pixel
            lower_idx = (row + 1) * width + col
            if lower_idx < len(pixels):
                r2, g2, b2 = pixels[lower_idx]
            else:
                r2, g2, b2 = 0, 0, 0
            
            # Create colored block
            fg_color = rgb_to_ansi(r1, g1, b1)
            bg_color = f"\033[48;2;{r2};{g2};{b2}m"
            
            line += f"{fg_color}{bg_color}{block_char}{reset}"
        
        ascii_lines.append(line)
    
    return "\n".join(ascii_lines)

if __name__ == "__main__":
    print("🎨 High-Quality ASCII Art Converter\n")
    
    image_path = "dilpriya.jpeg"
    
    # Try different widths
    widths = [80, 100, 120]
    
    print("Choose quality level:")
    print("1. High Quality (80 chars wide)")
    print("2. Ultra Quality (100 chars wide)")
    print("3. Maximum Quality (120 chars wide)")
    print("\nEnter choice (1-3) or press Enter for Ultra Quality: ", end="")
    
    choice = input().strip()
    
    if choice == "1":
        width = 80
        quality = "High"
    elif choice == "3":
        width = 120
        quality = "Maximum"
    else:
        width = 100
        quality = "Ultra"
    
    print(f"\n{'='*80}")
    print(f"{quality} Quality Colored ASCII Art ({width} characters wide)")
    print('='*80)
    
    # Generate ultra HQ ASCII
    colored_ascii = image_to_ultra_hq_ascii(image_path, width=width)
    print(colored_ascii)
    
    # Save to file
    output_file = f"dilpriya_ascii_{quality.lower()}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(colored_ascii)
    
    print(f"\n{'='*80}")
    print(f"✅ Saved to: {output_file}")
    
    # Save as banner code
    with open("dilpriya_banner_code.txt", "w", encoding="utf-8") as f:
        f.write(f'    # {quality} Quality ASCII Image ({width}x{len(colored_ascii.splitlines())} chars)\n')
        f.write(f'    ascii_image = f"""\n{colored_ascii}\n"""')
    
    print(f"✅ Banner code saved to: dilpriya_banner_code.txt")
    print(f"\n🎨 {quality} quality ASCII art ready for banner!")

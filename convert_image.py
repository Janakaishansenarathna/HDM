"""Convert dilpriya.jpeg to colored ASCII art for banner."""
from PIL import Image

def rgb_to_ansi(r, g, b):
    """Convert RGB to ANSI 256 color code."""
    # Use 256-color mode for better colors
    return f"\033[38;2;{r};{g};{b}m"

def image_to_colored_ascii(image_path, width=50):
    """Convert image to colored ASCII art using block characters."""
    # Use block characters for better image representation
    # Upper half block for better vertical resolution
    block_char = "▀"  # Upper half block
    
    # Open image
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    # Calculate height (divide by 2 since we use half-blocks)
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio)
    
    # Make height even for half-block pairing
    if height % 2 != 0:
        height += 1
    
    # Resize image
    img = img.resize((width, height))
    
    # Get pixel data
    pixels = list(img.getdata())
    
    # Build ASCII art with colors
    ascii_lines = []
    reset = "\033[0m"
    
    # Process two rows at a time (for upper/lower half blocks)
    for row in range(0, height, 2):
        line = ""
        for col in range(width):
            # Get upper pixel
            upper_idx = row * width + col
            if upper_idx < len(pixels):
                r1, g1, b1 = pixels[upper_idx]
            else:
                r1, g1, b1 = 0, 0, 0
            
            # Get lower pixel
            lower_idx = (row + 1) * width + col
            if lower_idx < len(pixels):
                r2, g2, b2 = pixels[lower_idx]
            else:
                r2, g2, b2 = 0, 0, 0
            
            # Create colored block
            # Upper half gets foreground color, lower half gets background color
            fg_color = rgb_to_ansi(r1, g1, b1)
            bg_color = f"\033[48;2;{r2};{g2};{b2}m"
            
            line += f"{fg_color}{bg_color}{block_char}{reset}"
        
        ascii_lines.append(line)
    
    return "\n".join(ascii_lines)

def image_to_simple_ascii(image_path, width=50):
    """Convert to simpler ASCII with basic colors."""
    # Density characters
    density = " .:-=+*#%@"
    
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.5)
    
    img = img.resize((width, height))
    pixels = list(img.getdata())
    
    ascii_str = ""
    reset = "\033[0m"
    
    for i, (r, g, b) in enumerate(pixels):
        # Calculate brightness
        brightness = (r + g + b) // 3
        char = density[brightness * len(density) // 256]
        
        # Add color
        color = rgb_to_ansi(r, g, b)
        ascii_str += f"{color}{char}{reset}"
        
        if (i + 1) % width == 0:
            ascii_str += "\n"
    
    return ascii_str

if __name__ == "__main__":
    print("🎨 Converting dilpriya.jpeg to colored ASCII art...\n")
    
    # Method 1: Block characters (better quality)
    print("=" * 60)
    print("Method 1: Colored Block ASCII Art (High Quality)")
    print("=" * 60)
    colored_ascii = image_to_colored_ascii("dilpriya.jpeg", width=80)
    print(colored_ascii)
    
    # Save to file
    with open("dilpriya_colored_ascii.txt", "w", encoding="utf-8") as f:
        f.write(colored_ascii)
    
    print("\n" + "=" * 60)
    print("✅ Colored ASCII art saved to: dilpriya_colored_ascii.txt")
    print("=" * 60)
    
    # Also create Python code version
    ascii_code = colored_ascii.replace("\\", "\\\\").replace('"', '\\"')
    with open("dilpriya_banner_code.txt", "w", encoding="utf-8") as f:
        f.write(f'    ascii_image = f"""\n{colored_ascii}\n"""')
    
    print("✅ Banner code saved to: dilpriya_banner_code.txt")
    print("\n🎨 You can now add this to banner.py!")

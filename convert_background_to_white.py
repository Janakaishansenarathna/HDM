import re

def rgb_to_ansi(r, g, b):
    """Convert RGB values to ANSI escape code"""
    return f'\033[38;2;{r};{g};{b}m'

def is_skin_tone(r, g, b):
    """
    Detect if RGB values represent skin tones or facial features.
    Returns True if the color should be preserved, False if it should be white.
    Only preserve colors that are clearly part of a person (skin, hair, clothing).
    """
    
    # Skin tone ranges (all shades from light to dark)
    # Light to medium skin tones
    if (r > 100 and r < 255 and 
        g > 70 and g < 200 and 
        b > 50 and b < 170 and
        r > g and g > b and
        (r - g) > 5 and (g - b) > 5):
        return True
    
    # Dark skin tones and brown colors
    if (r > 60 and r < 130 and
        g > 40 and g < 100 and
        b > 20 and b < 80 and
        r >= g >= b):
        return True
    
    # Very dark colors (hair, dark clothing, shadows)
    if r < 80 and g < 80 and b < 80:
        return True
    
    # Reddish/pinkish tones (lips, cheeks)
    if (r > 120 and r < 255 and
        g > 50 and g < 180 and
        b > 50 and b < 150 and
        r > g + 20 and r > b + 20):
        return True
    
    # Dark hair colors (black to dark brown)
    if (r > 20 and r < 90 and
        g > 10 and g < 80 and
        b > 0 and b < 70 and
        abs(r - g) < 30):
        return True
    
    # Everything else is background - convert to white
    return False

def process_portrait_file(input_file, output_file):
    """Process the portrait file and convert backgrounds to white"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match ANSI color codes with RGB values
    pattern = r'\[38;2;(\d+);(\d+);(\d+)m(.)\[0m'
    
    def replace_color(match):
        r, g, b, char = int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4)
        
        # If it's a skin tone or facial feature, keep original color
        if is_skin_tone(r, g, b):
            return f'[38;2;{r};{g};{b}m{char}[0m'
        else:
            # Convert to white (255, 255, 255)
            return f'[38;2;255;255;255m{char}[0m'
    
    # Process the content
    processed_content = re.sub(pattern, replace_color, content)
    
    # Write the processed content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_content)
    
    print(f"✅ Processed portrait saved to: {output_file}")
    print(f"Background colors converted to white while preserving facial features")

if __name__ == "__main__":
    input_file = "dilpriya_braille.txt"
    output_file = "dilpriya_braille_white_bg.txt"
    
    process_portrait_file(input_file, output_file)

import re

def convert_specific_to_white(input_file, output_file):
    """Convert only specific background colors to white"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Based on frequency analysis, these are the main background colors:
    # RGB(0,0,0) - 2006 occurrences - BLACK
    # RGB(255,255,255) - 610 occurrences - WHITE  
    # RGB(0,0,1), RGB(255,255,254), RGB(218,221,220) etc - near-black/near-white variations
    
    # Define background colors to convert (high frequency colors that are clearly background)
    background_colors = {
        (0, 0, 0),      # Pure black
        (0, 0, 1),      # Near black
        (1, 1, 1),
        (0, 1, 1),
        (0, 0, 2),
        (0, 0, 3),
        (2, 2, 2),
        (0, 0, 4),
        (1, 1, 0),
        (1, 0, 0),
        (0, 0, 5),
        (0, 1, 2),
        # Near-white colors
        (255, 255, 254),
        (254, 254, 254),
        (255, 255, 252),
        (255, 255, 251),
        (255, 255, 253),
        # Light gray colors (likely background)
        (218, 221, 220),
        (220, 223, 221),
        (217, 220, 218),
        (221, 224, 223),
        (220, 223, 222),
        (219, 222, 220),
        (217, 220, 219),
        (221, 221, 218),
        (219, 222, 221),
        (220, 221, 214),
        (221, 223, 215),
        (220, 222, 214),
    }
    
    pattern = r'\x1b\[38;2;(\d+);(\d+);(\d+)m(.)\x1b\[0m'
    
    def replace_color(match):
        r, g, b, char = int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4)
        
        # If this color is in background set, convert to white
        if (r, g, b) in background_colors:
            return f'\x1b[38;2;255;255;255m{char}\x1b[0m'
        else:
            # Keep original color (character, clothing, hair, etc.)
            return match.group(0)
    
    processed_content = re.sub(pattern, replace_color, content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_content)
    
    print(f"✅ Converted specific background colors to white")
    print(f"✅ Preserved all character colors (skin, clothing, hair, accessories)")

if __name__ == "__main__":
    input_file = "dilpriya_braille.txt"
    output_file = "dilpriya_braille_targeted.txt"
    
    convert_specific_to_white(input_file, output_file)

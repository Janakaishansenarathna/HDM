import re

def is_skin_tone(r, g, b):
    """
    Detect if a color is likely a human skin tone.
    Skin tones typically have:
    - R > G > B (red channel highest)
    - R and G relatively close
    - Specific ranges for each channel
    """
    # Skin tone detection rules
    if r < 95 or r > 255:
        return False
    if g < 40 or g > 200:
        return False
    if b < 20 or b > 150:
        return False
    
    # Red should be greater than green
    if r <= g:
        return False
    
    # Green should be greater than blue
    if g <= b:
        return False
    
    # Additional checks for skin tone characteristics
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    
    # Check if there's enough difference between channels
    if max_val - min_val < 15:
        return False
    
    # Check specific ratios
    if abs(r - g) < 15:
        return False
    
    return True

def convert_non_skin_to_white(input_file, output_file):
    """Convert all non-skin-tone colors to white"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match ANSI color codes with character
    pattern = r'\x1b\[38;2;(\d+);(\d+);(\d+)m(.)\x1b\[0m'
    
    def replace_color(match):
        r, g, b, char = int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4)
        
        # If it's a skin tone, keep it
        if is_skin_tone(r, g, b):
            return match.group(0)
        else:
            # Convert to white
            return f'\x1b[38;2;255;255;255m{char}\x1b[0m'
    
    processed_content = re.sub(pattern, replace_color, content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_content)
    
    print(f"✅ Processed portrait saved to: {output_file}")
    print("All non-skin-tone colors converted to white")

if __name__ == "__main__":
    input_file = "dilpriya_braille.txt"
    output_file = "dilpriya_braille_skin_only.txt"
    
    print("Converting all non-skin-tone colors to white...")
    convert_non_skin_to_white(input_file, output_file)

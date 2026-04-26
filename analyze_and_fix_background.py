import re
from collections import Counter

def analyze_portrait_colors(input_file):
    """Analyze the portrait to find background vs character colors"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match ANSI color codes with RGB values (with ESC character \x1b or \033)
    pattern = r'\x1b\[38;2;(\d+);(\d+);(\d+)m(.)\x1b\[0m'
    
    # Collect all colors with their characters
    colors = []
    for match in re.finditer(pattern, content):
        r, g, b, char = int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4)
        colors.append((r, g, b, char))
    
    print(f"Total characters in portrait: {len(colors)}")
    
    # Count color frequencies
    color_counts = Counter([(r, g, b) for r, g, b, _ in colors])
    
    print("\nTop 30 most frequent colors:")
    for (r, g, b), count in color_counts.most_common(30):
        print(f"RGB({r:3d}, {g:3d}, {b:3d}) - Count: {count:5d} - {'LIKELY BACKGROUND' if count > 100 else 'Character detail'}")
    
    # Identify background colors (colors that appear very frequently)
    background_colors = set()
    for (r, g, b), count in color_counts.items():
        # Background colors typically appear more than 80 times
        if count > 80:
            background_colors.add((r, g, b))
    
    print(f"\n{len(background_colors)} background colors identified")
    
    return background_colors

def fix_background_to_white(input_file, output_file, background_colors):
    """Convert specific background colors to white"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'\x1b\[38;2;(\d+);(\d+);(\d+)m(.)\x1b\[0m'
    
    def replace_color(match):
        r, g, b, char = int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4)
        
        # If this exact color is in background set, convert to white
        if (r, g, b) in background_colors:
            return f'\x1b[38;2;255;255;255m{char}\x1b[0m'
        else:
            # Keep original color (character detail)
            return f'\x1b[38;2;{r};{g};{b}m{char}\x1b[0m'
    
    processed_content = re.sub(pattern, replace_color, content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_content)
    
    print(f"\n✅ Processed portrait saved to: {output_file}")
    print(f"All background colors converted to white while preserving character details")

if __name__ == "__main__":
    input_file = "dilpriya_braille.txt"
    output_file = "dilpriya_braille_white_bg.txt"
    
    print("Analyzing portrait colors...")
    background_colors = analyze_portrait_colors(input_file)
    
    print("\nConverting background colors to white...")
    fix_background_to_white(input_file, output_file, background_colors)

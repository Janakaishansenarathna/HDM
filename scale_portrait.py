import re

def scale_portrait_width(input_file, output_file, scale_factor=0.5):
    """Scale portrait by sampling characters at intervals"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    scaled_lines = []
    
    for line in lines:
        # Extract all color codes and characters
        pattern = r'(\x1b\[38;2;\d+;\d+;\d+m)(.)(\x1b\[0m)'
        matches = list(re.finditer(pattern, line))
        
        if not matches:
            scaled_lines.append(line)
            continue
        
        # Sample characters at intervals based on scale factor
        step = int(1 / scale_factor)
        sampled_chars = []
        
        for i in range(0, len(matches), step):
            match = matches[i]
            color_code = match.group(1)
            char = match.group(2)
            reset = match.group(3)
            sampled_chars.append(f"{color_code}{char}{reset}")
        
        scaled_lines.append(''.join(sampled_chars))
    
    scaled_content = '\n'.join(scaled_lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(scaled_content)
    
    print(f"Original width: ~{len(matches)} characters per line")
    print(f"Scaled width: ~{len(sampled_chars)} characters per line")
    print(f"Scale factor: {scale_factor} ({int(scale_factor * 100)}%)")
    print(f"✅ Scaled portrait saved to: {output_file}")

if __name__ == "__main__":
    # Restore full size first
    import shutil
    shutil.copy("dilpriya_braille_full.txt", "dilpriya_braille_backup2.txt")
    
    input_file = "dilpriya_braille_full.txt"
    output_file = "dilpriya_braille.txt"
    
    print("Scaling portrait to 50% width (keeping all lines)...")
    scale_portrait_width(input_file, output_file, scale_factor=0.5)

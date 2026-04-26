import re

def resize_portrait(input_file, output_file, target_height=30):
    """Resize portrait by selecting every nth line"""
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Calculate how many lines to skip
    current_height = len(lines)
    skip_ratio = current_height / target_height
    
    # Select lines at regular intervals
    selected_lines = []
    for i in range(target_height):
        index = int(i * skip_ratio)
        if index < len(lines):
            selected_lines.append(lines[index])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(selected_lines)
    
    print(f"Original height: {current_height} lines")
    print(f"New height: {len(selected_lines)} lines")
    print(f"✅ Resized portrait saved to: {output_file}")

if __name__ == "__main__":
    input_file = "dilpriya_braille.txt"
    output_file = "dilpriya_braille_resized.txt"
    
    print("Resizing portrait to suitable height...")
    resize_portrait(input_file, output_file, target_height=30)

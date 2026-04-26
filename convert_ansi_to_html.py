"""Convert ANSI colored Braille portrait to HTML for README"""
import re

def ansi_to_html(ansi_text):
    """Convert ANSI escape codes to HTML spans with inline styles"""
    # Pattern to match ANSI color codes with actual escape character \x1b
    pattern = r'\x1b\[38;2;(\d+);(\d+);(\d+)m(.)\x1b\[0m'
    
    html_lines = []
    for line in ansi_text.strip().split('\n'):
        html_chars = []
        # Find all color-coded characters
        matches = re.findall(pattern, line)
        
        for r, g, b, char in matches:
            # Escape HTML special characters
            if char == '<':
                char = '&lt;'
            elif char == '>':
                char = '&gt;'
            elif char == '&':
                char = '&amp;'
            html_chars.append(f'<span style="color:rgb({r},{g},{b})">{char}</span>')
        
        if html_chars:
            html_lines.append(''.join(html_chars))
    
    return html_lines

# Read the Braille portrait
with open('dilpriya_braille.txt', 'r', encoding='utf-8') as f:
    ansi_content = f.read()

# Convert to HTML
html_lines = ansi_to_html(ansi_content)

# Create HTML block
html_output = '<div style="font-family: monospace; line-height: 1; white-space: pre; font-size: 8px; background: #1e1e1e; padding: 20px; border-radius: 8px;">\n'
for line in html_lines:
    html_output += f'{line}\n'
html_output += '</div>'

# Save to file
with open('portrait_html.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print(f"Converted {len(html_lines)} lines to HTML")
print("Saved to portrait_html.html")

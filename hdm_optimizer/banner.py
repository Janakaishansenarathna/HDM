"""ASCII banner for HDM Optimizer."""

from .__version__ import __version__, __author__, __license__, __url__


def display_banner():
    """Display the HDM Optimizer banner."""
    # ANSI color codes
    DARK_BLUE = '\033[34m'
    YELLOW = '\033[93m'  # Yellow for D letter
    DARK_PURPLE = '\033[35m'
    ORANGE = '\033[93m'
    GREEN = '\033[92m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Read the complete Braille portrait from file
    import os
    portrait_path = os.path.join(os.path.dirname(__file__), '..', 'dilpriya_braille.txt')
    try:
        with open(portrait_path, 'r', encoding='utf-8') as f:
            portrait_lines = f.readlines()
            # Center align each line (assuming 120 char terminal width, 60 char portrait)
            centered_lines = []
            for line in portrait_lines:
                line = line.rstrip()
                if line:  # Only center non-empty lines
                    # Calculate padding for center alignment (120 total width - 60 portrait width = 60 padding / 2 = 30 spaces on each side)
                    padding = ' ' * 30
                    centered_lines.append(padding + line)
                else:
                    centered_lines.append(line)
            portrait = '\n'.join(centered_lines)
    except:
        # Fallback if file not found
        portrait = "(Portrait unavailable)"
    
    banner = f"""
{WHITE}═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{RESET}
{BOLD}                                     A Tribute to Ms. Hirushi Dilpriya Thilakarathne{RESET}
{WHITE}═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{RESET}

{portrait}

{WHITE}═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{RESET}

                                        {WHITE}██╗  ██╗{RESET} {WHITE}██████╗ {RESET} {WHITE}███╗   ███╗{RESET}
                                        {WHITE}██║  ██║{RESET} {WHITE}██╔══██╗{RESET} {WHITE}████╗ ████║{RESET}
                                        {DARK_BLUE}███████║{RESET} {YELLOW}██║  ██║{RESET} {DARK_PURPLE}██╔████╔██║{RESET}
                                        {DARK_BLUE}██╔══██║{RESET} {YELLOW}██║  ██║{RESET} {DARK_PURPLE}██║╚██╔╝██║{RESET}
                                        {DARK_BLUE}██║  ██║{RESET} {YELLOW}██████╔╝{RESET} {DARK_PURPLE}██║ ╚═╝ ██║{RESET}
                                        {DARK_BLUE}╚═╝  ╚═╝{RESET} {YELLOW}╚═════╝ {RESET} {DARK_PURPLE}╚═╝     ╚═╝{RESET}

                           {BOLD}{WHITE}H. Dilpriya's Momentum (HDM) Multi-Strategy Gradient Optimizer{RESET}
                                   {BOLD}{WHITE}Hirushi Dilpriya Momentum (HDM){RESET} {ORANGE}|{RESET} {GREEN}Version {__version__}{RESET}

{WHITE}═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{RESET}
"""
    print(banner)

#!/usr/bin/env python3
"""
🚀 Terminal Spaceship Simulation
Press Ctrl+C to warp out
"""

import time
import random
import sys

# Spaceship designs
ROCKET = [
    "       |",
    "      / \\",
    "     / _ \\",
    "    |.o '.|",
    "    |'._.'|",
    "    |     |",
    "  .'  `-.  `.",
    " /  `.   `.  \\",
    "/___. `-.  .-'\\",
    "      `| |"
]

UFO = [
    "         _____",
    "     .-''     ''-.",
    "   .'   .-'\"'-.   `.",
    "  /    /        \\    \\",
    " |    |  o    o  |    |",
    "  \\    \\        /    /",
    "   `._  `-....-'  _.'",
    "       `-......-'"
]

STARSHIP = [
    "          /\\",
    "         /  \\",
    "        /    \\",
    "       /______\\",
    "      |  __  __  |",
    "      | |  ||  | |",
    "     /| |  ||  | |\\",
    "    / | |__||__| | \\",
    "   |  |  ____   |  |",
    "   |  | /    \\  |  |",
    "   |__|/      \\ |__|",
    "  / _____________ \\",
    " / /    ___      \\ \\",
    "||    /   \\      ||",
    "||   |     |     ||",
    " \\    \\___/     //",
    "  \\____________//",
    "     |||   |||",
    "    /|||   |||\\",
    "   / |||   ||| \\",
    "  /  |||   |||  \\",
    " '   '''   '''   '"
]

STARS = ['.', '*', '+', '·', '•', '◦']
COLORS = {
    'red': '\033[91m',
    'green': '\033[92m', 
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'reset': '\033[0m'
}

def clear():
    print('\033[2J\033[H', end='')

def colorize(text, color):
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"

def draw_stars(width, height, density=0.1):
    """Generate random starfield"""
    field = [[' ' for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if random.random() < density:
                field[y][x] = random.choice(STARS)
    return field

def overlay_ship(field, ship, offset_y, offset_x):
    """Place spaceship on starfield"""
    for i, line in enumerate(ship):
        y = offset_y + i
        if 0 <= y < len(field):
            for j, char in enumerate(line):
                x = offset_x + j
                if 0 <= x < len(field[0]) and char != ' ':
                    field[y][x] = char
    return field

def render(field, engine_trail=False):
    """Render the field to terminal"""
    output = []
    for y, row in enumerate(field):
        line = ''
        for x, char in enumerate(row):
            if char in STARS:
                line += colorize(char, random.choice(['white', 'cyan', 'blue']))
            elif char in '|/\\_-+.\'o"':
                if engine_trail and y > len(field) // 2:
                    line += colorize(char, random.choice(['red', 'yellow', 'magenta']))
                else:
                    line += colorize(char, 'white')
            else:
                line += char
        output.append(line)
    return '\n'.join(output)

def warp_effect():
    """Hyperspace warp effect"""
    for _ in range(20):
        clear()
        lines = []
        for i in range(20):
            indent = ' ' * random.randint(0, 40)
            streak = colorize('|' * random.randint(10, 30), random.choice(['cyan', 'blue', 'magenta']))
            lines.append(indent + streak)
        print('\n'.join(lines))
        time.sleep(0.05)

def launch_sequence(ship):
    """Animate spaceship launch"""
    term_height = 30
    term_width = 80
    
    for frame in range(term_height - len(ship) - 5):
        clear()
        
        # Generate starfield
        field = draw_stars(term_width, term_height, density=0.05)
        
        # Position ship (moving up)
        ship_y = term_height - len(ship) - 1 - frame
        ship_x = term_width // 2 - max(len(line) for line in ship) // 2
        
        # Add engine trail
        trail_y = ship_y + len(ship)
        for i in range(min(5, term_height - trail_y)):
            if trail_y + i < term_height:
                tx = ship_x + len(ship[0]) // 2
                if 0 <= tx < term_width:
                    field[trail_y + i][tx] = random.choice(['|', '!', 'i', ':'])
        
        field = overlay_ship(field, ship, ship_y, ship_x)
        print(render(field, engine_trail=True))
        print(colorize(f"\n   Altitude: {frame * 100} km  |  Velocity: Mach {frame + 1}", 'green'))
        time.sleep(0.08)

def fly_through_space(ship, duration=10):
    """Cruise through space"""
    term_height = 30
    term_width = 80
    start_time = time.time()
    
    while time.time() - start_time < duration:
        clear()
        field = draw_stars(term_width, term_height, density=0.08)
        
        # Add some twinkling
        for _ in range(5):
            y, x = random.randint(0, term_height-1), random.randint(0, term_width-1)
            field[y][x] = colorize('✦', 'yellow')
        
        ship_y = term_height // 2 - len(ship) // 2
        ship_x = term_width // 2 - max(len(line) for line in ship) // 2
        field = overlay_ship(field, ship, ship_y, ship_x)
        
        print(render(field))
        print(colorize("\n   🌌 Cruising through deep space...", 'cyan'))
        time.sleep(0.15)

def main():
    print(colorize("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║           🚀  WELCOME TO SPACESHIP SIMULATOR  🚀         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """, 'cyan'))
    
    print("Choose your spacecraft:")
    print(colorize("  1. Classic Rocket", 'red'))
    print(colorize("  2. UFO", 'green'))
    print(colorize("  3. Starship", 'blue'))
    print(colorize("  4. Random", 'yellow'))
    
    choice = input("\nSelection (1-4): ").strip()
    
    ships = [ROCKET, UFO, STARSHIP]
    if choice == '4':
        ship = random.choice(ships)
    else:
        try:
            ship = ships[int(choice) - 1]
        except (ValueError, IndexError):
            ship = ROCKET
    
    print(colorize("\n🔥 Initiating launch sequence...", 'yellow'))
    time.sleep(1)
    
    try:
        launch_sequence(ship)
        warp_effect()
        fly_through_space(ship, duration=8)
        
        clear()
        print(colorize("""
        ╔══════════════════════════════════════════════════════════╗
        ║                                                          ║
        ║        🌟 MISSION ACCOMPLISHED - WELCOME HOME 🌟        ║
        ║                                                          ║
        ╚══════════════════════════════════════════════════════════╝
        """, 'green'))
        
    except KeyboardInterrupt:
        clear()
        print(colorize("""
        ╔══════════════════════════════════════════════════════════╗
        ║                                                          ║
        ║           🛸 EMERGENCY LANDING INITIATED 🛸              ║
        ║                                                          ║
        ╚══════════════════════════════════════════════════════════╝
        """, 'red'))

if __name__ == "__main__":
    main()

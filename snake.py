# The game is based on the curses library
import curses
# Random library to generate random food positions
import random

logo = """
   _____                   _              _     _                      
  / ____|                 | |            | |   | |                     
 | (___    _ __     __ _  | | __  _   _  | |_  | |__     ___    _ __   
  \___ \  | '_ \   / _` | | |/ / | | | | | __| | '_ \   / _ \  | '_ \  
  ____) | | | | | | (_| | |   <  | |_| | | |_  | | | | | (_) | | | | | 
 |_____/  |_| |_|  \__,_| |_|\_\  \__, |  \__| |_| |_|  \___/  |_| |_| 
                                   __/ |                               
                                  |___/                                
"""

version = """
Snakython v 1.0
Created by
Pasquale Coscia
"""

# Main menu options
menu = ['Play', 'Help', 'Exit']

help_message = """
Welcome to Snakython v 1.0!
This is a python implementation of the famous video game concept 'Snake'.
The aim of the game is to maneuver a moving line representing a snake
which grows in length when eats randomly positioned items.

Keys:
     UP key -> Move snake up.
     DOWN key -> Move snake down.
     LEFT key -> Move snake left.
     RIGHT key -> Move snake right.
     [0..9] -> Change snake's style.

Press a key to return to the main menu.
"""

# Print logo function
def print_logo(logo, h, w, stdscr):
    
    rows = logo.split('\n')
    
    len_rows = [len(row) for row in rows]
    logo_width = max(len_rows)
    
    logo_height = len(rows)
    
    # Starting x printing position
    x = w//2 - logo_width//2
    # Starting y printing position
    y = 0
    # Print option
    for idx, row in enumerate(rows):
        stdscr.addstr(y+idx, x, row)

    stdscr.refresh()

# Print snake version
def print_version(version, h, w, stdscr):
    
    rows = version.split('\n')
    
    for idx, row in enumerate(rows):
        # Starting x printing position
        x = w//2 - len(row)//2
        # Starting y printing position
        y = h - len(rows)-2 + idx
        stdscr.addstr(y, x, row)

# Print score
def print_score(score, h, w, stdscr):
    
    text = 'Score: ' + str(score)
    # Starting x printing position
    x = w//2 - len(text)//2
    # Starting y printing position
    y = 1
    stdscr.addstr(y, x, text)
        
# Print help menu
def print_help(stdscr, h, w):
    
    stdscr.clear()
    
    rows = help_message.split('\n')
    
    for idx, row in enumerate(rows):
        # Starting x printing position
        x = w//2 - len(row)//2
        # Starting y printing position
        y = 0
        stdscr.addstr(y+idx, x, row)

    stdscr.refresh()
    
        # Wait input character
    key = stdscr.getkey()
    
    return key

# Snake game
def snake(s, sh, sw):

    # New window starting top-left screen
    w = curses.newwin(sh, sw, 0, 0)
    # Accept input keys
    w.keypad(1)
    # Refresh screen every 100 ms
    w.timeout(100)
    # Food symbol (i.e., character) unicode
    food_chr = ord('O')
    # Default snake style
    snake_style = curses.ACS_CKBOARD
    # Inizialize score
    score = 0
    
    # Snake's initial position
    snk_x = sw//4
    snk_y = sh//2
    
    # Snake's body parts
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x-1],
        [snk_y, snk_x-2]
        ]
    
    # Starting place food (center's screen)
    food = [sh//2, sw//2]
    # Add food to the screen
    w.addch(food[0], food[1], food_chr)
    
    # Initial direction
    key = curses.KEY_RIGHT
    
    # Infinite loop
    while True:
        # Print score
        print_score(score, sh, sw, s)
        
        # Refresh
        s.refresh()
        
        # Check pressed key
        next_key = w.getch()
        
        # Dictionary of styles (key: FN_key, value: style)
        # Keys: [0..9]
        stylesDict = {49: curses.ACS_CKBOARD, 
            50: curses.ACS_BULLET,
            51: curses.ACS_BLOCK,
            52: curses.ACS_DIAMOND,
            53: curses.ACS_HLINE,
            54: curses.ACS_VLINE,
            55: curses.ACS_UARROW,
            56: curses.ACS_DARROW,
            57: curses.ACS_LARROW,
            48: curses.ACS_RARROW,
        }
        
        # Change snake's style
        if next_key in stylesDict.keys():
            snake_style = stylesDict[next_key]
        else:
            # Set key
            key = key if next_key == -1 else next_key
            
        # Game over
        if snake[0][0] in [0, sh-1] or snake[0][1] in [0, sw-1] or snake[0] in snake[1:]:
            # Return to the main menu
            break
            
        # Detect new head of the snake
        new_head = [snake[0][0], snake[0][1]]
        
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1
            
        # Insert new head of the snake    
        snake.insert(0, new_head)
        
        # Eated food
        if snake[0] == food:
            # Increase score
            score += 100
            food = None
            # Create new food location
            while food is None:
                nf = [
                    random.randint(2, sh-1), # line 1 prints score
                    random.randint(1, sw-1)
                    ]
                # Set food
                food = nf if nf not in snake else None
            
            # Add new food position
            w.addch(food[0], food[1], food_chr)
        else:
            # Remove last snake's body part
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')
            
        # Add head of the snake
        w.addch(snake[0][0], snake[0][1], snake_style)

# Main menu visualization
def main_menu(stdscr, selected_row_idx, h, w):
    # Clear screen
    stdscr.clear()

    # Print logo
    print_logo(logo, h, w, stdscr)
    # Print menu options at the screen's center
    # Loop over menu options
    for idx, row in enumerate(menu):
        # Starting x printing position
        x = w//2 - len(row)//2
        # Starting y printing position
        y = h//2 - len(menu)//2 + idx
        # Change color pair for the selected option
        if idx == selected_row_idx:
            # Set color pair on
            stdscr.attron(curses.color_pair(1))
            # Print option
            stdscr.addstr(y, x, row)
            # Set color pair off
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    print_version(version, h, w, stdscr)
    
    stdscr.refresh()
    
# Main function    
def main(stdscr):
    # Hide blinking cursor
    curses.curs_set(0)
    # Get max x and y coordinates
    h, w = stdscr.getmaxyx()
    # Define color pair for selected menu option
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    # Initialize selected index row
    current_idx_row = 0
    
    # Visualize main menu
    main_menu(stdscr, current_idx_row, h, w)
    
    while True:
        # Wait input character
        key = stdscr.getch()
        
        # Clear screen
        stdscr.clear()
        
        # If the user pressed Up key then decrease current idx row
        if key == curses.KEY_UP and current_idx_row > 0:
            current_idx_row -= 1
        # If the user pressed Down key then increase current idx row
        elif key == curses.KEY_DOWN and current_idx_row < len(menu)-1:
            current_idx_row += 1
        # If the users pressed Enter then print message
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # if user selected Play then start game
            if current_idx_row == 0:
                snake(stdscr, h, w)
            # if user selected Help then visualize user's guide:
            if current_idx_row == 1:
                pressed_key = print_help(stdscr, h, w)
            # If user selected Exit then close windows
            if current_idx_row == 2:
                break
        
        # Visualize main menu
        main_menu(stdscr, current_idx_row, h, w)        
        # Refresh screen
        stdscr.refresh()

# Define wrapper to automatically handle initialization parameters    
curses.wrapper(main)

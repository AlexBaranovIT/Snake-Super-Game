import pygame
import sys
import random
import csv

# Initialization Pygame
pygame.init()
# Initialization sounds Pygame
pygame.mixer.init()


clock = pygame.time.Clock()

# Definition colors and parameters
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SAND_COLOR = (194, 178, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
screen_size = 500
# Definition cell size
cell_size = 20
current_level = 1  # Default level

# Checking the existence of files with images and sound
try:
    # Image loading for game
    # Snake head
    snake_head_img = pygame.image.load('snake_yellow_head.png')
    # Snake body
    snake_body_img = pygame.image.load('snake_yellow_blob.png')
    # Apples
    apple_green_img = pygame.image.load('apple_green.png')
    apple_red_img = pygame.image.load('apple_red.png')
    # Wall
    wall_block_img = pygame.image.load('wall_block.png')
    # Sound of fruit eating
    eat_sound = pygame.mixer.Sound('fruit_eat_sound.wav')
    # Game over sound
    game_over_sound = pygame.mixer.Sound('snake_die_sound.wav')
except pygame.error as e:
    print(f"Error while loading sources: {e}")
    sys.exit()


# Convert everything to the size of one cell
snake_head_img = pygame.transform.scale(snake_head_img, (cell_size, cell_size))
snake_body_img = pygame.transform.scale(snake_body_img, (cell_size, cell_size))
apple_green_img = pygame.transform.scale(apple_green_img, (cell_size, cell_size))
apple_red_img = pygame.transform.scale(apple_red_img, (cell_size, cell_size))
wall_block_img = pygame.transform.scale(wall_block_img, (cell_size, cell_size))

# Dict that keeps all level obstacles
fruit_images_by_level = {
    1: [apple_green_img],
    2: [apple_green_img, apple_red_img],
    3: [apple_green_img, apple_red_img],
    4: [apple_green_img, apple_red_img],
    5: [apple_green_img, apple_red_img]
}

# Fruit current image
current_fruit_img = apple_green_img

# Change of size if needed
apple_red_img = pygame.transform.scale(apple_red_img, (cell_size, cell_size))

screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Snake Game")

# Constant states of the game
MAIN_MENU, LEVEL_SELECTION, GAME_PLAYING, GAME_OVER = range(4)

# Current game state
game_state = MAIN_MENU
# Game score
score = 0
special_fruit_counter = 0
special_fruit_active = False
special_fruit = {"x": 0, "y": 0}
obstacles = []  # Add obstacles to the level
snake = [{"x": 100, "y": 100}, {"x": 90, "y": 100}, {"x": 80, "y": 100}]
snake_speed = 15  # Snake speed
change_direction = "RIGHT"
fruit = {"x": random.randrange(1, screen_size // cell_size) * cell_size,
         "y": random.randrange(1, screen_size // cell_size) * cell_size}


def draw_grid():
    # Draw a grid at the back
    for x in range(0, screen_size, cell_size):
        for y in range(0, screen_size, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect, 1)


# Functions of each level
# Reload every level obstacles and fruits
def level_1():
    global snake_speed, obstacles, current_fruit_img
    snake_speed = 10
    obstacles = []  # No obstacles on the level 1
    current_fruit_img = random.choice(fruit_images_by_level[1])


def level_2():
    global snake_speed, obstacles, current_fruit_img
    snake_speed = 10
    obstacles = [{'x': 5, 'y': 5}, {'x': 8, 'y': 8}]  # Obstacles level 2
    current_fruit_img = random.choice(fruit_images_by_level[2])


def level_3():
    global snake_speed, obstacles, current_fruit_img
    snake_speed = 10
    obstacles = [{'x': 3, 'y': 3}, {'x': 6, 'y': 6}, {'x': 9, 'y': 9}]  # Obstacles level 3
    current_fruit_img = random.choice(fruit_images_by_level[3])


def level_4():
    global snake_speed, obstacles, current_fruit_img
    snake_speed = 10
    obstacles = [{'x': 2, 'y': 2}, {'x': 5, 'y': 5}, {'x': 8, 'y': 8}, {'x': 11, 'y': 11}]  # Obstacles level 4
    current_fruit_img = random.choice(fruit_images_by_level[4])


def level_5():
    global snake_speed, obstacles, current_fruit_img
    snake_speed = 10
    obstacles = [
        {'x': 1, 'y': 1}, {'x': 3, 'y': 3}, {'x': 5, 'y': 5}, {'x': 7, 'y': 7},
        {'x': 9, 'y': 9}, {'x': 11, 'y': 11}, {'x': 13, 'y': 13}
    ]  # Obstacles level 5
    current_fruit_img = random.choice(fruit_images_by_level[5])


def authenticate():
    login = ''
    password = ''
    show_password = False
    login_active = False
    password_active = False
    # Font for the text
    font = pygame.font.Font(None, 30)
    error_font = pygame.font.Font(None, 24)  # Smaller font for error messages

    # Size of the screen
    screen_size = 500  # Example of screen size
    screen = pygame.display.set_mode((screen_size, screen_size))  # Stating the window size

    message = ''  # Error or status message

    login_rect = pygame.Rect(120, 100, 200, 32)  # Login field
    password_rect = pygame.Rect(120, 150, 200, 32)  # Password field

    # Inrease the rectangle size
    show_password_rect = pygame.Rect(325, 150, 120, 32)  # Expanded width

    # Subroutine for checking the login credentials
    def check_existing_credentials(login, password):
        try:
            with open('credentials.csv', 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == login:
                        return row[1] == password
                return None  # Login not found
        except FileNotFoundError:
            return None  # File not foudn

    while True:
        screen.fill((255, 255, 255))

        # Drawing the fields for authentication
        login_label = font.render("Login:", True, BLACK)
        password_label = font.render("Password", True, BLACK)
        screen.blit(login_label, (login_rect.x - 80, login_rect.y + 5))
        screen.blit(password_label, (password_rect.x - 100, password_rect.y + 5))

        # Drawing the rectangles for login and password
        pygame.draw.rect(screen, BLACK, login_rect, 2)
        pygame.draw.rect(screen, BLACK, password_rect, 2)
        pygame.draw.rect(screen, BLACK, show_password_rect)

        # Showing the password 'Show' button
        show_password_text = font.render("Show" if not show_password else "Hide", True, WHITE)
        screen.blit(show_password_text, (show_password_rect.x + 5, show_password_rect.y + 5))

        # Showing the typed login and password
        login_surf = font.render(login, True, BLACK)
        password_display = password if show_password else '*' * len(password)
        password_surf = font.render(password_display, True, BLACK)
        screen.blit(login_surf, (login_rect.x + 5, login_rect.y + 5))
        screen.blit(password_surf, (password_rect.x + 5, password_rect.y + 5))

        # Showing the error message with smaller font
        if message:
            message_surf = error_font.render(message, True, RED)
            # Centre the message
            message_rect = message_surf.get_rect(center=(screen_size / 2, 280))
            screen.blit(message_surf, message_rect.topleft)

        for event in pygame.event.get():
            # Checking the pygame events
            if event.type == pygame.QUIT:
                # If the event is close the game
                pygame.quit()  # Quit the game
                sys.exit()  # Program exit
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the mouse click appears
                if login_rect.collidepoint(event.pos):
                    # If click inside the login box
                    login_active = True  # Activate the login field
                    password_active = False  # Deactivate the password field
                elif password_rect.collidepoint(event.pos):
                    # If click inside the password box
                    password_active = True  # Activate the password field
                    login_active = False  # Dctivate the login field
                elif show_password_rect.collidepoint(event.pos):
                    # If the button "Show" is pressed
                    show_password = not show_password  # Switch the show of the password
                else:
                    # Если клик вне полей ввода и кнопки
                    login_active = False  # Deactivate the login field
                    password_active = False  # Deactivate the password field
            if event.type == pygame.KEYDOWN:
                # if any key is pressed
                if login_active:
                    # If the login field is acitve
                    if event.key == pygame.K_BACKSPACE:
                        # If the backspace is pressed
                        login = login[:-1]  # Delete the last symbol of the login
                    else:
                        login += event.unicode  # Add the typed symbol to the password
                elif password_active:
                    # If the password field in active
                    if event.key == pygame.K_BACKSPACE:
                        # If the backspace is pressed
                        password = password[:-1]  # delete last password symbol
                    else:
                        password += event.unicode  # Add typed symbol to the password

                if event.key == pygame.K_RETURN and login and password:
                    # If enter is pressed
                    existing_password = check_existing_credentials(login, password)
                    # Check if there is a password like this
                    if existing_password is not None:
                        # If login already exists
                        if existing_password:
                            # If password is correct
                            return True
                        else:
                            # If password is incorrect
                            message = "This login already exists with a different password"
                    else:
                        # If login is new
                        with open('credentials.csv', 'a', newline='', encoding='utf-8') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([login, password])  # Log password and login into csv
                        message = "New user registered successfully!"
                        return True  # Return True with successful registration

            pygame.display.flip()  # Reload screen
            clock.tick(30)

    return False  # Return false in case of unsuccess authentication


authenticate()


# Function to display the "Main Menu" screen
def main_menu():
    global game_state  # Declare game_state global to modify it within the function

    # Fill the screen with background color
    screen.fill(SAND_COLOR)

    # Create a font for the text
    font = pygame.font.SysFont(None, 36)

    # Create text for various buttons and titles
    title_text = font.render('Main Menu', True, BLACK)  # Title text
    start_text = font.render('Start Game', True, BLACK)  # Start game button text
    exit_text = font.render('Exit', True, BLACK)  # Exit button text

    # Text placement on the screen
    title_rect = title_text.get_rect(center=(screen_size / 2, 100))
    start_rect = start_text.get_rect(center=(screen_size / 2, 200))
    exit_rect = exit_text.get_rect(center=(screen_size / 2, 250))

    # Drawing text on the screen
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(exit_text, exit_rect)

    # Mouse event handling
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the "Start Game" button is pressed
            if start_rect.collidepoint(pygame.mouse.get_pos()):
                game_state = LEVEL_SELECTION  # Transition to the level selection screen
                reset_game()
            # If the "Exit" button is pressed
            elif exit_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()  # Close Pygame
                sys.exit()  # Exit the program


def level_selection():
    global game_state, current_level  # Declare global variables

    screen.fill(SAND_COLOR)  # Clear the screen and set the background color
    font = pygame.font.SysFont(None, 36)  # Create a font

    # Create texts for each level
    level_texts = []
    for i in range(1, 6):
        level_text = font.render(f'Level {i}', True, BLACK)
        level_rect = level_text.get_rect(center=(screen_size / 2, 100 + i * 50))
        level_texts.append((level_text, level_rect))
        screen.blit(level_text, level_rect)

    # Event processing in a loop
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, (_, rect) in enumerate(level_texts):
                if rect.collidepoint(pygame.mouse.get_pos()):
                    # If a specific level is selected
                    current_level = i + 1
                    game_state = GAME_PLAYING  # Switch game state to playing mode

                    # Initialization of the selected level
                    if current_level == 1:
                        level_1()
                    elif current_level == 2:
                        level_2()
                    elif current_level == 3:
                        level_3()
                    elif current_level == 4:
                        level_4()
                    elif current_level == 5:
                        level_5()


def game_playing():
    try:
        global game_state, score, snake, fruit, special_fruit_counter, special_fruit_active, change_direction, obstacles

        # Key event processing
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and change_direction != "DOWN":
                    change_direction = "UP"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and change_direction != "UP":
                    change_direction = "DOWN"
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and change_direction != "RIGHT":
                    change_direction = "LEFT"
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and change_direction != "LEFT":
                    change_direction = "RIGHT"
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Drawing the background
        screen.fill(SAND_COLOR)
        draw_grid()  # Drawing the grid

        # Drawing obstacles
        for obstacle in obstacles:
            screen.blit(wall_block_img, (obstacle['x'] * cell_size, obstacle['y'] * cell_size))

        # Updating the head coordinates of the snake
        if change_direction == "UP":
            snake[0]["y"] -= cell_size
        elif change_direction == "DOWN":
            snake[0]["y"] += cell_size
        elif change_direction == "LEFT":
            snake[0]["x"] -= cell_size
        elif change_direction == "RIGHT":
            snake[0]["x"] += cell_size

        # Checking collision with screen borders
        if snake[0]["x"] >= screen_size:
            snake[0]["x"] = 0
        elif snake[0]["x"] < 0:
            snake[0]["x"] = screen_size - cell_size
        if snake[0]["y"] >= screen_size:
            snake[0]["y"] = 0
        elif snake[0]["y"] < 0:
            snake[0]["y"] = screen_size - cell_size

        # Checking collision with itself
        for segment in snake[1:]:
            if segment["x"] == snake[0]["x"] and segment["y"] == snake[0]["y"]:
                game_state = GAME_OVER

        # Checking fruit eating
        if snake[0]["x"] == fruit["x"] and snake[0]["y"] == fruit["y"]:
            score += 10
            special_fruit_counter += 1
            snake.append({"x": -1, "y": -1})
            fruit = {"x": random.randrange(1, screen_size // cell_size) * cell_size,
                        "y": random.randrange(1, screen_size // cell_size) * cell_size}
            # Play sound on fruit eating
            eat_sound.play()

        # Updating the coordinates of the snake's body
        for i in range(len(snake) - 1, 0, -1):
            snake[i]["x"] = snake[i - 1]["x"]
            snake[i]["y"] = snake[i - 1]["y"]

        # Drawing the body of the snake
        for segment in snake[1:]:
            screen.blit(snake_body_img, (segment['x'], segment['y']))

        # Drawing the head of the snake should be after drawing the body
        if len(snake) > 0:
            head_position = (snake[0]['x'], snake[0]['y'])
            screen.blit(snake_head_img, head_position)

        # Drawing the fruit
        screen.blit(current_fruit_img, (fruit["x"], fruit["y"]))

        # Checking collisions with obstacles
        for obstacle in obstacles:
            if snake[0]['x'] == obstacle['x'] * cell_size and snake[0]['y'] == obstacle['y'] * cell_size:
                game_state = GAME_OVER

        # Updating and displaying the score
        update_score()

        # Updating the screen
        pygame.display.flip()
    except Exception as e:
        print(f"Error in function game_playing: {e}")
        raise


# Function to update the score
def update_score():
    # Setting the font for displaying the score
    font = pygame.font.SysFont(None, 36)
    # Creating the text for displaying
    score_text = font.render(f'Score: {score}', True, BLACK)
    # Placing the text on the screen
    screen.blit(score_text, (10, 10))


def reset_game():
    global snake, score, fruit, game_state, snake_speed, change_direction, obstacles, special_fruit_active, current_level

    score = 0
    snake_speed = 10  # default value
    change_direction = "RIGHT"
    special_fruit_active = False
    snake = [{"x": 100, "y": 100}, {"x": 90, "y": 100}, {"x": 80, "y": 100}]  # Initial length of the snake
    fruit = {"x": random.randrange(1, screen_size // cell_size) * cell_size,
                "y": random.randrange(1, screen_size // cell_size) * cell_size}
    obstacles = []  # Reset obstacles

    # Level initialization depending on the selected level
    if current_level == 1:
        level_1()
    elif current_level == 2:
        level_2()
    elif current_level == 3:
        level_3()
    elif current_level == 4:
        level_4()
    elif current_level == 5:
        level_5()


# Function to display the "Game Over" screen
def game_over():
    global game_state
    # Playing the game over sound
    game_over_sound.play()
    # Clearing the screen and setting the background color
    screen.fill(SAND_COLOR)

    # Creating a font object for the text
    font = pygame.font.SysFont(None, 36)

    # Creating the text "Game Over. Score:" with the current score
    game_over_text = font.render(f'Game Over. Score: {score}', True, BLACK)

    # Creating the text "Play Again" for the "Play Again" button
    retry_text = font.render('Play Again', True, BLACK)

    # Creating the text "Exit to Menu" for the "Exit to Menu" button
    menu_text = font.render('Exit to Menu', True, BLACK)

    # Getting rectangles where the text will be displayed
    game_over_rect = game_over_text.get_rect(center=(screen_size / 2, 100))
    retry_rect = retry_text.get_rect(center=(screen_size / 2, 200))
    menu_rect = menu_text.get_rect(center=(screen_size / 2, 250))

    # Displaying the text on the screen
    screen.blit(game_over_text, game_over_rect)
    screen.blit(retry_text, retry_rect)
    screen.blit(menu_text, menu_rect)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if retry_rect.collidepoint(pygame.mouse.get_pos()):
                reset_game()  # Reset the game and start again at the current level
                game_state = GAME_PLAYING
            elif menu_rect.collidepoint(pygame.mouse.get_pos()):
                game_state = MAIN_MENU  # Return to the main menu


# Main game loop
while True:
    clock.tick(snake_speed)  # Control the frame rate

    if game_state == MAIN_MENU:
        main_menu()
    elif game_state == LEVEL_SELECTION:
        level_selection()
    elif game_state == GAME_PLAYING:
        game_playing()
    elif game_state == GAME_OVER:
        game_over()
    pygame.display.flip()

pygame.quit()

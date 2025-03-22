import requests
import pygame


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Texas Holdem Poker")

font = pygame.font.Font(None, 36)
username = ""
password = ""
server_url = "http://127.0.0.1:8000"

state = "login"
message = ""
room_id_input = ""

def draw_text(text, x, y):
    render = font.render(text, True, (0, 0, 0))
    screen.blit(render, (x, y))


def login_screen():
    screen.fill((255, 255, 255))
    draw_text(f"Enter username: {username}", 100, 100)
    draw_text("Enter password: ", 100, 150)
    draw_text("*"*len(password), 250, 150)
    draw_text("[Enter] Enter", 100, 200)
    draw_text("[R] Registration", 100, 250)
    draw_text("[G] Play as a guest", 100, 300)
    if message:
        draw_text(message, 100, 350, (255, 0, 0))


def get_rooms():
    response = requests.get(f"{server_url}/rooms")
    if response.status_code == 200:
        return response.json()
    return {}


def menu_screen():
    screen.fill((255, 255, 255))
    draw_text("Menu", 100, 100)
    draw_text("[C] Create Room", 100, 150)
    draw_text("[J] Join Room", 100, 200)
    draw_text("[L] List of rooms", 100, 250)


def join_room_screen():
    screen.fill((255, 255, 255))
    draw_text("Enter Room ID: " + room_id_input, 100, 100)
    draw_text("[Enter] Join Room", 100, 150)
    draw_text("[Esc] Cancel", 100, 200)


def game_loop():
    global state, username, password, message

    running = True
    input_field = "username"
    while running:
        screen.fill((255, 255, 255))
        if state == "login":
            login_screen()
        elif state == "menu":
            menu_screen()
        elif state == "join_room":
            join_room_screen()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if state == "login":
                    if event.key == pygame.K_RETURN:
                        response = requests.post(f"{server_url}/login", params={"username": username, "password": password})
                        if response.status_code == 200:
                            state = "menu"
                            message = ""
                        else:
                            message = "Login failed"
                    elif event.key == pygame.K_r:
                        requests.post(f"{server_url}/registr", params={"username": username, "password": password})
                        if response.status_code == 200:
                            message = "Registration successful"
                        else:
                            message = "Registration failed"
                    elif event.key == pygame.K_g:
                        response = requests.post(f"{server_url}/guest")
                        if response.status_code == 200:
                            state = "menu"
                            message = ""
                    elif event.key == pygame.K_BACKSPACE:
                        if input_field == "username":
                            username = username[:-1]
                        else:
                            password = password[:-1]
                    elif event.key == pygame.K_TAB:
                        input_field = "password" if input_field == "username" else "username"
                    elif event.unicode and event.unicode.isprintable():
                        if input_field == "username":
                            username += event.unicode
                        else:
                            password += event.unicode

                    elif state == "menu":
                        if event.key == pygame.K_c:
                            requests.post(f"{server_url}/create_room")
                        elif event.key == pygame.K_j:
                            state = "join_room"
                        elif event.key == pygame.K_l:
                            rooms = get_rooms()
                            print("Rooms:", rooms)

                    elif state == "join_room":
                        if event.key == pygame.K_RETURN:
                            if room_id_input.isdigit():
                                room_id = int(room_id_input)
                                rooms = get_rooms()
                                if room_id in rooms:
                                    response = requests.post(f"{server_url}/join_room", json={"user_id": username, "room_id": room_id})
                                    if response.status_code == 200:
                                        message = f"Joined Room {room_id}"
                                        state = "game"
                                    else:
                                        message = "Failed to join room"
                                else:
                                    message = "Room not found"
                            else:
                                message = "Invalid Room ID"
                        elif event.key == pygame.K_ESCAPE:
                            state = "menu"
                        elif event.unicode.isdigit():
                            room_id_input += event.unicode


game_loop()
pygame.quit()

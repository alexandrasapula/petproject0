from fastapi import FastAPI, HTTPException
from game_logic import deal_card
from models import Player, Room, User
from uuid import uuid4


app = FastAPI()
global_user = 0
global_room = 0
users = {}
rooms = {}


@app.post('/registr')
def registr(username: str, password: str):
    global global_user
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(name=username, password=password, id=global_user)
    users[global_user] = new_user
    global_user += 1
    return {"message": "User registered", "user_id": new_user.id}


@app.post('/guest')
def be_guest():
    global global_user
    new_user = User(name=str(uuid4()), password=str(uuid4()), id=global_user)
    users[global_user] = new_user
    global_user += 1
    return {"message": "Guest account created", "guest_id": new_user.id}


@app.post('/login')
def login(username, password):
    for user in users.values():
        if user.name == username:
            if user.password == password:
                return {"message": "Login successful", "user_id": user.id}
            else:
                raise HTTPException(status_code=400, detail="Incorrect password")
    raise HTTPException(status_code=404, detail="User not found")


@app.post('/create_room')
def create_room(user_id: int):
    global global_room
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    community_cards = []
    while len(community_cards) < 5:
        card = deal_card()
        if card not in community_cards:
            community_cards.append(card)
    creator = Player(username=users[user_id].name, id=user_id, balance=1000, hand=[], status='waiting')
    new_room = Room(room_id=global_room, players=[creator], status="waiting", pot=0, max_blind=4, min_blind=2, community_cards=community_cards, turn=0)
    rooms[global_room] = new_room
    global_room += 1
    return {"message": "Room created", "room_id": new_room.room_id}


@app.get('/rooms')
def get_rooms():
    availible_rooms = {room_id: room for room_id, room in rooms.items() if len(room.players) < 6}
    return availible_rooms


@app.post('/join_room')
def join_room(user_id: int, room_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    room = rooms[room_id]
    if len(room.players) >= 6:
        raise HTTPException(status_code=400, detail="Room is full")
    new_player = Player(username=users[user_id].name, id=user_id, balance=1000, hand=[], status='waiting')
    room.players.append(new_player)
    return {"message": "Joined room", "room_id": room_id, "user_id": user_id}


@app.get('room/{room_id}')
def get_room_state(room_id: int):
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    room = rooms[room_id]
    return room

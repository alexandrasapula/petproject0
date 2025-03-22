from typing import Literal
from pydantic import BaseModel, conlist


class Player(BaseModel):
    username: str
    id: int
    balance: int
    hand = conlist(str, min_items=2, max_items=2)
    status: Literal['waiting', 'in_game', 'on_bench', 'winner']


class Room(BaseModel):
    room_id: int
    players: list[Player]
    status: str
    pot: int
    max_blind: int
    min_blind: int
    community_cards = conlist(list[str], min_items=5, max_items=5)


class User(BaseModel):
    name: str
    password: str
    id: int

from ..models import User, users_collection


def get_users(filter = {}):
    users = users_collection.find(filter)
    return [User(**u) for u in users]


def get_user(id: int):
    user = users_collection.find_one({'_id': id})
    return User(**user) if user else None


def create_user(id: int, name: str, username: str):
    user = users_collection.insert_one(
        {'_id': id, 'name': name, 'username': username})
    return get_user(user.inserted_id)


def set_init_user(id: int, init: bool):
    users_collection.find_one_and_update(
        {'_id': id}, {'$set': {'isInit': init}}, return_document=True)

def set_xp_user(id: int, xp: int):
    users_collection.find_one_and_update(
        {'_id': id}, {'$set': {'xp': xp}}, return_document=True)

def get_userdata(id: int):
    return users_collection.find_one(
        {'_id': id})

def set_solved_user(id: int, solved: dict):
    users_collection.find_one_and_update(
        {'_id': id}, {'$set': {'solved': solved}}, return_document=True)

def get_solved_user(id: int):
    return get_user(id).solved

def get_init_user(id: int):
    return get_user(id).isInit


def update_user(id: int, name: str, username: str):
    user = users_collection.find_one_and_update(
        {'_id': id}, {'$set': {'name': name, 'username': username}}, return_document=True)
    return User(**user)


def get_or_create_user(id: int, name: str, username: str):
    user = get_user(id)
    if user:
        user = update_user(id, name, username)
    else:
        user = create_user(id, name, username)
    return user

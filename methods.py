import random
from cards_and_messages_DB import *


def add_to_lobby_with_id(lobby, member_id, username):
    lobby[username] = member_id


def get_str_of_members(members):
    return "\n".join(members)


def right_number_of_players(lobby_members):
    count_of_players = len(lobby_members)
    return (count_of_players <= 16) #and count_of_players >= 4)


def find_card_photo_path(card, member_random_cards):
    file_name = "JPG/" + str(card) + "/" + member_random_cards[card]
    return open(file_name, "rb")


def find_player_random_cards():
    cards = {
        "special": random.choice(special),
        "baggage": random.choice(baggage),
        "biology": random.choice(biology),
        "health": random.choice(health),
        "job": random.choice(job),
        "fact": random.choice(facts),
        "hobby": random.choice(hobby)
    }
    return cards


def get_catastrophe_path():
    path = "JPG/Катастрофа/" + random.choice(catastrophe)
    return path


def get_count_of_voting(round, count_of_members):

    list_of_voting = get_list_of_voting(count_of_members)
    # пример для 4х игроков [0, 0, 0, 1, 1]

    return list_of_voting[round-1]


def get_list_of_voting(count_of_members):

    count_of_staying = count_of_members // 2
    count_of_banned = count_of_members - count_of_staying

    list_of_voting = [0, 0, 0, 0, 0]
    for i in [4, 3, 2, 1, 4, 3, 2, 1, 4, 3, 2, 1, 4, 3, 2, 1]:
        if count_of_banned != 0:
            list_of_voting[i] += 1

            count_of_banned -= 1

    return list_of_voting


def get_key_of_max_in_dict(input_dict):
    max_value = max(input_dict.values())
    for key, value in input_dict.items():
        if value == max_value:
            return key


async def send_messages_for_all(bot, message, lobby):
    for player in lobby:
        id_ = lobby[player]
        await bot.send_message(id_, message)


async def send_messages_for_all_with_markup(bot, message, lobby, markup):
    for player in lobby:
        id_ = lobby[player]
        await bot.send_message(id_, message, reply_markup=markup)
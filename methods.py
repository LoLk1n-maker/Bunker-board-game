import random
from cards_and_messages import *
from aiogram import types

# Handlers Methods
def add_to_lobby_with_id(lobby, member_id, username):
    lobby[username] = member_id

def player_in_lobby(username, lobby):
    return username in lobby

def player_is_admin(username, admin):
    return username == admin

async def send_round_panel(bot, id, message):
    round_markup = create_round_keyboard()
    await bot.send_message(id, message, reply_markup=round_markup)

def create_round_keyboard():
    round_markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("1", callback_data="1")
    button2 = types.InlineKeyboardButton("2", callback_data="2")
    button3 = types.InlineKeyboardButton("3", callback_data="3")
    button4 = types.InlineKeyboardButton("4", callback_data="4")
    button5 = types.InlineKeyboardButton("5", callback_data="5")
    round_markup.add(button1, button2, button3, button4, button5)
    return round_markup


# path Methods
def find_card_photo_path(card, member_random_cards):
    file_name = "JPG/" + str(card) + "/" + member_random_cards[card]
    return open(file_name, "rb")

def get_catastrophe_path():
    return "JPG/Катастрофа/" + random.choice(catastrophe)


# just chill method, don't touch him pls
def get_key_of_max_in_dict(input_dict):
    max_value = max(input_dict.values())
    for key, value in input_dict.items():
        if value == max_value:
            return key


# sending methods
async def send_messages_for_all(bot, message, lobby):
    for player in lobby:
        id_ = lobby[player]
        await bot.send_message(id_, message)

async def send_messages_for_all_with_markup(bot, message, lobby, markup):
    for player in lobby:
        id_ = lobby[player]
        await bot.send_message(id_, message, reply_markup=markup)


# MEGA SUPER DUPER CLASSES FOR GAME
class VotingMethods:
    def __init__(self, bot, this_round, players, dp):
        self.bot = bot
        self.this_round = this_round
        self.players = players
        self.dp = dp
        self.count_of_members = len(players)

    async def first_voting(self, zero_voting_message):
        for player in self.players:
            id = self.players[player]
            await self.bot.send_message(id, zero_voting_message)

    def get_list_of_voting(self):
        count_of_staying = self.count_of_members // 2
        count_of_banned = self.count_of_members - count_of_staying

        list_of_voting = [0, 0, 0, 0, 0]
        for i in [4, 3, 2, 1, 4, 3, 2, 1, 4, 3, 2, 1, 4, 3, 2, 1]:
            if count_of_banned != 0:
                list_of_voting[i] += 1

                count_of_banned -= 1

        return list_of_voting

    def get_count_of_voting(self):

        list_of_voting = self.get_list_of_voting()
        # пример для 4х игроков [0, 0, 0, 1, 1]

        return list_of_voting[self.this_round - 1]

    def create_voting_keyboard(self):

        markup = types.InlineKeyboardMarkup()
        for player in self.players:
            button = types.InlineKeyboardButton(text=player, callback_data=player)
            markup.add(button)

        return markup

    async def send_voting(self):
        voting_markup = self.create_voting_keyboard()
        await send_messages_for_all_with_markup(self.bot, "Голосование", self.players, voting_markup)

    def create_vote_dict(self):
        number_of_votes = {}
        for player in self.players:
            number_of_votes[player] = 0

        return number_of_votes

    def get_number_of_votes(self, number_of_votes, callback):
        for member in self.players:
            if callback.data == member:
                number_of_votes[member] += 1
        return number_of_votes

    def get_result_message(self, number_of_votes):

        results_message = get_results_message(number_of_votes)
        kicked_player = get_key_of_max_in_dict(number_of_votes)

        if self.without_loosers(number_of_votes):
            return f"Результаты голосования:\n{results_message}\n\n" + without_loosers_message
        else:
            return f"Результаты голосования:\n{results_message}\n\n\n" + get_with_looser_message(kicked_player)

    def everyone_voted(self, voted):
        return voted == len(self.players)

    def without_loosers(self, number_of_votes):
        temp_list_of_votes = []
        for member in number_of_votes:
            temp_list_of_votes.append(number_of_votes[member])

        return len(set(temp_list_of_votes)) != len(temp_list_of_votes)

    def kick_looser(self, number_of_votes):
        kicked_player = get_key_of_max_in_dict(number_of_votes)
        del self.players[kicked_player]
        print(f"{kicked_player} был изгнан)")

    def without_vote(self, count_of_votings):
        return count_of_votings == 0


class GameMethods:
    def __init__(self, lobby):
        self.lobby = lobby

    def right_number_of_players(self):
        count_of_players = len(self.lobby)
        return count_of_players <= 16  # and count_of_players >= 4 #Стоит здесь временно ибо как мне в соло тестить то

    def find_player_random_cards(self):
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

    def create_cards_group(self, player_random_cards):
        cards_photo_group = types.MediaGroup()
        for card in player_random_cards:
            card_path = find_card_photo_path(card, player_random_cards)
            cards_photo_group.attach_photo(card_path)
        return cards_photo_group
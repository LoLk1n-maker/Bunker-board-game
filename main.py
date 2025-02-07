from aiogram import Bot, Dispatcher, executor, types

from config import token
from messeges import *
from methods import *
from keyboards import *
#from game import start_bunker
#from messege_handlers import register_handlers


bot = Bot(token)
dp = Dispatcher(bot)

lobby_members = {}

number_of_votes = {}

voted = 0


async def send_messages_for_all(message, lobby):
    for player in lobby:
        id_ = lobby[player]
        await bot.send_message(id_, message)


async def send_messages_for_all_with_markup(message, lobby, markup):
    for player in lobby:
        id_ = lobby[player]
        await bot.send_message(id_, message, reply_markup=markup)


async def send_round_panel(id, message):

    round_markup = create_round_keyboard()

    await bot.send_message(id, message, reply_markup=round_markup)
    return

@dp.message_handler(commands=["start"])
async def starting(message: types.Message):
    await bot.send_message(message.chat.id, hello_message)

@dp.message_handler(commands=["join_lobby"])
async def joining_to_lobby(message: types.Message):
    global lobby_members
    add_to_lobby_with_id(lobby_members, message.chat.id, message.chat.username)
    str_of_members = get_str_of_members(lobby_members)

    await send_messages_for_all(join_to_lobby_message1 + str(len(lobby_members)) + join_to_lobby_message2 + str_of_members, lobby_members)


@dp.message_handler(commands=["new_game"])
async def creating_new_game(message: types.Message):
    global lobby_members
    lobby_members = {}
    await bot.send_message(message.chat.id, creating_game_message)


@dp.message_handler(commands=["rules"])
async def giving_the_rules(message: types.Message):
    photo_group = types.MediaGroup()

    for index_of_rule_page in range(1,9):
        file_name = "rules/" + str(index_of_rule_page) + ".jpg"
        rule_photo = open(file_name, "rb")
        photo_group.attach_photo(rule_photo)
    await bot.send_media_group(message.chat.id, photo_group)


@dp.message_handler(commands=["start_game"])
async def starting_game(message: types.Message):
    global lobby_members

    await send_round_panel(message.chat.id, "Раунды")
    await send_messages_for_all("GAME!!!!!", lobby_members)
    await start_bunker(lobby_members)


async def start_bunker(players):

    global round_ends

    #0 Проверка кол-ва игроков
    if not right_number_of_players(players):
        await send_messages_for_all(wrong_count_of_players_message, players)
        return

    # 1 получение катастрофы
    await know_catastrophe(players)

    # 2 получение карт
    await sending_photos(players)

    # 3 деление игры на раунды(их всегда 5, но голосований разное количество)

    @dp.callback_query_handler(lambda query: query.data.isdigit())
    async def change_round(callback: types.CallbackQuery):
        this_round = int(callback.data[0])

        # 4 голосования

        await voting(this_round, players)
        this_round += 1


async def know_catastrophe(players):
    bunker_path = get_catastrophe_path()

    #здесь почему-то происходит и/о ошибка, даже если файл не закрывается вовсе, или если использовать клоуз
    #photo_bunker = types.MediaGroup()
    #img1 = open(bunker_path, "rb")
    #photo_bunker.attach_photo(img1)

    for player in players:
        id = players[player]
        await bot.send_message(id, catastrophe_message)
        #await bot.send_media_group(id, photo_bunker)
        await bot.send_photo(id, open(bunker_path, "rb"))

    #img1.close()


async def sending_photos(players):
    for player in players:
        cards_photo_group = types.MediaGroup()

        player_random_cards = find_player_random_cards()
        for card in player_random_cards:
            card_path = find_card_photo_path(card, player_random_cards)
            cards_photo_group.attach_photo(card_path)

        id = players[player]
        await bot.send_message(id, receiving_cards_message)
        await bot.send_media_group(id, cards_photo_group)


async def voting(this_round, players):
    # Количество голосований в раунде иожет быть разным
    async def votings_n_times(n, players):
        for vote in range(n):
            await start_1_voting(players)

    # В первом раунде голосование не проводится никогда
    async def zero_voting(players):
        for player in players:
            id = players[player]
            await bot.send_message(id, zero_voting_message)

    if this_round == 1:
        await zero_voting(players)
        return

    count_of_votings = get_count_of_voting(this_round, len(players))
    await votings_n_times(count_of_votings, players)


async def start_1_voting(players):
    global number_of_votes
    print("голосование")

    async def send_voting(players):
        voting_markup = create_voting_keyboard(players)
        await send_messages_for_all_with_markup("Голосование", players, voting_markup)

    def create_vote_dict():
        number_of_votes = {}
        for player in players:
            number_of_votes[player] = 0

        return number_of_votes

    await send_voting(players)
    number_of_votes = create_vote_dict()

    @dp.callback_query_handler(lambda query: not query.data.isdigit())
    async def count_votes(callback: types.CallbackQuery):
        global lobby_members, number_of_votes, voted
        voted += 1

        def get_number_of_votes(number_of_votes, lobby):
            for member in lobby:
                if callback.data == member:
                    number_of_votes[member] += 1
            return number_of_votes

        def get_result_message(number_of_votes):
            results_list = ''
            for member in number_of_votes:
                results_list += member + " " + str(number_of_votes[member]) + " " + "голосов\n"
            kicked_player = get_key_of_max_in_dict(number_of_votes)

            if without_loosers(number_of_votes):
                return f"вот р-ты:\n{results_list}\n\n"+without_loosers_message
            else:
                return f"вот р-ты:\n{results_list}\n\n\n{kicked_player} сочли недостойным бункера :3\nОтправляйся восвояси"

        def everyone_voted(voted, lobby):
            return voted == len(lobby)

        def without_loosers(number_of_votes):
            temp_list_of_votes = []
            for member in number_of_votes:
                temp_list_of_votes.append(number_of_votes[member])

            return len(set(temp_list_of_votes)) != len(temp_list_of_votes)

        number_of_votes = get_number_of_votes(number_of_votes, lobby_members)
        results_message = get_result_message(number_of_votes)

        if everyone_voted(voted, lobby_members):
            await send_messages_for_all(results_message, lobby_members)
            voted = 0


executor.start_polling(dp)

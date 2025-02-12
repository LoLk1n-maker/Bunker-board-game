from methods import *


voted = 0
zero_votes = {}


async def start_bunker(bot, players, dp):

    # 0 Проверка кол-ва игроков
    if not right_number_of_players(players):
        await send_messages_for_all(bot, wrong_count_of_players_message, players)
        return

    # 1 получение катастрофы
    await know_catastrophe(bot, players)

    # 2 получение карт
    await sending_photos(bot, players)

    # 3 деление игры на раунды(их всегда 5, но голосований разное количество)

    @dp.callback_query_handler(lambda query: query.data.isdigit())
    async def change_round(callback: types.CallbackQuery):
        this_round = int(callback.data[0])
        print(f"------------------------{this_round}_раунд-------------------------------")
        # 4 голосования

        await voting(bot, this_round, players, dp)
        this_round += 1


async def know_catastrophe(bot, players):
    bunker_path = get_catastrophe_path()

    # здесь почему-то происходит и/о ошибка, даже если файл не закрывается вовсе, или если использовать клоуз
    # photo_bunker = types.MediaGroup()
    # img1 = open(bunker_path, "rb")
    # photo_bunker.attach_photo(img1)

    for player in players:
        id = players[player]
        await bot.send_message(id, catastrophe_message)
        # await bot.send_media_group(id, photo_bunker)
        await bot.send_photo(id, open(bunker_path, "rb"))

    # img1.close()


async def sending_photos(bot, players):
    for player in players:
        cards_photo_group = types.MediaGroup()

        player_random_cards = find_player_random_cards()
        # выводим карты игроков, на случай если необходима проверка игрока(например есть подозрения в обмане)
        print(f"Карты игрока {player}:\n{player_random_cards}\n")

        for card in player_random_cards:
            card_path = find_card_photo_path(card, player_random_cards)
            cards_photo_group.attach_photo(card_path)

        id = players[player]
        await bot.send_message(id, receiving_cards_message)
        await bot.send_media_group(id, cards_photo_group)


async def voting(bot, this_round, players, dp):

    voting = votingMethods(bot, this_round, players, dp)

    # Количество голосований в раунде иожет быть разным
    async def votings_n_times(n, players):
        for vote in range(n):
            await start_1_voting(bot, players, dp, voting)

    # В первом раунде голосование не проводится никогда
    # async def first_voting(players):
    #     for player in players:
    #         id = players[player]
    #         await bot.send_message(id, zero_voting_message)

    def get_without_vote_message():
        return f"В этом раунде ({this_round}) голосования не будет\nТак что еще можете надеяться"

    if this_round == 1:
        await voting.first_voting(zero_voting_message)
        return

    count_of_votings = voting.get_count_of_voting()
    if count_of_votings == 0:
        await send_messages_for_all(bot, get_without_vote_message(), players)
    else:
        await votings_n_times(count_of_votings, players)

async def start_1_voting(bot, players, dp, voting):

    # async def send_voting(players):
    #     voting_markup = create_voting_keyboard(players)
    #     await send_messages_for_all_with_markup(bot, "Голосование", players, voting_markup)

    # def create_vote_dict():
    #     number_of_votes = {}
    #     for player in players:
    #         number_of_votes[player] = 0
    #
    #     return number_of_votes

    global zero_votes
    print("голосование")

    voted = 0

    await voting.send_voting()
    zero_votes = voting.create_vote_dict()

    @dp.callback_query_handler(lambda query: not query.data.isdigit())
    async def count_votes(callback: types.CallbackQuery):

        # def get_number_of_votes(number_of_votes, lobby):
        #     for member in lobby:
        #         if callback.data == member:
        #             number_of_votes[member] += 1
        #     return number_of_votes
        #
        # def get_result_message(number_of_votes):
        #     results_list = ''
        #     for member in number_of_votes:
        #         results_list += member + " " + str(number_of_votes[member]) + " " + "голосов\n"
        #     kicked_player = get_key_of_max_in_dict(number_of_votes)
        #
        #     if without_loosers(number_of_votes):
        #         return f"вот р-ты:\n{results_list}\n\n"+without_loosers_message
        #     else:
        #         return f"вот р-ты:\n{results_list}\n\n\n{kicked_player} сочли недостойным бункера :3\nОтправляйся восвояси"
        #
        # def everyone_voted(voted, lobby):
        #     return voted == len(lobby)
        #
        # def without_loosers(number_of_votes):
        #     temp_list_of_votes = []
        #     for member in number_of_votes:
        #         temp_list_of_votes.append(number_of_votes[member])
        #
        #     return len(set(temp_list_of_votes)) != len(temp_list_of_votes)
        #
        # def kick_looser():
        #     kicked_player = get_key_of_max_in_dict(number_of_votes)
        #     del players[kicked_player]
        #     print(f"{kicked_player} был изгнан)")

        global voted, zero_votes

        voted += 1

        number_of_votes = voting.get_number_of_votes(zero_votes, callback)
        results_message = voting.get_result_message(number_of_votes)

        if voting.everyone_voted(voted):

            await send_messages_for_all(bot, results_message, players)
            voting.kick_looser(number_of_votes)

            voted = 0
            zero_votes = voting.create_vote_dict()


# def create_voting_keyboard(players):
#
#     markup = types.InlineKeyboardMarkup()
#     for player in players:
#         button = types.InlineKeyboardButton(text=player, callback_data=player)
#         markup.add(button)
#
#     return markup

from methods import *


voted = 0
zero_votes = {}
already_vote = []

async def start_bunker(bot, players, dp):
    bunker = GameM(players)
    players_in_begin = players.copy() # костыль чтобы не переписывать хранения пользователей

    # 0 Проверка кол-ва игроков
    if not bunker.right_number_of_players():
        await send_messages_for_players(bot, wrong_count_of_players_message, players)
        return

    # 1 получение катастрофы
    await send_catastrophy(bot, players)

    # 2 получение карт
    await send_cards(bot, players)

    #3 Раздача 5-ти карт о бункере    -    видимо нужно только для финала
    #bunker_cards = bunker.get_list_of_cards_about_bunker()

    # 4 деление игры на раунды(их всегда 5, но голосований разное количество)
    await send_messages_for_players(bot, first_round_message, players)

    @dp.callback_query_handler(lambda query: query.data.isdigit())
    async def change_round(callback: types.CallbackQuery):

        current_round = int(callback.data[0])
        print(f"------------------------{current_round}_раунд-------------------------------")

        #3.1 Раздаем по карте о бункере в начале каждого раунда     -    видимо нужно только для финала
        #await send_1_card_about_bunker(bot, players, current_round, bunker_cards)

        # 5 голосования
        await voting(bot, current_round, players, dp)

        await end_of_round(bot, players, current_round, players_in_begin)


#1
async def send_catastrophy(bot, players):
    bunker_path = get_catastrophe_path()

    for player in players:
        id = players[player]
        await bot.send_message(id, catastrophe_message)
        await bot.send_photo(id, open(bunker_path, "rb"))


#2
async def send_cards(bot, players): # очистить

    for player in players:
        player_cards = GameM.find_player_random_cards()

        # выводим карты игроков, на случай если необходима проверка игрока(например есть подозрения в обмане)
        print(f"Карты игрока {player}:\n{player_cards}\n")

        cards_photo_group = GameM.create_cards_group(player_cards)

        id = players[player]
        await bot.send_message(id, receiving_cards_message)
        await bot.send_media_group(id, cards_photo_group)


#3
async def send_1_card_about_bunker(bot, players, current_round, bunker_cards):
    bunker_card = bunker_cards[current_round-1]
    for player in players:
        id = players[player]
        await bot.send_message(id, "Раскрылась деталь о бункере:")
        await bot.send_photo(id, open(bunker_card, "rb"))


#5
async def voting(bot, this_round, players, dp):

    voting = VotingM(bot, this_round, players, dp)

    #Проверяем раунд, и понимаем проволить ли голосование или нет
    if this_round == 0:
        return
    elif this_round == 1:
        await voting.first_voting(zero_voting_message)
    else:
        await start_voting(voting, bot, dp, players, this_round)


async def start_voting(voting, bot, dp, players, this_round):

    count_of_voting = voting.get_count_of_voting()

    if VotingM.without_vote(count_of_voting):
        await send_messages_for_players(bot, get_without_vote_message(this_round), players)

    else:

        # Количество голосований в раунде иожет быть разным
        async def votings_n_times(n):
            for vote in range(n):
                await start_1_voting(bot, players, dp, voting)

        await votings_n_times(count_of_voting)


async def start_1_voting(bot, players, dp, voting):
    global zero_votes, already_vote

    #Проверяем чтобы человек не мог проголосовать больше одного раза - урод такой челобрек

    voted = 0

    await voting.send_voting()
    zero_votes = voting.create_vote_dict()

    @dp.callback_query_handler(lambda query: not query.data.isdigit())
    async def somebody_vote(callback: types.CallbackQuery):
        global voted, zero_votes
        player = callback.from_user.username

        if voting.player_didnt_vote(player, already_vote):

            print(f"{player} проголосовал за {callback.data}")

            voted += 1

            await count_the_voting_results(bot, voting, players, callback)
            voting.player_already_vote(player, already_vote)

        else:
            await callback.answer("Уже голосовал!")

    already_vote = []


async def count_the_voting_results(bot, voting, players, callback):
    global voted, zero_votes
    number_of_votes = voting.get_number_of_votes(zero_votes, callback)

    if voting.everyone_voted(players, voted):

        results_message = voting.get_result_message(number_of_votes)

        if VotingM.without_loosers(number_of_votes):
            await send_messages_for_players(bot, results_message, players)
            await voting.send_to_kicked(results_message)
            # в разработке
        else:
            await send_messages_for_players(bot, results_message, players)
            await voting.send_to_kicked(results_message)

            voting.kick_looser(number_of_votes)

        voted = 0
        zero_votes = voting.create_vote_dict()



#4
async def end_of_round(bot, players, current_round, players_in_begin):

    if GameM.game_ends(current_round):
        await send_messages_for_players(bot, get_final_message(players), players_in_begin)
    elif current_round == 5:
        # without next round message
        pass
    else:
        await send_messages_for_players(bot, f"Начало {current_round + 1}го раунда", players_in_begin)
        current_round += 1

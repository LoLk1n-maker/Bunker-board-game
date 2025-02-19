from methods import *


voted = 0
zero_votes = {}


async def start_bunker(bot, players, dp):
    bunker = GameM(players)

    # 0 Проверка кол-ва игроков
    if not bunker.right_number_of_players():
        await send_messages_for_players(bot, wrong_count_of_players_message, players)
        return

    # 1 получение катастрофы
    await send_catastrophy(bot, players)

    # 2 получение карт
    await send_cards(bot, players)

    # 3 деление игры на раунды(их всегда 5, но голосований разное количество)
    await send_messages_for_players(bot, f"Начало 1го раунда", players
                                    )
    @dp.callback_query_handler(lambda query: query.data.isdigit())
    async def change_round(callback: types.CallbackQuery):

        current_round = int(callback.data[0])
        print(f"------------------------{current_round}_раунд-------------------------------")
        # 4 голосования
        await start_voting(bot, current_round, players, dp)

        if GameM.game_ends(current_round):
            await send_messages_for_players(bot, get_final_message(players), players)
            return
        elif current_round == 5:
            # without next round message
            return
        else:
            await send_messages_for_players(bot, f"Начало {current_round + 1}го раунда", players)
            current_round += 1
    return


async def send_catastrophy(bot, players):
    bunker_path = get_catastrophe_path()

    for player in players:
        id = players[player]
        await bot.send_message(id, catastrophe_message)
        await bot.send_photo(id, open(bunker_path, "rb"))


async def send_cards(bot, players): # очистить

    for player in players:
        player_cards = GameM.find_player_random_cards()

        # выводим карты игроков, на случай если необходима проверка игрока(например есть подозрения в обмане)
        print(f"Карты игрока {player}:\n{player_cards}\n")

        cards_photo_group = GameM.create_cards_group(player_cards)

        id = players[player]
        await bot.send_message(id, receiving_cards_message)
        await bot.send_media_group(id, cards_photo_group)


async def start_voting(bot, this_round, players, dp):

    voting = VotingM(bot, this_round, players, dp)
    if this_round == 0:
        return
    elif this_round == 1:
        await voting.first_voting(zero_voting_message)
    else:
        count_of_votings = voting.get_count_of_voting()

        if VotingM.without_vote(count_of_votings):
            await send_messages_for_players(bot, get_without_vote_message(this_round), players)
        else:
            # Количество голосований в раунде иожет быть разным
            async def votings_n_times(n):
                for vote in range(n):
                    await start_1_voting(bot, players, dp, voting)

            await votings_n_times(count_of_votings)


async def start_1_voting(bot, players, dp, voting):
    global zero_votes

    voted = 0

    await voting.send_voting()
    zero_votes = voting.create_vote_dict()

    @dp.callback_query_handler(lambda query: not query.data.isdigit())
    async def count_votes(callback: types.CallbackQuery):

        global voted, zero_votes

        print(f"{callback.from_user.username} проголосовал за {callback.data}")

        voted += 1
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
            return


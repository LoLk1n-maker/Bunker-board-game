from methods import *
from game import start_bunker

lobby_members = {}
admin = ""


async def register_handlers(dp, bot):

    @dp.message_handler(commands=["start"])
    async def starting(message: types.Message):
        await bot.send_message(message.chat.id, hello_message)

    @dp.message_handler(commands=["join_lobby"])
    async def joining_to_lobby(message: types.Message):
        global lobby_members, admin

        if HandlerM.player_in_lobby(message.chat.username, lobby_members):
            await bot.send_message(message.chat.id, already_in_lobby_message)
        elif lobby_members == {}:
            await bot.send_message(message.chat.id, without_lobby_message)
        else:
            HandlerM.add_to_lobby_with_id(lobby_members, message.chat.id, message.chat.username)

            await send_messages_for_players(bot, get_joining_message(lobby_members, admin), lobby_members)

    @dp.message_handler(commands=["new_game"])
    async def creating_new_game(message: types.Message):
        global lobby_members, admin

        lobby_members = {}
        admin = message.chat.username
        HandlerM.add_to_lobby_with_id(lobby_members, message.chat.id, message.chat.username)
        str_of_members = get_str_of_members(lobby_members.copy(), admin)

        await bot.send_message(message.chat.id, "Ты сейчас админ этого лобби\nВот лобби сейчас:" + str_of_members + creating_game_message)

    @dp.message_handler(commands=["rules"])
    async def giving_the_rules(message: types.Message):

        def add_rules_to_group():
            for index_of_rule_page in range(1, 9):
                file_name = "rules/" + str(index_of_rule_page) + ".jpg"
                rule_photo = open(file_name, "rb")
                photo_group.attach_photo(rule_photo)

        photo_group = types.MediaGroup()
        add_rules_to_group()

        await bot.send_media_group(message.chat.id, photo_group)

    @dp.message_handler(commands=["start_game"])
    async def starting_game(message: types.Message):
        global lobby_members, admin

        # Player_...
        p_username = message.chat.username
        p_id = message.chat.id

        if HandlerM.player_in_lobby(p_username, lobby_members):
            if HandlerM.player_is_admin(p_username, admin):
                async def start():
                    await HandlerM.send_round_panel(bot, p_id, round_message)
                    await send_messages_for_players(bot, "STARTING GAME!!!!!", lobby_members)
                    await start_bunker(bot, lobby_members, dp)
                await start()
            else:
                await bot.send_message(p_id, get_not_admin_message(admin))
        else:
            await bot.send_message(p_id, without_lobby_message)

    @dp.message_handler(commands=['cleanup'])
    async def cleanup_handler(message: types.Message):
        chat_id = message.chat.id

        # Получаем последние сообщения в чате (достаточно 1, если уверены, что только одно)
        messages = await bot.get_updates(offset=-1, limit=1)

        if messages:
            last_message = messages[0].message

            for id in range(35):
                try:
                    await bot.delete_message(chat_id=chat_id, message_id=last_message.message_id - id)
                except Exception as e:
                    print(f"Ошибка при удалении сообщения: {e}")
        else:
            print("В чате нет сообщений.")

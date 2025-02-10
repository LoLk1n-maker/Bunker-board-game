from aiogram import types
from methods import *
from game import start_bunker

lobby_members = {}


async def register_handlers(dp, bot):

    @dp.message_handler(commands=["start"])
    async def starting(message: types.Message):
        await bot.send_message(message.chat.id, hello_message)

    @dp.message_handler(commands=["join_lobby"])
    async def joining_to_lobby(message: types.Message):
        global lobby_members
        add_to_lobby_with_id(lobby_members, message.chat.id, message.chat.username)
        str_of_members = get_str_of_members(lobby_members)

        await send_messages_for_all(bot, join_to_lobby_message1 + str(len(lobby_members)) + join_to_lobby_message2 + str_of_members, lobby_members)

    @dp.message_handler(commands=["new_game"])
    async def creating_new_game(message: types.Message):
        global lobby_members
        lobby_members = {}
        await bot.send_message(message.chat.id, creating_game_message)

    @dp.message_handler(commands=["rules"])
    async def giving_the_rules(message: types.Message):
        photo_group = types.MediaGroup()

        for index_of_rule_page in range(1, 9):
            file_name = "rules/" + str(index_of_rule_page) + ".jpg"
            rule_photo = open(file_name, "rb")
            photo_group.attach_photo(rule_photo)
        await bot.send_media_group(message.chat.id, photo_group)

    @dp.message_handler(commands=["start_game"])
    async def starting_game(message: types.Message):
        global lobby_members

        async def send_round_panel(id, message):
            round_markup = create_round_keyboard()

            await bot.send_message(id, message, reply_markup=round_markup)
            return


        await send_round_panel(message.chat.id, "Раунды")
        await send_messages_for_all(bot, "GAME!!!!!", lobby_members)
        await start_bunker(bot, lobby_members, dp)

    @dp.message_handler(commands=['cleanup'])
    async def cleanup_handler(message: types.Message):
        chat_id = message.chat.id

        # Получаем последние сообщения в чате (достаточно 1, если уверены, что только одно)
        messages = await bot.get_updates(offset=-1, limit=1)

        if messages:
            last_message = messages[0].message
            print(messages)
            print(last_message.message_id)
            for id in range(10000):
                try:
                    await bot.delete_message(chat_id=chat_id, message_id=id)
                except Exception as e:
                    print(f"Ошибка при удалении сообщения: {e}")
        else:
            print("В чате нет сообщений.")




def create_round_keyboard():
    round_markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("1", callback_data="1")
    button2 = types.InlineKeyboardButton("2", callback_data="2")
    button3 = types.InlineKeyboardButton("3", callback_data="3")
    button4 = types.InlineKeyboardButton("4", callback_data="4")
    button5 = types.InlineKeyboardButton("5", callback_data="5")
    round_markup.add(button1, button2, button3, button4, button5)
    return round_markup
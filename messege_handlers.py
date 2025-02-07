from aiogram import types
from messeges import *
from methods import *
from config import send_messages_for_all
from keyboards import create_round_keyboard
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
token = '_'


async def send_messages_for_all(bot, message, lobby):
    for player in lobby:
        id_ = lobby[player]
        await bot.send_message(id_, message)


async def send_messages_for_all_with_markup(bot, message, lobby, markup):
    for player in lobby:
        id_ = lobby[player]
        await bot.send_message(id_, message, reply_markup=markup)


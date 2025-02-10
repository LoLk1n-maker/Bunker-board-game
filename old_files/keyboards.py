from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_voting_keyboard(players):
    markup = InlineKeyboardMarkup()
    for player in players:
        button = InlineKeyboardButton(text=player, callback_data=player)
        markup.add(button)
    return markup


def create_round_keyboard():
    round_markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("1", callback_data="1")
    button2 = InlineKeyboardButton("2", callback_data="2")
    button3 = InlineKeyboardButton("3", callback_data="3")
    button4 = InlineKeyboardButton("4", callback_data="4")
    button5 = InlineKeyboardButton("5", callback_data="5")
    round_markup.add(button1, button2, button3, button4, button5)
    return round_markup

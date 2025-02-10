import sqlite3

def load_cards_from_db():
    conn = sqlite3.connect('cards.db')
    cursor = conn.cursor()

    data = {}
    table_names = ['baggage', 'biology', 'health', 'special', 'job', 'facts', 'hobby', 'catastrophe', 'bunkers']

    for table_name in table_names:
        cursor.execute(f"SELECT card_name FROM {table_name}")
        cards = [row[0] for row in cursor.fetchall()]
        data[table_name] = cards

    conn.close()
    return data

card_data = load_cards_from_db()

#формируем списки карт
baggage = card_data['baggage']
biology = card_data['biology']
health = card_data['health']
special = card_data['special']
job = card_data['job']
facts = card_data['facts']
hobby = card_data['hobby']
catastrophe = card_data['catastrophe']
bunkers = card_data['bunkers']


def load_messages_from_database():
    filename = "messages.db"
    with sqlite3.connect(filename) as conn:

        # conn = sqlite3.connect(filename)
        cursor = conn.cursor()

        cursor.execute("SELECT message_name, message_text FROM messages")
        messages = cursor.fetchall()

        # conn.close()

    global_vars = {}
    for message_name, message_text in messages:
        global_vars[message_name] = message_text

    return global_vars


messages = load_messages_from_database()

# формируем сообщения
without_loosers_message = messages["without_loosers_message"]
hello_message = messages['hello_message']
join_to_lobby_message1 = messages['join_to_lobby_message1']
join_to_lobby_message2 = messages['join_to_lobby_message2']
zero_voting_message = messages['zero_voting_message']
voting_message = messages['voting_message']
creating_game_message = messages['creating_game_message']
receiving_cards_message = messages['receiving_cards_message']
catastrophe_message = messages['catastrophe_message']
wrong_count_of_players_message = messages['wrong_count_of_players_message']




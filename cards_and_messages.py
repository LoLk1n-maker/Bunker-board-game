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
        cursor = conn.cursor()
        cursor.execute("SELECT message_name, message_text FROM messages")
        messages = cursor.fetchall()

    global_vars = {}
    for message_name, message_text in messages:
        new_message_text = message_text.replace(r'\n', '\n')#т к из базы данных строка идет сырая
        global_vars[message_name] = new_message_text

    return global_vars


messages = load_messages_from_database()

# формируем сообщения
without_loosers_message = messages["without_loosers_message"]
hello_message = messages['hello_message']
zero_voting_message = messages['zero_voting_message']
voting_message = messages['voting_message']
creating_game_message = messages['creating_game_message']
receiving_cards_message = messages['receiving_cards_message']
catastrophe_message = messages['catastrophe_message']
wrong_count_of_players_message = messages['wrong_count_of_players_message']

already_in_lobby_message = "Ты уже в лобби🤡🤡🤡"
round_message = "Раунды:\n" \
                "Нажимать в конце соответствующего раунда▶"
without_lobby_message = "Лобби еще нет, его нужно создать.\n" \
                        "Команду я дам: /new_game\n" \
                        "Друзей. я. не. дам"

def get_not_admin_message(admin):
    return f"Чтобы начать игру ты должен быть админом\n👑" \
           f"Админ сейчас - {admin}"

def get_without_vote_message(this_round):
    return f"В {this_round}м раунде голосования не будет\n" \
           f"Надежда есть"

def get_with_looser_message(kicked_player):
    return f"{kicked_player} сочли недостойным бункера:3\n" \
           f"Отправляйся восвояси"

def get_results_message(number_of_votes):
    results_list = ''
    for member in number_of_votes:
        results_list += member + " " + str(number_of_votes[member]) + " " + "голосов\n"
    return results_list

def get_str_of_members(members, admin):

    admin_str = admin + "👑\n"
    del members[admin]
    members_without_admin = members

    return admin_str + "\n".join(members_without_admin)

def get_joining_message(lobby_members, admin):
    str_of_members = get_str_of_members(lobby_members.copy(), admin)
    return f"Приветствую тебя в Бункере!!!!\n" \
           f"Лобби:" \
           f"\n{str_of_members}"


import random
import chatlib_skeleton
import select
import socket

# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later
messages_to_send = []
client_sockets = []
data_queue = {}
ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS
def build_and_send_message(conn, code, msg):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), msg (str)
    Returns: Nothing
    """
    msg = chatlib_skeleton.build_message(code, msg)
    add_message_to_queue(conn, msg)

    print("[SERVER] ", msg)  # Debug print
    print("Message sent to: ", conn.getpeername())


def recv_message_and_parse(conn):
    """
    Receives a new message from given socket.
    Prints debug info, then parses the message using chatlib.
    Parameters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    """
    try:
        received_msg = conn.recv(1024).decode()
    except socket.error:
        return "", ""
    if received_msg == "":
        return "", ""
    else:
        cmd, msg = chatlib_skeleton.parse_message(received_msg)
        return cmd, msg


def print_client_sockets(client_socket):
    """
    This function prints the client sockets.
    """
    print("List of clients: ")
    for c in client_socket:
        print("\t", c.getpeername())
    if len(client_socket) == 0:
        print("\t", "No clients connected currently")
    print("------------")


# Data Loaders #


def add_message_to_queue(conn, data):
    """
    The function recieves a socket and data, and it adds messages into messages_to_send, in order to create a queue.
    """
    global messages_to_send
    global data_queue
    data_queue[conn.getpeername()] = data
    x = (conn, data)
    messages_to_send.append(x)


def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    quests = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpelier"],
               "correct": 3},
        1234: {"question": "What is the capital city of USA?",
               "answers": ["Washington DC", "New York", "Los Angeles", "Detroit"], "correct": 1},
        4364: {"question": "Who wrote the song Yellow submarine?",
               "answers": ["Elvis Presley", "The Beatles", "Led Zeppelin", "Britney Spears"], "correct": 2},
        1: {"question": "How much is 1+1?", "answers": ["5", "6", "7", "2"], "correct": 4},
        2: {"question": "Which horoscope sign is a fish?", "answers":
            ["Pisces", "Virgin", "Scorpion", "Cancer"], "correct": 1},
        3: {"question": "The fear of insects is known as what?", "answers": ["MotoPhobia", "Ailurophobia",
                                                                             "Arachnophobia", "Entomophobia"],
            "correct": 4},
        4: {"question": "Which of the following languages has the longest alphabet?", "answers":
            ["Hebrew", "Russian", "Arabic", "Greek"], "correct": 2},
        5: {"question": "What number was the Apollo mission that successfully put a man on the moon for the first "
                        "time in human history?", "answers": ["9", "12", "11", "13"], "correct": 3},
        6: {"question": "Who is generally considered the inventor of the motor car?", "answers": ["Henry Ford",
                                                                                                  "Karl Benz",
                                                                                                  "Henry M. Leland",
                                                                                                  "John F. Kennedy"],
            "correct": 2},
        7: {"question": "Where was the first example of paper money used?", "answers": ["Turkey", "Greece", "China",
                                                                                        "Macedonia"], "correct": 3},
        8: {"question": "Which city is home to the Brandenburg Gate?", "answers": ["Las Vegas", "Berlin", "Rome",
                                                                                   "Tokyo"], "correct": 2},
        9: {"question": "The human body is made up of approximately how much water?", "answers": ["50%", "35%", "60%",
                                                                                                  "70%"], "correct": 4},
        10: {"question": "How many sides does a Dodecahedron have?", "answers": ["5", "8", "12", "20"], "correct": 3},
        11: {"question": "In which continent are Chile, Argentina and Brazil?", "answers": ["South America",
                                                                                            "North America", "Europe",
                                                                                            "Asia"], "correct": 1},
        12: {"question": "What is the currency of Qatar?", "answers": ["Pound", "Euro", "Riyal", "Dollar"],
             "correct": 3},
        13: {"question": " In which city were the 1992 Summer Olympics held?", "answers": ["Jerusalem", "Barcelona",
                                                                                           "London", "Berlin"],
             "correct": 2},
        14: {"question": "What is the national language of Canada?",
             "answers": ["French", "English", "Dutch", "Spanish"], "correct": 2},
        15: {"question": "Who was elected President of the United States in 2017?",
             "answers": ["Donald Trump", "Barack Obama", "George Bush", "Hilary Clinton"], "correct": 1},
        16: {"question": "In the Board Game, Settlers of Catan, a die roll of what number causes the Robber to attack?",
             "answers": ["10", "9", "7", "6"], "correct": 3},
        17: {"question": "Which Game of Thrones character is known as the Young Wolf?",
             "answers": ["Robb Stark", "Arya Stark", "Sansa Stark", "Rocket Stark"], "correct": 1},
        18: {"question": "How many plays do people (generally) believe that Shakespeare wrote?",
             "answers": ["54", "20", "254", "37"], "correct": 4},
        19: {"question": "How long did dinosaurs live on the earth?",
             "answers": ["200+ million years", "150-200 million years", "100-150 million years",
                         "50-100 million years"], "correct": 2},
        20: {"question": "What Italian city is famous for its system of canals?",
             "answers": ["Rome", "Milano", "Venice", "Naples"], "correct": 3},
        21: {"question": "What is the strongest muscle in the human body?",
             "answers": ["Jaw", "Muscle", "Heart", "Glutes"], "correct": 1},
        69: {"question": "What is the longest running Broadway show ever?",
             "answers": ["The Lion King", "Les Miserable", "The Phantom of the Opera", "Wicked"], "correct": 3},
        22: {"question": "Where was tea invented?",
             "answers": ["Israel", "USA", "UK", "China"], "correct": 4},
        23: {"question": "Where was the earliest documented case of the Spanish flu?",
             "answers": ["Spain", "USA", "Mexico", "Norway"], "correct": 2},
        24: {"question": "Which of the following languages is NOT driven from Latin?",
             "answers": ["English", "French", "German", "Portuguese"], "correct": 1},
        25: {"question": "Which of the following was considered one of the Seven Ancient Wonders?",
             "answers": ["Colosseum", "Great Wall of China", "Colossus of Rhodes", "The Western Wall"], "correct": 3},
        26: {"question": "Which app has the most total users?",
             "answers": ["Instagram", "TikTok", "Snapchat", "Pokemon Go"], "correct": 1},
        27: {"question": "What is the largest US state (by landmass)?",
             "answers": ["Texas", "New York", "California", "Alaska"], "correct": 4},
        28: {"question": "Who was the lead singer of the band The Who?",
             "answers": ["Roger Daltrey", "Don Henley", "Robert Plant", "Marshall Mathers"], "correct": 1}

    }
    return quests


def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Receives: nothing
    Returns: user dictionary
    """
    file = open(r"D:\Trivia\usersdata.txt", 'r')
    dict_users = file.read()
    users = eval(dict_users)
    return users


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Receives: nothing
    Returns: the socket object
    """
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print(f'server is up at port {SERVER_PORT}')
    return server_socket


def split_msg(conn, msg, expect_fields):
    """
        Helper method. gets a string and number of expected fields in it. Splits the string
        using protocol's delimiter (|) and validates that there are correct number of fields.
        Returns: list of fields if all ok. If some error occurred, returns None
    """
    return chatlib_skeleton.split_msg(msg, expect_fields)


def send_error(conn, error_msg):
    """
    Send error message with given message
    Receives: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(conn, "ERROR", error_msg)


# MESSAGE HANDLING


def handle_getscore_message(conn, username):
    """
    This function receives a socket and a username, and if the user exists, it sends the users' score back to him.
    Else, it sends back a error message saying the username was not found.
    """
    global users
    if username in users:
        current_user = users.get(username)
        score = current_user["score"]
        print("Current score:", score)
        build_and_send_message(conn, "YOUR_SCORE", score)
    else:
        send_error(conn, "Username not found")


def handle_logout_message(conn):
    """
    Closes the given socket (in later chapters, also remove user from logged_users dictionary)
    Recieves: socket
    Returns: None
    """
    global logged_users
    if conn.getpeername() in logged_users.keys():
        logged_users.pop(conn.getpeername())
    else:
        send_error(conn, "Socket not in dictionary")


# Implement code ...
def checkint(str1):
    """
    this function checks if the string it receives is an integer, returns true if it is and false otherwise.
    """
    try:
        int(str1)
        return True
    except ValueError:
        return False


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Receives: socket, message code and data
    Returns: None (sends answer to client)
    """

    global users  # This is needed to access the same users dictionary from all functions
    global logged_users  # To be used later
    split_data = data.split("#")
    x = chatlib_skeleton.build_message("LOGIN", data)
    count = x.count('|')
    expected_fields = count + 1
    field_list = split_msg(conn, x, expected_fields)
    user = split_data[0]
    if user in users.keys() and user not in logged_users.values():
        if None not in field_list:
            password = split_data[1]
            current_user = users.get(user)
            if password == current_user['password']:
                build_and_send_message(conn, chatlib_skeleton.PROTOCOL_SERVER["login_ok_msg"], "")
                addr = conn.getpeername()
                logged_users[addr] = user
            else:
                send_error(conn, "Login failed")
        else:
            send_error(conn, "Fields error")
    else:
        send_error(conn, "User not in database or already logged")


# Implement code ...
def create_random_question(username):
    """
    this function receives a username, and creates a question message to send to the user.
    The question that is sent is a question he has not been asked before.
    If the user has answered all the questions already, None is sent instead.
    """
    asked = users[username]["questions_asked"]
    all_questions = load_questions()
    not_asked = []
    key_list = list(all_questions.keys())
    for i in key_list:
        if i not in asked:
            question = {i: {"question": all_questions[i]["question"], "answers": all_questions[i]["answers"],
                            "correct": all_questions[i]["correct"]}}
            not_asked.append(question)
    if len(not_asked) == 0:
        return None
    else:
        x = random.randint(0, len(not_asked) - 1)
        question1 = not_asked[x]
        quest_id = str(list(question1.keys())[0])
        values = list(question1.values())[0]
        question = values["question"]
        answer1 = str(values["answers"][0])
        answer2 = str(values["answers"][1])
        answer3 = str(values["answers"][2])
        answer4 = str(values["answers"][3])
        msg1 = quest_id + "#" + question + "#" + answer1 + "#" + answer2 + "#" + answer3 + "#" + answer4
        msg = chatlib_skeleton.build_message("YOUR_QUESTION", msg1)
        return msg


# take second element for sort
def takesecond(elem):
    return elem[1]


def get_high_scores(conn):
    """
    The function receives a socket, and sends a message that contains a list of the
    top five leading users in terms of score.
    """
    global users
    keys = list(users.keys())
    scores = []
    string_to_send = ""
    for i in range(len(keys)):
        info = [keys[i], (users[keys[i]]["score"])]
        scores.append(info)
    scores = sorted(scores, key=takesecond, reverse=True)
    for i in range(5):
        string_to_send += scores[i][0] + ": " + str(scores[i][1]) + "\n"
    build_and_send_message(conn, "ALL_SCORE", string_to_send)


def handle_logged_message(conn):
    """
    This function receives a socket, and builds a message to send back to the clients, which contains a list of
    the logged users currently.
    """
    user_list = list(logged_users.values())
    user_string = ""
    for i in range(len(user_list) - 1):
        user_string += str(user_list[i]) + ","
    user_string += str(user_list[-1])
    build_and_send_message(conn, "LOGGED_ANSWER", user_string)


def handle_question_message(conn, username):
    """
    This function receives a socket and a username and creates a new question using the create_random_question function.
    If the user exists, it sends him the question, if there are any left. If not, it sends an error
    saying the user was not found.
    """
    global users
    if username in users:
        question = create_random_question(username)
        if question is None:
            build_and_send_message(conn, "NO_QUESTIONS", "")
        else:
            print("Current score:", question)
            conn.send(question.encode())
    else:
        send_error(conn, "Username not found")


def handle_answer_message(conn, username, answer):
    """
    The function receives a socket, a username, and an answer (consisting of the question id and answer chosen),
    and if the answer is correct, the score is updated, and a message telling the user that
    he was correct is sent to him. If the user was wrong, a message telling the user that he was wrong is sent to him.
    If the user inputted an invalid answer an error is sent back to him.
    """
    ans = answer.split("#")
    question_id = ans[0]
    question_choice = ans[1]
    questions_x = load_questions()
    if checkint(question_choice):
        if int(question_choice) == 1 or int(question_choice) == 2 or int(question_choice) == 3 or int(
                question_choice) == 4:
            if questions_x.get(int(question_id))["correct"] == int(question_choice):
                users[username]["score"] += 5
                print("Current score: ", users[username]["score"])
                build_and_send_message(conn, "CORRECT_ANSWER", "")
            else:
                build_and_send_message(conn, "WRONG_ANSWER", questions[int(question_id)]["correct"])
            users[username]["questions_asked"].append(int(question_id))
        else:
            send_error(conn, "Wrong input")
    else:
        send_error(conn, "Wrong input")


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Receives: socket, message code and data
    Returns: None
    """
    global messages_to_send
    global data_queue
    global users
    if conn.getpeername() not in logged_users.keys():
        print("----------")
        if cmd == "LOGIN":
            handle_login_message(conn, data)
        else:
            send_error(conn, "Unknown/Unauthorized command")
        print("----------")
    else:
        print("----------")
        if cmd == "LOGOUT" or cmd == "MY_SCORE" or cmd == "GET_QUESTION" or cmd == "SEND_ANSWER" or cmd == "LOGGED" or \
                cmd == "HIGHSCORE":
            if cmd == "LOGOUT":
                handle_logout_message(conn)
            if cmd == "MY_SCORE":
                handle_getscore_message(conn, logged_users[conn.getpeername()])
            if cmd == "GET_QUESTION":
                handle_question_message(conn, logged_users[conn.getpeername()])
            if cmd == "SEND_ANSWER":
                handle_answer_message(conn, logged_users[conn.getpeername()], data)
                f = open(r"D:\Trivia\usersdata.txt", "r+")
                # r+ mode opens the file in read and write mode
                f.truncate(0)
                f.write(str(users))
                f.close()
            if cmd == "LOGGED":
                handle_logged_message(conn)
            if cmd == "HIGHSCORE":
                get_high_scores(conn)
            print("----------")
        else:
            send_error(conn, "Unknown/Unauthorized command")


# Implement code ...


def main():
    # Initializes global users and questions dictionaries using load functions, will be used later
    global users, current_socket
    global questions
    global messages_to_send
    users = load_user_database()
    server_socket = setup_socket()
    questions = load_questions()
    print("Listening for clients...")
    client_sockets = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets,
                                                                client_sockets)
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:
                print("New data from client: ", current_socket.getpeername())
                cmd, msg = recv_message_and_parse(current_socket)
                print("Command: ", cmd)
                print("Message:", msg)
                if (cmd == "" and msg == "") or cmd == "LOGOUT":
                    print("Connection closed", )
                    client_sockets.remove(current_socket)
                    handle_logout_message(current_socket)
                    current_socket.close()
                    print_client_sockets(client_sockets)
                else:
                    handle_client_message(current_socket, cmd, msg)
        for socks in ready_to_write:
            for i in range(len(messages_to_send)):
                if messages_to_send[i][0] == socks:
                    if socks in client_sockets:
                        socks.send(messages_to_send[i][1].encode())
                        data_queue.pop(messages_to_send[i][0].getpeername())
                        messages_to_send.remove(messages_to_send[i])

        for socks in in_error:
            client_sockets.remove(current_socket)
            handle_logout_message(current_socket)
            current_socket.close()


if __name__ == '__main__':
    main()

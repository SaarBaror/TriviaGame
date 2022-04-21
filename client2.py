import socket
import chatlib_skeleton  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), msg (str)
    Returns: Nothing
    """
    message = chatlib_skeleton.build_message(code, msg)
    # print("[Client] Message to send: ", message)
    conn.send(message.encode())


def get_score(conn):
    """
    The function receives a socket, and uses build_send_recv_parse to send MY_SCORE message to the server,
    receives a YOUR_SCORE message back, and prints the score.
    """
    msg, cmd = build_send_recv_parse(conn, "MY_SCORE", "")
    if cmd == "YOUR_SCORE":
        print("Score: ", msg)
    else:
        error_and_exit(msg)


def build_send_recv_parse(conn, command, message):
    """
    The function receives a socket, message and command and it builds a message to send to the server.
    Then, it receives back a message from the server and returns the data and command.
    """
    build_and_send_message(conn, command, message)
    cmd, msg = recv_message_and_parse(conn)
    return msg, cmd


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket.
    Prints debug info, then parses the message using chatlib.
    Parameters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    """
    # Implement Code
    # ..
    data = conn.recv(1024)
    if type(data) == bytes:
        cmd, msg = chatlib_skeleton.parse_message(data.decode())
    else:
        cmd, msg = chatlib_skeleton.parse_message(data)
    return cmd, msg


def connect():
    """
    connects the client with the server and returns the socket.
    """
    # Implement Code
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def get_logged_users(conn):
    """
    This func receives a socket, and uses build_send_recv_parse in order to get a list
    of all the logged users, and then prints it.
    """
    msg, cmd = build_send_recv_parse(conn, "LOGGED", "")
    print("The logged users are: ", msg)


def get_highscore(conn):
    """
    This function receives a socket and uses  build_send_recv_parse to get a list of the 5 users with best score,
    and then it prints it.
    """
    msg, cmd = build_send_recv_parse(conn, "HIGHSCORE", "")
    print(msg)


def play_question(conn):
    """
    This function receives a socket, and gets a random question from the server using  build_send_recv_parse.
    If no questions are left, the function stops.
    Else, the function builds a trivia question using the data it got from the server, and it prints a message
    that says if you were correct or not, depending on your answer.
    """
    msg, cmd = build_send_recv_parse(conn, "GET_QUESTION", "")
    if cmd != "ERROR":
        if cmd == "NO_QUESTIONS":
            print("No questions left")
        else:
            msg_split = msg.split("#")
            id1 = msg_split[0]
            question = msg_split[1]
            answer1 = msg_split[2]
            answer2 = msg_split[3]
            answer3 = msg_split[4]
            answer4 = msg_split[5]
            space1 = ""
            space2 = ""
            for i in range(len(answer1)):
                space1 += " "
            for i in range(len(answer3)):
                space2 += " "
            print("---------")
            print(question + "\n")
            print("Answer 1: ", answer1 + space2 + "Answer 2: ", answer2 + "\n")
            print("Answer 3: ", answer3 + space1 + "Answer 4: ", answer4 + "\n")
            print("---------")
            choice = input("Which answer do you think is correct? answer 1,2,3 or 4 ")
            x = id1 + "#" + choice
            msg, cmd = build_send_recv_parse(conn, "SEND_ANSWER", x)
            if cmd == "CORRECT_ANSWER":
                print("The answer was correct! Well done")
            if cmd == "WRONG_ANSWER":
                if int(msg) == 1:
                    print("Wrong answer. The correct answer was answer number 1 : ", answer1)
                if int(msg) == 2:
                    print("Wrong answer. The correct answer was answer number 2 : ", answer2)
                if int(msg) == 3:
                    print("Wrong answer. The correct answer was answer number 3: ", answer3)
                if int(msg) == 4:
                    print("Wrong answer. The correct answer was  answer number 4 : ", answer4)
            if cmd == "ERROR":
                print(msg)
    else:
        return error_and_exit(msg)


def error_and_exit(msg):
    """
    The function receives a message, prints it and returns exit.
    """
    print(msg)
    return exit()


def login(conn):
    """
    The function receives a socket, and loops until a user and password 
    that are in the database (and not logged to the server already),
    then it prints a message telling the client the login was succesfull.
    """
    username = input("Please enter username: \n")
    password = input("Please enter password: \n")
    data = username + "#" + password
    build_and_send_message(conn, "LOGIN", data)
    cmd, msg = recv_message_and_parse(conn)
    while cmd != chatlib_skeleton.PROTOCOL_SERVER["login_ok_msg"]:
        print("Login failed:", msg)
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        data = username + "#" + password
        build_and_send_message(conn, "LOGIN", data)
        cmd, msg = recv_message_and_parse(conn)
        print("------------")
    print("Login was successful")
    # Implement code


# Implement code
def logout(conn):
    """
    The function receives a socket, and sends a log out message to the server.
    """
    build_and_send_message(conn, "LOGOUT", "")


def main():
    sock = connect()
    login(sock)
    x_msg = "dsgsdg"
    while x_msg != "Log out":
        x = input("Please choose an option: [h,l,m,t,q] : " + "\n" + "\t" + "h: Get High Score" + "\n" + "\t" +
                  "l: Get Logged users" + "\n" + "\t" + "m: Get My Score" + "\n" + "\t" + "t: Play a trivia question"
                  + "\n" + "\t" + "q: Quit" + "\n")
        if x == "q" or x == "l" or x == "m" or x == "t" or x == "h":
            if x == "t":
                play_question(sock)
                print("---------")
            if x == "h":
                print("---------")
                get_highscore(sock)
                print("---------")
            if x == "l":
                print("---------")
                get_logged_users(sock)
                print("---------")
            if x == "m":
                print("---------")
                get_score(sock)
                print("---------")
            if x == "q":
                print("---------")
                x_msg = "Log out"
                print("Logging out.....")
                print("---------")
        else:
            error_and_exit("Unknown input")
    logout(sock)
    error_and_exit("")


if __name__ == '__main__':
    main()

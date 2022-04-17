# Protocol Constants


CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
BASIC_DELIMITERS = 2

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT"
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR"
}  # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def checkint(str1):
    try:
        int(str1)
        return True
    except ValueError:
        return False


def build_message(cmd, data):
    """
    Gets command name and data field and creates a valid protocol message
    Returns: str, or None if error occurred
    """
    full_msg = ""
    length_msg = ""
    len_cmd = len(cmd)
    if len_cmd <= CMD_FIELD_LENGTH:
        for i in range(CMD_FIELD_LENGTH - len_cmd):
            cmd += " "
    else:
        return None
    full_msg += cmd + DELIMITER
    if type(data) == str:
        len_data = len(data)
    else:
        len_data = len(str(data))
    if MAX_DATA_LENGTH >= len_data >= 0:
        str_data = len(str(len_data))
        for i in range(LENGTH_FIELD_LENGTH - str_data):
            length_msg += "0"
        length_msg += str(len_data)
    else:
        return None
    if type(data) == str:
        full_msg += length_msg + DELIMITER + data
    else:
        full_msg += length_msg + DELIMITER + str(data)
    return full_msg


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occurred, returns None, None
    """
    if data is None or data == "":
        return None, None

    if len(data) < MSG_HEADER_LENGTH:
        return None, None

    else:
        if data[16] != DELIMITER:
            return None, None
        cmd = ""
        msg = ""
        msg1 = ""
        splatted_msg = data.split(DELIMITER)
        if checkint((splatted_msg[1])):
            if len(splatted_msg) >= 3 and 0 <= int(splatted_msg[1]) <= 9999:
                for i in range(2, len(splatted_msg)):
                    msg += splatted_msg[i].replace(" ", "")
                    msg1 += splatted_msg[i]
                    if i < len(splatted_msg)-1:
                        msg += DELIMITER
                        msg1 += DELIMITER
                if int(splatted_msg[1]) == len(msg1):
                    cmd += splatted_msg[0].replace(" ", "")
                    # The function should return 2 values
                    if cmd != "ERROR" and cmd != "YOUR_QUESTION":
                        return cmd, msg
                    else:
                        return cmd, msg1
                else:
                    return None, None
            else:
                return None, None
        else:
            return None, None


def split_msg(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's delimiter (|) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occurred, returns None
    """
    splitted_msg = msg.split(DELIMITER)
    if len(splitted_msg) == expected_fields:
        return splitted_msg
    else:
        none_list = []
        for i in range(expected_fields):
            none_list.append(None)
        return none_list


# Implement code ...


def join_msg(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the delimiter.
    Returns: string that looks like cell1|cell2|cell3
    """
    msg_str = ""
    for i in range(len(msg_fields)):
        if type(msg_fields[i]) != str:
            msg_str += str(msg_fields[i])
        else:
            msg_str += msg_fields[i]
        if i < len(msg_fields) - 1:
            msg_str += DELIMITER
    return msg_str



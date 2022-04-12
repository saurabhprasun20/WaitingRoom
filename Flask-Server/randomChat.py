from random import randrange
import os, json

data = {}
current_dir = os.path.join(os.path.dirname(__file__))
with open(os.path.join(current_dir, "chat_choice.json"), 'r+') as jsonFile:
    data = json.load(jsonFile)


chat_choice = data['chat_choice']
init_max = data['init_max']
print(data)
print(init_max)
flag = 0
last_choice = -1


# def check_last_choice_exception():
#     last_choice_available_flag = 0
#     all_other_exhausted_flag = 0
#     if chat_choice[last_choice] < init_max:
#         last_choice_available_flag = 1
#         for i in range(0,4):
#             if i != last_choice:
#                 if chat_choice[i] == init_max:
#                     all_other_exhausted_flag += 1
#
#     if last_choice_available_flag == 1 and all_other_exhausted_flag == 3:
#         return True
#     else:
#         return False

def check_max():
    chat_set = set(chat_choice)
    if len(chat_set) == 1:
        if init_max in chat_set:
            return True


def select_chat_room():
    global flag, last_choice, init_max
    final_choice = -1
    while True:
        choice = randrange(4)
        if chat_choice[choice] < init_max:
            chat_choice[choice] += 1
            flag = 1
            last_choice = choice
            final_choice = choice
            break
        else:
            if check_max():
                init_max = init_max + 1
            else:
                continue

    with open(os.path.join(current_dir, "chat_choice.json"), 'w+') as jsonFile:
        data['chat_choice'] = chat_choice
        data['init_max'] = init_max
        json.dump(data, jsonFile)

    return final_choice




print(select_chat_room())
# print(chat_choice)

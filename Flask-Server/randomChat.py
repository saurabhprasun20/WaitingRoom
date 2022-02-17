from random import randrange

init_max = 3
chat_choice = [0,0,0,0]
flag = 0
last_choice = -1

def check_last_choice_exception():
    last_choice_available_flag = 0
    all_other_exhausted_flag = 0
    if chat_choice[last_choice] < init_max:
        last_choice_available_flag = 1
        for i in range(0,4):
            if i != last_choice:
                if chat_choice[i] == init_max:
                    all_other_exhausted_flag += 1

    if last_choice_available_flag == 1 and all_other_exhausted_flag == 3:
        return True
    else:
        return False

def check_max():
    chat_set = set(chat_choice)
    if len(chat_set) == 1:
        if init_max in chat_set:
            # print("Chat choice is max")
            # print(chat_choice)
            return True


def select_chat_room():
    global flag,last_choice, init_max
    final_choice = -1
    while True:
        choice = randrange(4)
        if chat_choice[choice] < init_max:
            if check_last_choice_exception():
                # print("Valid choice from last exception - " + str(choice))
                chat_choice[choice] += 1
                flag = 1
                last_choice = choice
                final_choice = choice
                break
            else:
                if choice != last_choice:
                    # print("Valid choice is - "+ str(choice))
                    chat_choice[choice] += 1
                    flag = 1
                    last_choice = choice
                    final_choice = choice
                    break
                else:
                    continue
        else:
            if check_max():
                init_max = init_max+3
            else:
                continue

    return final_choice

# for i in range(0,20):
#     print(select_chat_room())
#
# print(chat_choice)

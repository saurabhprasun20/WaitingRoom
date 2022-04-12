from random import randrange
import os, csv

init_max = 3
chat_choice = [0, 0, 0, 0]
current_dir = os.path.join(os.path.dirname(__file__))
with open(os.path.join(current_dir, "chat_choice.csv"), 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        print("row is")
        print(row)
        # if count == 1:
        chat_choice = list(map(int, row))
        # print(list(map(int, row)))
        # chat_choice[0] = int(row['0'])

print(chat_choice)
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
            # print("Chat choice is max")
            # print(chat_choice)
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

    with open(os.path.join(current_dir, "chat_choice.csv"), 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(chat_choice)
    return final_choice


for i in range(0,20):
    print(select_chat_room())

# print(select_chat_room())
print(chat_choice)

import random


original_list = ["look Left", "Look Right", "Look Down", "Look Up"]

def output_list():
    random.shuffle(original_list)
    new_list = []
    while len(new_list) < 5:
        string = random.choice(original_list)
        if string not in new_list or new_list[-1] != string:
            new_list.append(string)
    missing_strings = set(original_list) - set(new_list)
    new_list.extend(random.sample(list(missing_strings), len(missing_strings)))
    return new_list

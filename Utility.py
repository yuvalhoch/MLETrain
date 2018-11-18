def generate_q_dic_from_file(q_file_path):
    q_dic = {}
    q_file = open(q_file_path, "r")
    # Each line in e_file in the format:
    # tag1 tag2 tag3   appearancesCount, (separated by a tab. second and third tag are optional)

    lines = q_file.readlines()  # In order to go over the lines in q_file.
    for line in lines:
        line = line.replace("\n", "")
        by_tab = line.split("\t")
        tags = by_tab[0]
        event_count = by_tab[1]
        q_dic[tags] = event_count
    return q_dic


def generate_e_dic_from_file(e_file_path):
    e_dic = {}
    e_file = open(e_file_path, "r")
    # Each line in e_file in the format:
    # word pos   appearancesCount, (separated by a tab.)

    lines = e_file.readlines()  # In order to go over the lines in e_file.
    # For every line in e_file, split the line word pos\t count_of_event by split('\t').
    for line in lines:
        line = line.replace("\n", "")
        by_tab = line.split("\t")
        word_and_pos = by_tab[0]
        event_count = by_tab[1]
        by_spaces = word_and_pos.split(" ")
        word = by_spaces[0]
        pos = by_spaces[1]

        # If the word not in e_dic, create a new entry {word: {pos: event_count}},
        # where event_count represent the num of appearances of word/POS in the corpus.
        if word not in e_dic.keys():
            e_dic[word] = {}
            e_dic[word][pos] = event_count
        else:
            # If word exist [and there is already {pos: num} entry for word] then its a new pos add new entry
            e_dic[word][pos] = event_count
    return e_dic


def read_possible_poses_from_file(pos_file_path):
    pos_list = []
    pos_file = open(pos_file_path, "r")
    lines = pos_file.readlines()  # In order to go over the lines in pos_file.
    for line in lines:
        line = line.replace("\n", "")
        pos_list.append(line)
    return pos_list

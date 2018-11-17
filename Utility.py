def generate_q_dic_from_file(q_file_path):
    q_dic = {}
    q_file = open(q_file_path, "r")
    # Each line in e_file in the format:
    # tag1 tag2 tag3   appearancesCount, (separated by a tab. second and third tag are optional)

    lines = q_file.readlines()  # In order to go over the lines in q_file.
    for line in lines:
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


def read_possible_poses_from_file(pos_file):
    pos_list = []
    lines = pos_file.readlines()  # In order to go over the lines in pos_file.
    for line in lines:
        pos_list.append(line)
    return pos_list




    # # Calculate the e equation = e(count(word, POS)/count(POS)) using given e_dic, q_dic
    # def get_e_using_dic(word, tag, e_dic, q_dic):
    #     count_word_pos = float(e_dic[word + " " + tag])
    #     count_pos = float(q_dic[tag])
    #     prob = count_word_pos / count_pos
    #     return prob
    #
    # def get_q(pprev, prev, cur):
    #     global q_dic
    #     prob_2_pos = count_c = prob_1_pos = 0.0
    #     count_abc = abc_seq_count(cur, pprev, prev)
    #     # Calculate the probability of the [pprev prev cur] occurrence,
    #     # by using the count(pprev, prev, cur).
    #     prob_3_pos = prob_of_3_pos(count_abc, pprev, prev)
    #     count_bc = bc_seq_count(cur, prev)
    #     # If prev have seen in the corpus before.
    #     if prev in q_dic.keys():
    #         count_b = float(q_dic[prev])
    #         # Calculate the probability of the [pprev prev] occurrence,
    #         # by using the count(prev).
    #         prob_2_pos = count_bc / count_b
    #     # If cur have seen in the corpus before.
    #     if cur in q_dic.keys():
    #         count_c = float(q_dic[cur])
    #     count_all_words = float(q_dic["NUM_WORDS"])     # Is the number of words in the corpus
    #     # Calculate the probability of the [cur] occurrence,
    #     # by using the count(cur)/count_all_words.
    #     prob_1_pos = count_c / count_all_words
    #     wight = [0.85, 0.1, 0.05]       # The lambda vector of wights.
    #     q_values = [prob_3_pos, prob_2_pos, prob_1_pos]      # The three values of q equation.
    #     # Return the interpolation of <wight, q_values>.
    #     return np.sum(np.multiply(wight,q_values))

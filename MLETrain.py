import numpy as np
import sys

e_dic = {}
q_dic = {}
# Dictionary to count appearances of each part of speech (pos -> appearances)
pos_count_dic = {}
suffix_dic = {}
word_signature = ['ing', 'ed', '\'s', 'n\'t', 'hood', 'ist', 'ness', 'able', 'ible',
                  'en', 'ic', 'ish', 'less', 'ly', 'tial', 'er', 's']
punctuation_marks = ['.', ',', '"', '``', '(', ')', '=', '-', '!', '@', '#', '?',
                     '$', '%', '&', '*', '+', '{', '}', '\'\'', ':', '...', ';', '--']


def start():
    train_file = open("ass1-tagger-train")
    e_file = open("e_file.txt", "a")
    q_file = open("q_file.txt", "a")
    pos_file = open("extra_file_name.txt", "a")  # file which contain all the possible POSes. each line contains a pos.
    ################################
    #train_file = open(sys.argv[1])
    #e_file = open(sys.argv[2], "a")
    #q_file = open(sys.argv[3], "a")
    ################################
    create_e(train_file)
    write_to_e_file(e_file)
    train_file.close()
    train_file = open("ass1-tagger-train")
    create_q(train_file)
    write_to_q_file(q_file)

    # write pos file...
    write_pos_file(pos_file)

    train_file.close()


# pos file is file which contain all the possible POSes. each line contains a pos.
def write_pos_file(pos_file):
    for pos in pos_count_dic.keys():
        pos_file.write(pos + "\n")
    pos_file.close()


def write_to_e_file(e_file):
    global e_dic
    # Each line in e_file represents an event and a count, separated by a tab.
    for word in e_dic:
        for en in e_dic[word].keys():
            e_file.write(word + " " + en + "\t" + str(e_dic[word][en]) + "\n")
    e_file.close()


def write_to_q_file(q_file):
    global q_dic
    # Each line in e_file represents an event and a count, separated by a tab.
    for en in q_dic:
        q_file.write(en + "\t" + str(q_dic[en]) + "\n")
    q_file.close()


def create_q(train_file):
    global q_dic
    # q_dic['NUM_WORDS'] is the number of the words in the corpus.
    q_dic['NUM_WORDS'] = 0
    lines = train_file.readlines()    # In order to go over the lines in train_file.
    # Represents the prev and prev-prev POS of the current POS.
    prev = None
    pprev = None
    # For every line in train_file, split the line to words by split(' ').
    for line in lines:
        by_spaces = line.split(" ")
        # For every pair - word/POS in the corpus.
        for pair in by_spaces:
            # Increase the q_dic['NUM_WORDS'] by 1.
            q_dic['NUM_WORDS'] += 1
            # Extract the POS from the pair
            pos = pair.split("/")[1].split("\n")[0]
            # Avoid word\word case in the corpus.
            if (not pos.isupper()) and pos not in punctuation_marks:
                break
            # Create 3 sequences for a, a-b, a-b-c.
            pos_cur = pos
            add_entry_to_q_dict(q_dic, pos_cur)
            # If there is no prev-prev POS, case of the second word in the sentence.
            if prev != None and pprev == None:
                pos_inc_prev = prev + " " + pos_cur
                add_entry_to_q_dict(q_dic, pos_inc_prev)
            # If the is prev-prev POS.
            elif prev != None and pprev != None:
                pos_inc_prev = prev + " " + pos_cur
                pos_inc_pprev = pprev + " " + prev + " " + pos_cur
                add_entry_to_q_dict(q_dic, pos_inc_prev)
                add_entry_to_q_dict(q_dic, pos_inc_pprev)
            # Move on to the next pair of word/POS.
            pprev = prev
            prev = pos


def add_entry_to_q_dict(dic, pos):
    add_entry_to_counter_dict(dic, pos)


# Counter dictionary is dict that the values are the sum of the appearances of the keys
# for example dic[a] = 2 means that a inserted 2 times to dictionary
# the method receives dic & entry then updates the dictionary accordingly
def add_entry_to_counter_dict(dic, entry):
    if entry in dic.keys():
        dic[entry] += 1
        return
    dic[entry] = 1


def create_e(train_file):
    global e_dic, word_signature, pos_count_dic

    # A word-signature that mentions whether the first letter or the
    # whole word is in upper case.
    starts_with_capital_letter = '^Aa'
    all_capital_letters = '^AAA'
    e_dic[all_capital_letters] = {}
    e_dic[starts_with_capital_letter] = {}

    lines = train_file.readlines()      # In order to go over the lines in train_file.
    # For every line in train_file, split the line to words by split(' ').
    for line in lines:
        by_spaces = line.split(" ")

        # For every pair - word/POS in the corpus.
        for pair in by_spaces:
            by_slash = pair.split("/")
            # Extract the word from the pair.
            word = by_slash[0]
            # Extract the POS from the pair.
            pos = by_slash[1].split("\n")[0]
            # In case of the word CD, change it to lower case because of the tag CD.
            if word == 'CD':
                word = 'cd'
            # Avoid word\word case in the corpus.
            if (not pos.isupper()) and pos not in punctuation_marks:
                break

            # Add pos to pos_count_dic.
            add_entry_to_counter_dict(pos_count_dic, pos)
            # If the word not in e_dic, create a new entry {word: {pos: 1}},
            # where 1 represent the first appearance of word/POS in the corpus.
            if word not in e_dic.keys():
                e_dic[word] = {}
                e_dic[word][pos] = 1
            else:
                # If there is already {pos: num} entry in e_dic[word] entry, just add 1
                # to the number of appearances.
                if pos in e_dic[word].keys():
                    e_dic[word][pos] += 1
                # Else, create a new {pos: 1} entry in e_dic[word].
                else:
                    e_dic[word][pos] = 1

            # Check if this word have a special suffix (from the word_signature list),
            # if it has, add one to the e_dic[^suffix].
            for suffix in word_signature:
                if word.endswith(suffix):
                    add_word_signature(e_dic, pos, '^' + suffix)
            # Checks whether the first letter or the whole word is in upper case.
            if word.isupper():
                if pos not in e_dic[all_capital_letters]:
                    e_dic[all_capital_letters][pos] = 1
                else:
                    e_dic[all_capital_letters][pos] += 1
            elif word[0].isupper():
                if pos not in e_dic[starts_with_capital_letter]:
                    e_dic[starts_with_capital_letter][pos] = 1
                else:
                    e_dic[starts_with_capital_letter][pos] += 1


def add_word_signature(dic, pos, suffix):
    if suffix in dic.keys():
        # If there is an {POS: num} entry in the suffix key,
        # add 1 to the number of occurrences.
        if pos in dic[suffix]:
            dic[suffix][pos] += 1
        else:
            dic[suffix][pos] = 1
    # If there is no suffix key in the dictionary - create one.
    else:
        dic[suffix] = {}
        dic[suffix][pos] = 1


def load_the_model(q_file_name, e_file_name):
    global q_dic, e_dic
    tag_set = set()
    words_dic = {}
    q_file = open(q_file_name)
    e_file = open(e_file_name)
    # Move on the q_file lines and save in q_dic the pairs {word: POS}.
    for line in q_file:
        word, pos = line.strip().split("\t", 1)
        q_dic[word] = pos
        # Add tag to the tag set.
        for tag in word.split(" "):
            tag_set.add(tag)
    # Move on the e_file lines and save in e_dic the pairs {(word, POS): count}.
    for line in e_file:
        word, count = line.strip().split("\t", 1)
        e_dic[word] = count
        # Split the pair (word, POS) and add {word: POS} as new entry in words_dic.
        word, pos = word.split(" ")
        if word in words_dic:
            words_dic[word].append(pos)
        else:
            words_dic[word] = [pos]
    # Close the open files.
    q_file.close()
    e_file.close()

    return tag_set, words_dic


def get_q(pprev, prev, cur):
    global q_dic
    prob_2_pos = count_c = prob_1_pos = 0.0
    count_abc = abc_seq_count(cur, pprev, prev)
    # Calculate the probability of the [pprev prev cur] occurrence,
    # by using the count(pprev, prev, cur).
    prob_3_pos = prob_of_3_pos(count_abc, pprev, prev)
    count_bc = bc_seq_count(cur, prev)
    # If prev have seen in the corpus before.
    if prev in q_dic.keys():
        count_b = float(q_dic[prev])
        # Calculate the probability of the [pprev prev] occurrence,
        # by using the count(prev).
        prob_2_pos = count_bc / count_b
    # If cur have seen in the corpus before.
    if cur in q_dic.keys():
        count_c = float(q_dic[cur])
    count_all_words = float(q_dic["NUM_WORDS"])     # Is the number of words in the corpus
    # Calculate the probability of the [cur] occurrence,
    # by using the count(cur)/count_all_words.
    prob_1_pos = count_c / count_all_words
    wight = [0.85, 0.1, 0.05]       # The lambda vector of wights.
    q_values = [prob_3_pos, prob_2_pos, prob_1_pos]      # The three values of q equation.
    # Return the interpolation of <wight, q_values>.
    return np.sum(np.multiply(wight,q_values))


# Calculate the number of appearances of the tow POS - prev cur.
def bc_seq_count(cur, prev):
    global q_dic
    count_bc = 0.0
    pos_seq = cur
    # If there is a prev POS.
    if prev != '':
        pos_seq = prev + " " + cur
    if pos_seq in q_dic.keys():
        count_bc = float(q_dic[pos_seq])
    return count_bc


def prob_of_3_pos(count_abc, pprev, prev):
    global q_dic
    prob_3_pos = 0.0
    pos_seq = prev
    # If there is a prev POS.
    if pprev != '':
        pos_seq = pprev + " " + prev
    if pos_seq in q_dic.keys():
        count_ab = float(q_dic[pos_seq])
        # Calculate the probability of the three POS (q equation first part) -
        # q(count(a, b, c)/count(a, b))
        prob_3_pos = count_abc / count_ab
    return prob_3_pos


# Calculate the number of appearances of the three POS - pprev prev cur.
def abc_seq_count(cur, pprev, prev):
    global q_dic
    pos_seq = cur
    count_abc = 0.0
    # If there is a prev-prev and prev POS.
    if pprev != '' and prev != '':
        pos_seq = pprev + " " + prev + " " + cur
    # Else, if there is only prev POS.
    elif prev != '':
        pos_seq = prev + " " + cur
    if pos_seq in q_dic.keys():
        count_abc = float(q_dic[pos_seq])  # Is the number of that sequence occurrence
    return count_abc


# Calculate the e equation = e(count(word, POS)/count(POS))
def get_e(word, tag):
    global e_dic, q_dic
    count_word_pos = float(e_dic[word + " " + tag])
    count_pos = float(q_dic[tag])
    prob = count_word_pos / count_pos
    return prob


def find_word_signature(word):
    global word_signature
    # Check if this word have a special suffix and return it.
    for suffix in word_signature:
        if word.endswith(suffix):
            return '^' + suffix
    # Check if the whole word is in upper case and return '^AAA'.
    if word.isupper():
        return '^AAA'
    # Else if, the word only starts with a upper letter, return '^Aa'.
    elif word[0].isupper():
        return '^Aa'
    # Check if the word is a number format.
    elif any(x.isdigit() for x in word):
        return 'CD'
    # Check if the word is a punctuation mark.
    elif word in punctuation_marks:
        return punctuation_mark_pos(word)
    return 'UNK'


# Return the punctuation mark that feets to the word, or the word itself.
def punctuation_mark_pos(word):
    if word == ';' or word == '--' or word == '...':
        return ':'
    elif word == '{':
        return '('
    elif word == '}':
        return ')'
    elif word == '!' or word == '?':
        return '.'
    else:
        return word


if __name__ == "__main__":
    start()
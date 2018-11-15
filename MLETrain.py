import sys


def start():
    train_file = open("ass1-tagger-train1")
    e_file = open("e_file.txt", "a")
    #q_file = open(sys.argv[3], "a")
    dic_e, pos_count_dic = create_e(train_file)
    dic_e = write_to_e_file(dic_e, e_file)
    train_file.close()
    train_file = open("ass1-tagger-train1")
    dic_q = write_to_q_file(train_file)
    train_file.close()

    # test for get_e/get_q
    # print (get_e("A", "FINE", dic_e, pos_count_dic))
    # print (get_q("FINE", "FINE", "FINE", dic_q))
    return dic_e, dic_q, pos_count_dic


def write_to_e_file(dic_e, e_file):
    for word in dic_e:
        for en in dic_e[word].keys():
            e_file.write(word + " " + en + "\t" + str(dic_e[word][en]) + "\n")
    e_file.close()

    return dic_e  # for later use in get_e method


def write_to_q_file(train_file):
    q_file = open("q_file.txt", "a")
    dic_q = create_q(train_file)
    for en in dic_q:
        q_file.write(en + "\t" + str(dic_q[en]) + "\n")
    q_file.close()

    return dic_q  # for later use in get_q method


def create_q(train_file):
    dic = {}
    lines = train_file.readlines()
    prev = None
    pprev = None
    for line in lines:
        by_spaces = line.split(" ")
        for pos in by_spaces:
            # extract pos
            pos_ = pos.split("/")[1].split("\n")[0]
            # create 3 sequences for a, a-b, a-b-c
            pos_cur = pos_
            add_entry_to_q_dict(dic, pos_cur)
            if prev != None and pprev == None:
                pos_inc_prev = prev + " " + pos_cur
                add_entry_to_q_dict(dic, pos_inc_prev)
            elif prev != None and pprev != None:
                pos_inc_prev = prev + " " + pos_cur
                pos_inc_pprev = pprev + " " + prev + " " + pos_cur
                add_entry_to_q_dict(dic, pos_inc_prev)
                add_entry_to_q_dict(dic, pos_inc_pprev)
            pprev = prev
            prev = pos_
    return dic


def add_entry_to_q_dict(dic, pos):
    add_entry_to_counter_dict(dic, pos)


# counter dictionary is dict that the values are the sum of the apperances of the keys
# for example dic[a] = 2 means that a inserted 2 times to dictionary
# the method receives dic & entry then updates the dictonary accordingly
def add_entry_to_counter_dict(dic, entry):
    if entry in dic.keys():
        dic[entry] += 1
        return
    dic[entry] = 1


def create_e(train_file):
    dic = {}
    pos_count_dic = {}  # dictionary to count appearances of each part of speech
    lines = train_file.readlines()
    for line in lines:
        by_spaces = line.split(" ")
        for pos in by_spaces:
            by_slash = pos.split("/")
            word = by_slash[0]
            pos = by_slash[1].split("\n")[0]
            add_entry_to_counter_dict(pos_count_dic, pos)  # add pos to pos_count_dic
            if word not in dic.keys():
                dic[word] = {}
                dic[word][pos] = 1
            else:
                if pos in dic[word].keys():
                    dic[word][pos] += 1
                else:
                    dic[word][pos] = 1
    return dic, pos_count_dic


# return q based on calc of:  q(t3|t1,t2) = count(t1,t2,t3) / count(t1,t2)
def get_q(tag1, tag2, tag3, dic_q):
    count_t1_t2_t3 = dic_q[tag1 + " " + tag2 + " " + tag3]
    count_t1_t2 = dic_q[tag1 + " " + tag2]
    return (count_t1_t2_t3 / count_t1_t2)


# return e based on calc of:  e(word|part_of_speech) = count(word,pos) / count(pos)
def get_e(word, pos, dic_e, pos_count_dic):
    count_word_pos = dic_e[word][pos]
    count_pos = pos_count_dic[pos]
    return (count_word_pos / count_pos)

# def main():
#     start()
#
#
# main()

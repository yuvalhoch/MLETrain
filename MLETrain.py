import sys


def start():
    train_file = open("ass1-tagger-train")
    e_file = open("e_file.txt", "a")
    #q_file = open(sys.argv[3], "a")
    dic_e = create_e(train_file)
    write_to_e_file(dic_e, e_file)
    train_file.close()
    train_file = open("ass1-tagger-train")
    write_to_q_file(train_file)
    train_file.close()


def write_to_e_file(dic_e, e_file):
    for word in dic_e:
        for en in dic_e[word].keys():
            e_file.write(word + " " + en + "\t" + str(dic_e[word][en]) + "\n")
    e_file.close()


def write_to_q_file(train_file):
    q_file = open("q_file.txt", "a")
    dic_q = create_q(train_file)
    for en in dic_q:
        q_file.write(en + "\t" + str(dic_q[en]) + "\n")
    q_file.close()


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
    if pos in dic.keys():
        dic[pos] += 1
        return
    dic[pos] = 1


def create_e(train_file):
    dic = {}
    lines = train_file.readlines()
    for line in lines:
        by_spaces = line.split(" ")
        for pos in by_spaces:
            by_slash = pos.split("/")
            word = by_slash[0]
            pos = by_slash[1].split("\n")[0]
            if word not in dic.keys():
                dic[word] = {}
                dic[word][pos] = 1
            else:
                if pos in dic[word].keys():
                    dic[word][pos] += 1
                else:
                    dic[word][pos] = 1
    return dic


def main():
    start()


main()

import MLETrain
import MLETrain as mletrain
import sys
import Utility
import re

"""
given word as x, tag1 and tag2 (tags of previous words)
iterate over all possible part of speeches ("poses")
find which one is the the best tag for x, the pos with the highest probability
using formula t3 = pos which maximize: e(x|t3)*q(t3|t1,t2)
pos_count_dic is count_dic which its keys represent the possible part of speeches
"""


def greedy_tag_word(x, t1, t2, dic_e, dic_q, pos_list):
    t3 = "default"
    max_t3_prob = 0
    # dic_e = mletrain.e_dic
    # dic_q = mletrain.q_dic
    # print (dic_e['City']['NNP'])
    # print (str(dic_e['influential']))

    # If the word has not in the corpus, try to find the tag by checking the suffix.
    if x not in dic_e.keys():
        x = MLETrain.find_word_signature(x)
    # if word is unknown tag it as UNK
    if x == 'UNK':
        return 'UNK'
    elif x == 'CD':
        return 'CD'

    for pos in pos_list:
        if pos in dic_e[x].keys():  # first check if the given word could be pos (if you've seen it before)
            e_x_given_t3 = MLETrain.get_e(x, pos)
            q_t3_given_t1t2 = MLETrain.get_q(t1, t2, pos)
            cur_pos_porb = e_x_given_t3 * q_t3_given_t1t2  # calc cur pos probability using e(x|t3)*q(t3|t1,t2)
            #print(cur_pos_porb)
            # update t3 to hold the pos which maximize prob
            if cur_pos_porb > max_t3_prob:
                max_t3_prob = cur_pos_porb
                t3 = pos
    return t3


def main():
    # arguments are: input_file_name, q.mle, e.mle, out_file_name, extra_file_name
    #inp_file_path = sys.argv[1]
    #q_mle_file = sys.argv[2]
    #e_mle_file = sys.argv[3]
    #out_file_name = sys.argv[4]
    #extra_file = sys.argv[5]
    ########################################
    inp_file_path = "ass1-tagger-test-input"
    q_mle_file = "q_file.txt"
    e_mle_file = "e_file.txt"
    out_file_name = "output.txt"
    extra_file = "extra_file_name.txt"
    ########################################
    pos_list = Utility.read_possible_poses_from_file(extra_file)
    dic_q = Utility.generate_q_dic_from_file(q_mle_file)
    dic_e = Utility.generate_e_dic_from_file(e_mle_file)
    out_file = open(out_file_name, "a")
    mletrain.load_the_model(q_mle_file, e_mle_file)

    inp_file = open(inp_file_path, "r")
    lines = inp_file.readlines()  # In order to go over the lines in input file.
    for line in lines:
        line = line.replace("\n","")
        # in the begging of each sentence reset the prev and pprev tag to none
        prev_tag = ''  # none
        pprev_tag = ''  # none

        # split the sentence
        words = line.split("\n")[0].split(" ")
        for i in range(words.__len__()):
            cur_word_tag = greedy_tag_word(words[i], pprev_tag, prev_tag,
                                           dic_e, dic_q, pos_list)
            # If last word
            if (i == words.__len__() - 1):
                # If its the last word, first split to word and . (if possible)
                # then tag each of them and write to file. doesn't write the space at end of a line
                pattern = re.compile(r'(\s+|[{}])'.format(re.escape(".")))
                t = [part for part in pattern.split(words[i]) if part.strip()]
                if t.__len__() == 2:  # if last word is: "word." write word/tag and ./tag
                    t0_tag = greedy_tag_word(t[0], pprev_tag, prev_tag, dic_e, dic_q, pos_list)
                    out_file.write(t[0] + "/" + t0_tag + " ")
                    t1_tag = greedy_tag_word(t[1], prev_tag, t0_tag, dic_e, dic_q, pos_list)
                    out_file.write(t[1] + "/" + t1_tag)
                # Last word is regular word...
                else:
                    out_file.write(t[0] + "/" + cur_word_tag)
            # Regular word in sentence (not last)
            else:
                out_file.write(words[i] + "/" + cur_word_tag + " ")

            # Update pprev and prev tag for next iteration...
            pprev_tag = prev_tag
            prev_tag = cur_word_tag
    out_file.close()


if __name__ == "__main__":
    main()

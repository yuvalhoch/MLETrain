import os

import ExtractFeatures
import MLETrain
import MLETrain as mletrain
import sys
import Utility
import re
import liblin as lbln
import Utility as util

"""
given word as x, tag1 and tag2 (tags of previous words)
iterate over all possible part of speeches ("poses")
find which one is the the best tag for x, the pos with the highest probability
using formula t3 = pos which maximize: e(x|t3)*q(t3|t1,t2)
pos_count_dic is count_dic which its keys represent the possible part of speeches
"""


def greedy_tag_word(feature_list, llb):
    t3 = "default"
    max_t3_prob = 0

    tag_porb_list = llb.predict(feature_list)  # calc cur feature list probability using the model
    # update t3 to hold the tag which maximize prob
    for tag, prob_tag in enumerate(tag_porb_list, 0):
        cur_tag_porb = prob_tag
        if cur_tag_porb > max_t3_prob:
            max_t3_prob = cur_tag_porb
            t3 = tag  # tag number in the list, counting from 0
    return t3


def main():
    # arguments are: input_file_name, q.mle, e.mle, out_file_name, extra_file_name
    # input_file_name = sys.argv[1]
    # modelname = sys.argv[2]
    # feature_map_file  = sys.argv[3]
    # out_file_name = sys.argv[4]
    ########################################
    input_file_name = "ass1-tagger-test-input"
    modelname = "MODEL_FILE"
    feature_map_file = "feature_map_file"
    out_file_name = "out_file"
    ########################################
    os.system("python ExtractFeatures.py " + input_file_name + " feature_file_temp")
    os.system("python ConvertFeatures.py feature_map_file " + feature_map_file + " feature_vecs_temp")
    llb = lbln.LiblinearLogregPredictor(modelname)

    pos_list = Utility.read_possible_poses_from_file("pos_file")

    out_file = open(out_file_name, "a")
    input_file_name = open("ass1-tagger-test-input")

    feature_vecs = open("feature_vecs_temp", "r")
    word_lines = input_file_name.readline()
    for word in word_lines.split(" "):
        line = feature_vecs.readline()  # In order to go over the lines in input file.
        line = line.replace("\n", "")
        # in the begging of each sentence reset the prev and pprev tag to none
        prev_tag = ''  # none
        pprev_tag = ''  # none

        # split the sentence
        features = line[1:].split(" ")
        for feature in features:
            feature.strip(":1")

        # features stands for word features
        cur_word_tag_index = greedy_tag_word(features, llb)
        cur_word_tag = pos_list[cur_word_tag_index]
        if (word.endswith("\n")):
            out_file.write(word.strip("\n") + "/" + cur_word_tag + "\n")
        else:
            out_file.write(word + "/" + cur_word_tag + " ")

    out_file.close()


if __name__ == "__main__":
    main()

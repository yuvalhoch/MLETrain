import json
import sys
import liblin as lbln
import MEMMUtils as MemmUtil


def greedy_tag_word(num_to_pos_dic, features_set_to_on_list, llb):
    # llb.predict needs features_set_to_on_list, returns dic contains probabilities for each tag, such that
    # { 1->0.3, 2->0.5, 3->0.1 } means that probability for tag #2 is 0.5
    # we need to find the maximizer_key - the key which maximize tag_porb.
    # then we convert maximizer_key (which is a number stands for pos) to actual pos using num_to_pos_dic[maximizer_key]
    # caution!!! remember that tag to pos starts to count from 1

    maximizer_key = 0
    max_tag_prob = 0

    tag_porb_dic = llb.predict(features_set_to_on_list)  # calcs using the model
    # update maximizer_key to hold the index which maximize tag_porb.
    for key in tag_porb_dic.keys():
        cur_tag_porb = tag_porb_dic[key]
        if cur_tag_porb > max_tag_prob:
            max_tag_prob = cur_tag_porb
            maximizer_key = key  # update maximizer_key

    # convert maximizer_key to actual pos
    return num_to_pos_dic[int(maximizer_key)]  # return pos


def main():
    if len(sys.argv) != 5:
        print ("bad parameters!")
        exit(1)

    inp_file = open(sys.argv[1], "r")
    llb = lbln.LiblinearLogregPredictor(sys.argv[2])
    with open(sys.argv[3], 'r') as f:
        features_to_num_dic = json.load(f)
        # features_to_num_dic[feature] = feature number.
        # exp: features_to_num_dic["pprev_word=Chicago"] = 108
    out_file = open(sys.argv[4], "a")
    num_to_pos_dic = MemmUtil.create_num_to_pos_dic("pos_file")

    sentences_lines = inp_file.readlines()
    for sentences in sentences_lines:
        words = sentences.replace("\n", "").split(" ")
        # in the begging of each sentence prev and pprev's word and tags are set to "start".
        prev_word = "start"
        pprev_word = "start"
        prev_tag = "start"
        pprev_tag = "start"

        # run over the words in the sentence
        # build features, greedy tag and write to "out" file
        for i in range(len(words)):

            # build features, returns list with all the features which are set to 1 in feature_vec & actual word
            features_set_to_on_list, word = MemmUtil.build_features(features_to_num_dic, i, pprev_tag, prev_tag, words)

            # greedy tag current word
            cur_word_tag = greedy_tag_word(num_to_pos_dic, features_set_to_on_list, llb)

            # write to file
            if (i == len(words) - 1): # If last word
                out_file.write(word + "/" + cur_word_tag + "\n")
            else:
                out_file.write(word + "/" + cur_word_tag + " ")

            # save for next word
            pprev_tag = prev_tag
            prev_tag = cur_word_tag

    out_file.close()


main()

import sys
import math
import MLETrain as mletrain
import liblin as lbln
import json
import MEMMUtils as MemmUtil


def start():
    if len(sys.argv) != 5:
        print ("bad parameters!")
        exit(1)

    tagger_test_input = open(sys.argv[1], "r")
    tagger_test = open("ass1-tagger-test")
    llb = lbln.LiblinearLogregPredictor(sys.argv[2])
    with open(sys.argv[3], 'r') as f:
        features_to_num_dic = json.load(f)
        # features_to_num_dic[feature] = feature number.
        # exp: features_to_num_dic["pprev_word=Chicago"] = 108
    output_file = open(sys.argv[4], "a")





    tag_set, words_dic = mletrain.load_the_model("q_file.txt", "e_file.txt")
    lines = tagger_test_input.readlines()
    num_words = 0
    incorrect = 0 #########
    line_test = tagger_test.readline()
    for line in lines:
        word = line.split("\n")[0].split(" ")
        word_test = line_test.split("\n")[0].split(" ") ###############
        num_words += len(word)
        score = viterbi(word, words_dic, features_to_num_dic, llb)

        for i in range(0, len(word_test)): ################
            word1 = word_test[i]
            word2 = (' '.join(["{}/{}".format(word[i], score[i])]))
            if word1 != word2: ############
                incorrect += 1 ############
                #print ("test: " + word1 + "\toutput: " + word2 + "\n")

        output_file.write(' '.join(["{}/{}".format(word, label) for word, label in zip(word, score)]))
        output_file.write("\n")
        line_test = tagger_test.readline() #######
    output_file.close()

    percent = 100 - (100 * incorrect / num_words) ##############3
    print (percent)#################
    tagger_test.close() ###############
    tagger_test_input.close()


def viterbi(word_seq, words_dic, features_to_num_dic, llb):
    prob_values = [{('', ''): 0.0}]
    back_pointers = []
    for i, word in enumerate(word_seq):
        # If the word has not in the corpus, try to find the tag by checking the suffix.
        if word not in words_dic:
            word = mletrain.find_word_signature(word)
        prob = {}
        tags = {}
        for t_tag, t in prob_values[i]:
            # If the word tag in un-known or 'CD' (probably a number),
            # set the probability of this tag to be 1.
            if word == 'UNK' or word == 'CD':
                prob[(t, word)] = 1
                tags[(t, word)] = t_tag
            else:
                # Pruning the un-seen tags
                available_tags = words_dic[word]
                # Move on the optional tags and get for every one of them the score
                # by calculating the log probability of e and q values.
                for r in available_tags:
                    prob_ = get_score(word, r, t, t_tag, word_seq, features_to_num_dic, llb, i)
                    score = prob_values[i][(t_tag, t)] + prob_
                    # Update the scores by the max score of (t, r).
                    if ((t, r) not in prob) or score > prob[(t, r)]:
                        prob[(t, r)] = score
                        tags[(t, r)] = t_tag
        prob_values.append(prob)
        back_pointers.append(tags)
    # Initial max probability.
    max_prob_cur = float("-inf")
    # Extract the cur and prev POS.
    prev, cur = list(prob_values[len(word_seq)].keys())[0]
    # Move on the probabilities.
    for t, r in prob_values[len(word_seq)]:
        max_prob = prob_values[len(word_seq)][(t, r)]
        # Change the max_probability according to the highest value.
        if max_prob > max_prob_cur:
            max_prob_cur = max_prob
            cur = r
            prev = t
    # Create y_seq to be the expected values by the order of the word_seq.
    y_seq = []
    y_seq.append(cur)
    if len(word_seq) > 1:
        y_seq.append(prev)
    prev_pos = cur
    pprev_pos = prev
    for i in range(len(prob_values) - 2, 1, -1):
        t = back_pointers[i][(pprev_pos, prev_pos)]
        y_seq.append(t)
        prev_pos = pprev_pos
        pprev_pos = t
    return list(reversed(y_seq))


# find & returns probability of given tag (cur_tag)
def get_score(word, cur_tag, prev_tag, pprev_tag, words, features_to_num_dic, llb, word_idx_in_words):
    # build features, returns list with all the features which are set to 1 in feature_vec & actual word
    features_set_to_on_list, word = MemmUtil.build_features(features_to_num_dic, word_idx_in_words, pprev_tag, prev_tag, words)

    # create pos_to_num_dic from file
    pos_to_num_dic = MemmUtil.create_pos_to_num_dic("pos_file")

    # convert pos to label_num
    if cur_tag in pos_to_num_dic.keys():
        label_num = pos_to_num_dic[cur_tag]
    else:
        label_num = 5  # arbitary!

    # calculate probabilities for each label
    tag_porb_dic = llb.predict(features_set_to_on_list)  # calcs using the model

    # find the probability for cur_tag (label)
    cur_tag_porb = float("-inf")
    cur_tag_porb = tag_porb_dic[str(label_num)]

    # return probability for cur_tag (label)
    return cur_tag_porb


if __name__ == "__main__":
    start()
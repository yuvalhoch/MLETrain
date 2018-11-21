import json
import re
import sys
import liblin as lbln


def greedy_tag_word(num_to_pos_dic, features_set_to_on_list, llb):
    # llb.predict needs features_set_to_on_list, returns list contains probabilities for each tag, such that
    # [ 0.3,0.5,0,1 ] means that probability for tag #2 is 0.5
    # caution!!! remember that tag to pos starts to count from 1
    # [while list indexes starting to count from 0!
    # therefore we will calc using num_to_pos_dic[maximizer_index_of_predict+1]]
    # ***or in this case set index counter in enumerate to start from 1!***

    maximizer_index = 0
    max_tag_prob = 0
    index = 1

    tag_porb_list = llb.predict(features_set_to_on_list)  # calcs using the model
    # update tag to hold the index which maximize prob
    for prob_of_tag in tag_porb_list.values():
        cur_tag_porb = prob_of_tag
        if cur_tag_porb > max_tag_prob:
            max_tag_prob = cur_tag_porb
            maximizer_index = index  # tag index in the list, counting from 1!
        index+=1

    # convert maximizer_index to actual pos
    return num_to_pos_dic[maximizer_index]  # return pos

# def greedy_tag_word(num_to_pos_dic, features_set_to_on_list, llb):
#     # llb.predict needs features_set_to_on_list, returns list contains probabilities for each tag, such that
#     # [ 0.3,0.5,0,1 ] means that probability for tag #2 is 0.5
#     # caution!!! remember that tag to pos starts to count from 1
#     # [while list indexes starting to count from 0!
#     # therefore we will calc using num_to_pos_dic[maximizer_index_of_predict+1]]
#     # ***or in this case set index counter in enumerate to start from 1!***
#
#     maximizer_index = 0
#     max_tag_prob = 0
#
#     tag_porb_list = llb.predict(features_set_to_on_list)  # calcs using the model
#     # update tag to hold the index which maximize prob
#     for index, prob_of_tag in enumerate(tag_porb_list, 1):
#         cur_tag_porb = prob_of_tag
#         if cur_tag_porb > max_tag_prob:
#             max_tag_prob = cur_tag_porb
#             maximizer_index = index  # tag index in the list, counting from 1!
#
#     # convert maximizer_index to actual pos
#     return num_to_pos_dic[maximizer_index]  # return pos

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
    num_to_pos_dic = create_num_to_pos_dic("pos_file")

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
            features_set_to_on_list = []  # list with all the features which are set to 1 in feature_vec

            # calc features for current word
            word = words[i]
            prev_word = words[i - 1] if i > 0 else "start"
            pprev_word = words[i - 2] if i > 1 else "start"
            next_word = words[i + 1] if i < (len(words) - 1) else "end"
            nnext_word = words[i + 2] if i < (len(words) - 2) else "end"

            # find actual features numbers using features_to_num_dic, then add them to features_set_to_on_list
            f1 = find_feature_number("form=" + word, features_to_num_dic)
            f2 = find_feature_number("prev_word=" + prev_word, features_to_num_dic)
            f3 = find_feature_number("prev_tag=" + prev_tag, features_to_num_dic)
            f4 = find_feature_number("pprev_word=" + pprev_word, features_to_num_dic)
            f5 = find_feature_number("pprev_tag=" + pprev_tag, features_to_num_dic)
            f6 = find_feature_number("next_word=" + next_word, features_to_num_dic)
            f7 = find_feature_number("nnext_word=" + nnext_word, features_to_num_dic)
            add_to_feature_set_to_on_list(f1,features_set_to_on_list)
            add_to_feature_set_to_on_list(f2,features_set_to_on_list)
            add_to_feature_set_to_on_list(f3,features_set_to_on_list)
            add_to_feature_set_to_on_list(f4,features_set_to_on_list)
            add_to_feature_set_to_on_list(f5,features_set_to_on_list)
            add_to_feature_set_to_on_list(f6,features_set_to_on_list)
            add_to_feature_set_to_on_list(f7,features_set_to_on_list)
            # add also features_using_word_signatures, they are also added to features_set_to_on_list
            calc_features_using_word_signatures(word,features_to_num_dic,features_set_to_on_list)

            features_set_to_on_list.sort()  # sort the features to constant specific order (increasing/decreasing)

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

        # for word in words:
        #     # build features, greedy tag and write to "out" file
        #     add_to_feature_set_to_on_list(features_to_num_dic["form=" + word],features_set_to_on_list
        #     features_to_num_dic["prev_word=" + prev_word]
        #     features_to_num_dic["prev_tag=" + prev_tag]
        #     features_to_num_dic["pprev_word=" + pprev_word]
        #     features_to_num_dic["pprev_tag=" + pprev_tag]
        #     features_to_num_dic["next_word=" + next_word]
        #     features_to_num_dic["nnext_word=" + nnext_word]
        #
        #     if count_word_appearance_dic[word] == 1:  # if word appears only once in the text
        #         calc_features_using_word_signatures(word, feature_vec)
        #
        #     pprev_tag = prev_tag
        #     prev_tag = cur_word_tag
        #
        # # in the begging of each sentence reset the prev and pprev tag to none
        # prev_tag = ''  # none
        # pprev_tag = ''  # none
        #
        # # split the sentence
        # features = line[1:].split(" ")
        # for feature in features:
        #     feature.strip(":1")
        #
        # # features stands for word features
        # cur_word_tag_index = greedy_tag_word(features, llb)
        # cur_word_tag = pos_list[cur_word_tag_index]
        # if (word.endswith("\n")):
        #     out_file.write(word.strip("\n") + "/" + cur_word_tag + "\n")
        # else:
        #     out_file.write(word + "/" + cur_word_tag + " ")
    out_file.close()


def find_feature_number(feature, features_to_num_dic):
    if feature in features_to_num_dic.keys():
        return features_to_num_dic[feature]
    return None


def add_to_feature_set_to_on_list(feature_number, features_set_to_on_list):
    if feature_number is not None:
        features_set_to_on_list.append(int(feature_number))  # NOTE we added them as STRINGS not ints


def calc_features_using_word_signatures(word, features_to_num_dic, features_set_to_on_list):
    # calc the 2, 3 and 4-suffix, and also 2, 3 and 4-prefix of word,
    # find actual features numbers using features_to_num_dic, then add them to features_set_to_on_list
    if len(word) > 2 and word[len(word) - 1] != '.':
        if len(word) > 3:
            if len(word) > 4:
                f1 = find_feature_number("4_suffix=" + word[-4:], features_to_num_dic)
                add_to_feature_set_to_on_list(f1, features_set_to_on_list)
                f2 = find_feature_number("4_prefix=" + word[:4], features_to_num_dic)
                add_to_feature_set_to_on_list(f2, features_set_to_on_list)
            f3 = find_feature_number("3_suffix=" + word[-3:], features_to_num_dic)
            add_to_feature_set_to_on_list(f3, features_set_to_on_list)
            f4 = find_feature_number("3_prefix=" + word[:3], features_to_num_dic)
            add_to_feature_set_to_on_list(f4, features_set_to_on_list)
        f5 = find_feature_number("2_suffix=" + word[-2:], features_to_num_dic)
        add_to_feature_set_to_on_list(f5, features_set_to_on_list)
        f6 = find_feature_number("2_prefix=" + word[:2], features_to_num_dic)
        add_to_feature_set_to_on_list(f6, features_set_to_on_list)

    # The feature is if the word has '-'
    if '-' in word:
        f7 = find_feature_number("contains_hyphen=true", features_to_num_dic)
        add_to_feature_set_to_on_list(f7, features_set_to_on_list)
    # The feature is if the word has '/'
    if '/' in word:
        f8 = find_feature_number("contains_slash=true", features_to_num_dic)
        add_to_feature_set_to_on_list(f8, features_set_to_on_list)
    # The feature is if the word has number.
    if any(x.isdigit() for x in word):
        f9 = find_feature_number("has_number=true", features_to_num_dic)
        add_to_feature_set_to_on_list(f9, features_set_to_on_list)
    # The feature is if the whole word with upper case letters.
    if word.isupper():
        f10 = find_feature_number("is_upper=true", features_to_num_dic)
        add_to_feature_set_to_on_list(f10, features_set_to_on_list)
    # The feature is if the word start with upper case letter.
    elif word[0].isupper():
        f11 = find_feature_number("start_upper=true", features_to_num_dic)
        add_to_feature_set_to_on_list(f11, features_set_to_on_list)


# reads poses file, creates dic from line number to pos and returns it, exp: dic[line # which contains pos] = pos
def create_num_to_pos_dic(pos_file_path):
    num_to_pos_dic = {}
    pos_file = open(pos_file_path, "r")
    lines = pos_file.readlines()  # In order to go over the lines in pos_file.
    for counter, line in enumerate(lines, 1):
        num_to_pos_dic[counter] = line.replace("\n","")
    pos_file.close()
    return num_to_pos_dic


main()

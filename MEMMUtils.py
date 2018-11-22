def find_feature_number(feature, features_to_num_dic):
    if feature in features_to_num_dic.keys():
        return features_to_num_dic[feature]
    return None


def add_to_feature_set_to_on_list(feature_number, features_set_to_on_list):
    if feature_number is not None:
        features_set_to_on_list.append(int(feature_number))  # NOTE we added them as INTS not strings


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


# reads poses file, creates dic from pos to line number and returns it, exp: dic[pos] = (line # which contains pos)
def create_pos_to_num_dic(pos_file_path):
    pos_to_num_dic = {}
    pos_file = open(pos_file_path, "r")
    lines = pos_file.readlines()  # In order to go over the lines in pos_file.
    for counter, line in enumerate(lines, 1):
        pos_to_num_dic[line.replace("\n","")] = counter
    pos_file.close()
    return pos_to_num_dic


# builds features, returns list with all the features which are set to 1 in feature_vec & actual word
def build_features(features_to_num_dic, word_idx_in_words, pprev_tag, prev_tag, words):
    features_set_to_on_list = []  # list with all the features which are set to 1 in feature_vec
    # calc features for current word
    word = words[word_idx_in_words]
    prev_word = words[word_idx_in_words - 1] if word_idx_in_words > 0 else "start"
    pprev_word = words[word_idx_in_words - 2] if word_idx_in_words > 1 else "start"
    next_word = words[word_idx_in_words + 1] if word_idx_in_words < (len(words) - 1) else "end"
    nnext_word = words[word_idx_in_words + 2] if word_idx_in_words < (len(words) - 2) else "end"
    # find actual features numbers using features_to_num_dic, then add them to features_set_to_on_list
    f1 = find_feature_number("form=" + word, features_to_num_dic)
    f2 = find_feature_number("prev_word=" + prev_word, features_to_num_dic)
    f3 = find_feature_number("prev_tag=" + prev_tag, features_to_num_dic)
    f4 = find_feature_number("pprev_word=" + pprev_word, features_to_num_dic)
    f5 = find_feature_number("pprev_tag=" + pprev_tag, features_to_num_dic)
    f6 = find_feature_number("next_word=" + next_word, features_to_num_dic)
    f7 = find_feature_number("nnext_word=" + nnext_word, features_to_num_dic)
    add_to_feature_set_to_on_list(f1, features_set_to_on_list)
    add_to_feature_set_to_on_list(f2, features_set_to_on_list)
    add_to_feature_set_to_on_list(f3, features_set_to_on_list)
    add_to_feature_set_to_on_list(f4, features_set_to_on_list)
    add_to_feature_set_to_on_list(f5, features_set_to_on_list)
    add_to_feature_set_to_on_list(f6, features_set_to_on_list)
    add_to_feature_set_to_on_list(f7, features_set_to_on_list)
    # add also features_using_word_signatures, they are also added to features_set_to_on_list
    calc_features_using_word_signatures(word, features_to_num_dic, features_set_to_on_list)
    features_set_to_on_list.sort()  # sort the features to constant specific order (increasing/decreasing)
    return features_set_to_on_list, word

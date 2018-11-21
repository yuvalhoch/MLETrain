import sys


def read_file(input_file, features_file):
    lines = input_file.readlines()
    count_word_appearance_dic = {}
    pos_count_dic = {}
    text_lines = []
    for line in lines:
        words_and_tags = line.split(" ")  # contain words and their tag ex. Home/NN
        for pair in words_and_tags:  # run over the txt count appearances of each word
            # splits only on last occurrence of '/' in string, for words like "higher/lower/Adjective"
            word = pair.rsplit("/", 1)[0]
            add_entry_to_counter_dict(count_word_appearance_dic, word) # counts the appreacnes of word in text
            add_entry_to_counter_dict(pos_count_dic, pair.rsplit("/", 1)[1].replace("\n",""))  # counts the appreacnes of specific pos in text
        # each line in the corpus stands for list entry ex. "Hey/NN my/VERB" is entry, save it on memory to later read
        text_lines.append(words_and_tags)
    for words_and_tags in text_lines: # run on each line ("Hey/NN my/VERB") and extract her features string
        words_feature_vec_str = extract_feature_line(words_and_tags, count_word_appearance_dic)
        for feature_line_str in words_feature_vec_str:
            # writes entire line's features to output feature file [there's multiple words in line..]
            # note that each word has entire "word's feature" line in output feature file...
            # We are writing here all the words that assembles specific line.
            features_file.write(feature_line_str)

    write_pos_file(pos_count_dic) # write to pos file all the possible POSes...


# pos file is file which contain all the possible POSes. each line contains a pos.
def write_pos_file(pos_dic):
    pos_file = open("pos_file", 'a')
    for pos in pos_dic.keys():
        pos_file.write(pos + "\n")
    pos_file.close()


def extract_feature_line(words_and_tags, count_word_appearance_dic):
    words_array = []
    words_feature_vec_str = []  # contains word_feature_vec_str for EACH word
    for i in range(len(words_and_tags)):
        # splits only on last occurrence of '/' in string, for words like "higher/lower/Adjective"
        word, tag = words_and_tags[i].replace("\n", "").rsplit("/", 1)
        words_array.append((word,tag))

    for i in range(len(words_array)):
        feature_vec = []
        word, tag = words_array[i]
        prev_word, prev_tag = words_array[i-1] if i > 0 else ("start","start")
        pprev_word, pprev_tag = words_array[i-2] if i > 1 else ("start","start")
        next_word, next_tag = words_array[i+1] if i < (len(words_array)-1) else ("end","end")
        nnext_word, nnext_tag = words_array[i+2] if i < (len(words_array)-2) else ("end","end")

        # create strings to add to feature file
        feature_vec.append(tag)  # first thing in feature vec line is actual word tag
        feature_vec.append("form=" + word)
        feature_vec.append("tag=" + tag)
        feature_vec.append("prev_word=" + prev_word)
        feature_vec.append("prev_tag=" + prev_tag)
        feature_vec.append("pprev_word=" + pprev_word)
        feature_vec.append("pprev_tag=" + pprev_tag)
        feature_vec.append("next_word=" + next_word)
        feature_vec.append("next_tag=" + next_tag)
        feature_vec.append("nnext_word=" + nnext_word)
        feature_vec.append("nnext_tag=" + nnext_tag)

        if count_word_appearance_dic[word] == 1:  # if word appears only once in the text
            word_signatures(word,feature_vec)
            
        # convert feature vector of specific word to string and append it to list of fv as string of all words
        words_feature_vec_str.append(' '.join(feature_vec)+ "\n")

    return words_feature_vec_str


def word_signatures(word, features_list):
    # The feature is 2, 3 and 4-suffix, and also 2, 3 and 4-prefix.
    if len(word) > 2 and word[len(word) - 1] != '.':
        if len(word) > 3:
            if len(word) > 4:
                features_list.append("4_suffix=" + word[-4:])
                features_list.append("4_prefix=" + word[:4])
            features_list.append("3_suffix=" + word[-3:])
            features_list.append("3_prefix=" + word[:3])
        features_list.append("2_suffix=" + word[-2:])
        features_list.append("2_prefix=" + word[:2])
    # The feature is if the word has '-'
    if '-' in word:
        features_list.append("contains_hyphen=true")
    # The feature is if the word has '/'
    if '/' in word:
        features_list.append("contains_slash=true")
    # The feature is if the word has number.
    if any(x.isdigit() for x in word):
        features_list.append("has_number=true")
    # The feature is if the whole word with upper case letters.
    if word.isupper():
        features_list.append("is_upper=true")
    # The feature is if the word start with upper case letter.
    elif word[0].isupper():
        features_list.append("start_upper=true")



def add_entry_to_counter_dict(dic, entry):
    if entry in dic.keys():
        dic[entry] += 1
        return
    dic[entry] = 1


def main():
    if len(sys.argv) != 3:
        print ("bad parameters!")
        exit(1)

    corpus_file_name = sys.argv[1]
    features_file_name = sys.argv[2]
    corpus_file = open(corpus_file_name, 'r')
    features_file = open(features_file_name, 'a')
    read_file(corpus_file, features_file)

    corpus_file.close()
    features_file.close()


main()

import sys
import MLETrain as mletrain
END = 'end'
START = 'start'
punctuation_marks = ['.', ',', '"', '``', '(', ')', '=', '-', '!', '@', '#', '?',
                     '$', '%', '&', '*', '+', '{', '}', '\'\'', ':', '...', ';', '--']


def start():
    corpus_file  = open(sys.argv[1])
    features_file = open(sys.argv[2], "a")
    data, words_dic = extract_features(corpus_file)
    for words, pos in data:
        for i, word in enumerate(words):
            features_list = create_features_list(words, pos, word, i, words_dic[word])
            features_string = " ".join([feature for feature in features_list])
            if len(pos) == 0:
                features_file.write(features_string + "\n")
            else:
                features_file.write(pos[i] + " " + features_string + "\n")
    corpus_file.close()
    features_file.close()


def extract_features(corpus_file):
    words_dic = {}
    data = []
    pos_dic = {}
    # Move on the lines in the corpus file.
    lines = corpus_file.readlines()
    for line in lines:
        words = []
        pos = []
        # Split every line to the pairs of word/POS.
        pairs = line.split("\n")[0].split(" ")
        # Move on the pairs of every line, and split them into word and POS.
        for pair in pairs:
            by_slash = pair.split("/")
            word = by_slash[0]
            if len(by_slash) == 2:
                pos_ = by_slash[1]
                if pos_ not in pos_dic.keys():
                    pos_dic[pos_] = ' '
                if (not pos_.isupper()) and pos not in punctuation_marks:
                    break
                # Words is a array of the all file words, and pos is a array of all the POS.
                pos.append(pos_)
                words.append(word)
                add_to_words_dic(word, words_dic)
                # If the word is in words dictionary, add 1 to the number of appearances
                # of that word, else - create a new entry with the number 1.
            elif len(by_slash) > 2:
                for i in range(len(by_slash) - 1):
                    pos.append(by_slash[-1])
                    words.append(by_slash[i])
                    add_to_words_dic(by_slash[i], words_dic)
            else:
                words.append(word)
                add_to_words_dic(word, words_dic)
        # Append to data the pair of words and POS for every line in the corpus.
        data.append((words, pos))
    corpus_file.close()
    try:
        pos_file = open("pos_file")
        pos_file.close()
    except:
        pos_file = open("pos_file", "a")
        for pos in pos_dic.keys():
            pos_file.write(pos + "\n")
        pos_file.close()
    return data, words_dic


def add_to_words_dic(word, words_dic):
    if word in words_dic.keys():
        words_dic[word] += 1
    else:
        words_dic[word] = 1


def create_features_list(words, pos, cur, i, rar_word):
    features_list = []
    # The feature is form=word
    form = "form=" + cur
    features_list.append(form)
    if len(pos) != 0:
        tag = "tag=" + (pos[i])
        features_list.append(tag)
        # The feature is prev_tag=prev_POS
        prev_tag = "prev_tag=" + (pos[i - 1] if i != 0 else START)
        features_list.append(prev_tag)

        # The feature is prev_prev_tag=prev_prev_POS
        if i > 1:
            pprev_tag = "pprev_tag=" + pos[i - 1] + "+" + pos[i - 2]
        else:
            pprev_tag = "pprev_tag=start+prev_tag=" + (pos[i - 1] if i == 1 else START)
        features_list.append(pprev_tag)

    # The feature is prev_word
    prev_word = "prev_word=" + (words[i - 1] if i > 0 else START)
    features_list.append(prev_word)

    # The feature is prev_prev_word=pprev_word
    pprev_word = "pprev_word=" + (words[i - 2] if i > 1 else START)
    features_list.append(pprev_word)

    # The feature is next_word
    next_word = "next_word=" + (words[i + 1] if i < len(words) - 1 else END)
    features_list.append(next_word)

    # The feature is next_next_word=nnext_word
    nnext_word = "nnext_word=" + (words[i + 2] if i < len(words) - 2 else END)
    features_list.append(nnext_word)

    # Find more signatures for rar words.
    if rar_word == 1:
        word_signatures(cur, features_list)

    return features_list


def word_signatures(cur, features_list):
    # The feature is 2, 3 and 4-suffix, and also 2, 3 and 4-prefix.
    if len(cur) > 2 and cur[len(cur) - 1] != '.':
        if len(cur) > 3:
            if len(cur) > 4:
                features_list.append('4_suffix''=' + cur[-4:])
                features_list.append('4_prefix''=' + cur[:4])
            features_list.append('3_suffix''=' + cur[-3:])
            features_list.append('3_prefix''=' + cur[:3])
        features_list.append('2_suffix''=' + cur[-2:])
        features_list.append('2_prefix''=' + cur[:2])
    # The feature is if the word has '-'
    if '-' in cur:
        features_list.append('contains_hyphen=true')
    # The feature is if the word has '/'
    if '/' in cur:
        features_list.append('contains_slash=true')
    # The feature is if the word has number.
    if any(x.isdigit() for x in cur):
        features_list.append('has_number=true')
    # The feature is if the whole word with upper case letters.
    if cur.isupper():
        features_list.append('is_upper=true')
    # The feature is if the word start with upper case letter.
    elif cur[0].isupper():
        features_list.append('start_upper=true')


if __name__ == "__main__":
    start()

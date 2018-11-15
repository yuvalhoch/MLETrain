import MLETrain
import GreedyTag


def main():
    print("Hey!")
    dic_e, dic_q, pos_count_dic = MLETrain.start()

    # test for the greedy tagger using the
    # print(GreedyTag.greedy_tag_word("c","A","B",dic_e,dic_q,pos_count_dic))


main()

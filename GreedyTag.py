import MLETrain

"""
given word as x, tag1 and tag2 (tags of previous words)
iterate over all possible part of speeches ("poses")
find which one is the the best tag for x, the pos with the highest probability
using formula t3 = pos which maximize: e(x|t3)*q(t3|t1,t2)
pos_count_dic is count_dic which its keys represent the possible part of speeches
"""


def greedy_tag_word(x, t1, t2, dic_e, dic_q, pos_count_dic):
    t3 = "default"
    max_t3_prob = 0
    for pos in pos_count_dic.keys():
        if pos in dic_e[x].keys():  # first check if the given word could be pos (if you've seen it before)
            e_x_given_t3 = MLETrain.get_e(x, pos, dic_e, pos_count_dic)
            q_t3_given_t1t2 = MLETrain.get_q(t1, t2, pos, dic_q)
            cur_pos_porb = e_x_given_t3 * q_t3_given_t1t2  # calc cur pos probability using e(x|t3)*q(t3|t1,t2)
            print(cur_pos_porb)
            # update t3 to hold the pos which maximize prob
            if cur_pos_porb > max_t3_prob:
                max_t3_prob = cur_pos_porb
                t3 = pos
    return t3

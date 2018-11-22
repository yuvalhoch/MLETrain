import sys
import json
import MEMMUtils


def convert_features_to_feature_vec(features_file, feature_vec_file, feature_to_feature_num_map_file):
    # create pos_to_num_dic from file
    pos_to_num_dic = MEMMUtils.create_pos_to_num_dic("pos_file")

    features_to_num_dic = {}  # features_to_num_dic[feature] = feature number.
    # exp: features_to_num_dic["pprev_word=Chicago"] = 108
    lines = features_file.readlines()
    feature_counter = 1  # counter to give each feature unique number (=count)
    for word_feature_line in lines:
        # list with all the features which are set to 1 in the line (which represent specific word)
        #  - list with all features numbers to write in feature vec line for this word
        features_set_to_on = []
        feature_list = word_feature_line.replace("\n", "").split(" ")[1:]  # holds line with all the features WITHOUT the label
        label_str = word_feature_line.split(" ")[0]  # holds the label
        # if label_str == "\n":
        #     print("problem")
        label_num = pos_to_num_dic[label_str]  # convert label as string to number for exp. NNP = 2
        for feature in feature_list:
            if feature not in features_to_num_dic.keys():
                add_to_feature_map(features_to_num_dic,feature,feature_counter)
                feature_counter += 1  # increase the counter to give next feature the next following number

            feature_num = features_to_num_dic[feature]
            features_set_to_on.append(feature_num)  # append the feature num set to on to "features_set_to_on" list

        features_set_to_on.sort() # sort the features to constant specific order (increasing/decreasing)
        # write to feature_vec_file this specific word feature line
        feature_line = str(label_num) + " " + " ".join((str(x) + ":1 ") for x in features_set_to_on) + "\n"
        feature_vec_file.write(feature_line)

    # write features_to_num_dic to "feature_to_feature_num_map" file (using json for convenience)
    with open(feature_to_feature_num_map_file, 'w') as file:
        file.write(json.dumps(features_to_num_dic))  # use `json.loads` to do the reverse


# receives map, feature and number adds the feature to map exp: map[feature] = number
def add_to_feature_map(feature_to_feature_num_map,feature, number):
    feature_to_feature_num_map[feature] = number


def main():
    if len(sys.argv) != 4:
        print ("bad parameters!")
        exit(1)

    features_file_name = sys.argv[1]
    features_vec_name = sys.argv[2]
    features_map_name = sys.argv[3]

    features_file = open(features_file_name, 'r')
    features_vec_file = open(features_vec_name, 'a')
    #pos_file = open("pos_file", 'a')

    #features_map_file = open(features_map_name, 'a')

    convert_features_to_feature_vec(features_file, features_vec_file, features_map_name)
    features_file.close()
    features_vec_file.close()


main()


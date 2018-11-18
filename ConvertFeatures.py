import sys


def start():
    features_file = open("features_file.txt")
    #features_file = open(sys.argv[1])
    feature_vecs_file = open("feature_vecs_file.txt", "a")
    #feature_vecs_file = open(sys.argv[2])
    feature_map_file = open("feature_map_file.txt", "a")
    #feature_map_file = open(sys.argv[3])
    pos_dic, features_dic, data_vecs = features_to_data_vector(features_file)
    # Write to feature_vecs_file the feature vectors, such that the first word is the label
    # number, and the rest are the features numbers : 1 (the 'on' bit).
    for vec in data_vecs:
        ########################################
        feature_vecs_file.write(
            "{} {}".format(vec[0], " ".join("{}:1".format(feature_index)
                                            for feature_index in vec[1:])) + "\n")

    for feature, index in features_dic.items():
        feature_map_file.write(feature + " " + str(index) + "\n")
    features_file.close()
    feature_vecs_file.close()
    feature_map_file.close()


def features_to_data_vector(features_file):
    features_dict = {}
    data_vecs = []
    pos_dic = {}
    # Move on the lines in the feature_file, and convert every line to a
    # vector of features by indexes.
    lines = features_file.readlines()
    for line in lines:
        vec = features_line_to_data_vector(line, pos_dic, features_dict)
        data_vecs.append(vec)
    return pos_dic, features_dict, data_vecs


def features_line_to_data_vector(features_line, pos_dic, features_dic):
    features = features_line.split(" ")
    pos = features[0]
    feature_vector = []
    # Move on the features in the line.
    for feature_str in features[1:]:
        # If the feature already in the features dictionary,
        # set the features_dic[feature_str] value to be the number of the feature
        # line in the file.
        if feature_str in features_dic.keys():
            feature_vector.append(features_dic[feature_str])
        else:
            features_dic[feature_str] = len(features_dic)
            feature_vector.append(features_dic[feature_str])
    # Sorted the feature list.
    feature_vector = list(sorted(feature_vector))
    if pos not in pos_dic.keys():
        pos_dic[pos] = len(pos_dic)
    # Add the POS to be in the head of the vector.
    feature_vector.insert(0, pos_dic[pos])
    return feature_vector


if __name__ == "__main__":
    start()

import sys
flag = True


def start():
    global flag
    feature_map_file = None
    features_file = open(sys.argv[1])
    feature_vecs_file = open(sys.argv[2], "a")
    # Try to open feature map file - to know if that is the train or the test.
    try:
        feature_map_file = open(sys.argv[3], "r")
    except:
        flag = False
    pos_dic, features_dic, data_vecs = features_to_data_vector(features_file, feature_map_file)
    # Try to write to map file if that is the train, if not - read from the train map file.
    feature_map_file = open(sys.argv[3], "a")
    if flag:
        feature_map_file.close()
        feature_map_file = open(sys.argv[3], "a")
        for feature, index in features_dic.items():
            feature_map_file.write(feature.strip("\n") + " " + str(index) + "\n")
    else:
        for feature, index in features_dic.items():
            feature_map_file.write(feature.strip("\n") + " " + str(index) + "\n")
    # Write to feature_vecs_file the feature vectors, such that the first word is the label
    # number, and the rest are the features numbers : 1 (the 'on' bit).
    for vec in data_vecs:
        feature_vecs_file.write(
            "{} {}".format(vec[0], " ".join("{}:1".format(feature_index)
                                            for feature_index in vec[1:])) + "\n")
    features_file.close()
    feature_vecs_file.close()
    feature_map_file.close()


def features_to_data_vector(features_file, feature_map_file):
    global flag
    features_dic = {}
    data_vecs = []
    pos_dic = {}
    feature_map_dic = {}
    if flag:
        lines = feature_map_file.readlines()
        for line in lines:
            feature = line.split("\n")[0].split(" ")
            feature_str = feature[0]
            if feature_str not in feature_map_dic:
                feature_map_dic[feature_str] = feature[1]
    else:
        lines = features_file.readlines()
        for line in lines:
            vec = features_line_to_data_vector(line, pos_dic, features_dic, feature_map_dic)
            data_vecs.append(vec)
    # Move on the lines in the feature_file, and convert every line to a
    # vector of features by indexes.
    lines = features_file.readlines()
    for line in lines:
        vec = features_line_to_data_vector(line, pos_dic, features_dic, feature_map_dic)
        data_vecs.append(vec)
    return pos_dic, features_dic, data_vecs


def features_line_to_data_vector(features_line, pos_dic, features_dic, feature_map_dic):
    features = features_line.split(" ")
    pos = features[0]
    feature_vector = []

    # Move on the features in the line.
    for feature_str in features:
        # If the feature already in the features dictionary,
        # set the features_dic[feature_str] value to be the number of the feature
        # line in the file.
        if flag:
            if feature_str in feature_map_dic.keys():
                if feature_str in features_dic.keys():
                    feature_vector.append(int(feature_map_dic[feature_str]))
                else:
                    features_dic[feature_str] = int(feature_map_dic[feature_str])
                    feature_vector.append(features_dic[feature_str])
        else:
            if feature_str in features_dic.keys():
                feature_vector.append(features_dic[feature_str])
            else:
                features_dic[feature_str] = len(features_dic) + 1
                feature_vector.append(features_dic[feature_str])
    # Sorted the feature list.
    feature_vector.sort()
    if pos not in pos_dic.keys():
        pos_dic[pos] = len(pos_dic) + 1
    # Add the POS to be in the head of the vector.
    feature_vector.insert(0, pos_dic[pos])
    return feature_vector


if __name__ == "__main__":
    start()

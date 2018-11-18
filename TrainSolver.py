import os
import sys
import subprocess as process

import ConvertFeatures
import ExtractFeatures


def start():
    #os.system("java -cp liblinear-2.20.jar de.bwaldvogel.liblinear.Train -s 0 -c 0.001 feature_vecs_file MODEL_FILE")
    features_vecs_file = sys.argv[1]
    os.system("java -cp liblinear-2.20.jar de.bwaldvogel.liblinear.Predict -b 1 " + features_vecs_file + " MODEL_FILE output")


if __name__ == "__main__":
    start()

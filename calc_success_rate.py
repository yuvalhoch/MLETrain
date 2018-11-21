def main():
    tagger_test_input = open("OUT")
    tagger_test = open("ass1-tagger-test") #############
    num_words = 0
    incorrect = 0 #########
    line_input = tagger_test_input.readline()
    line_test = tagger_test.readline()

    #num_lines = sum(1 for line in open('tagger_test'))
    for line_input, line_test in zip(tagger_test_input, tagger_test):

        for line_in_inp, line_in_tst in zip(line_input.split(" "), line_test.split(" ")):
            word_inp = line_in_inp.split("/")
            num_words += 1
            word_test = line_in_tst.split("/") ###############
            if word_inp[1] != word_test[1]: ############
                incorrect += 1 ############
                #print ("test: " + word_test[1] + "\toutput: " + word_inp[1] + "\n")
        #line_input = tagger_test_input.readline()
        #line_test = tagger_test.readline()

    percent = 100 - (100 * incorrect / num_words) ##############3
    print (str(percent) + "%")#################
    tagger_test.close() ###############
    tagger_test_input.close()

main()

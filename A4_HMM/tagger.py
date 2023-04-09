import os
import sys
import argparse
import numpy as np

"""
Steps:

1. Parse training and testing data into single sentences
2. Training phase:
    1. learn three probability tables described below:
        (i) The initial probabilities over the POS tags (how likely each POS tag
         appears at the beginning of a sentence)
        (ii) The transition probabilities from one POS tag to another.
        (iii) The observation probabilities from each POS tag to each observed 
        word.
    2. store these tables for quick and easy access
3. Testing phase:
    Use Viterbi algorithm to determine the most likely tag for each word in a 
    sentence
    
    Algorithm:
    1. store tag for each word
    
4. Output file:
    same format as the training files
    the POS tags in the output file are predicted by your HMM model

Things to keep in mind:
- tag that only appears in the test data never be predicted because all
probabilities involving that tag would be 0?
"""

TAGS = ["AJ0", "AJC", "AJS", "AT0", "AV0", "AVP", "AVQ", "CJC", "CJS", "CJT",
        "CRD",
        "DPS", "DT0", "DTQ", "EX0", "ITJ", "NN0", "NN1", "NN2", "NP0", "ORD",
        "PNI",
        "PNP", "PNQ", "PNX", "POS", "PRF", "PRP", "PUL", "PUN", "PUQ", "PUR",
        "TO0",
        "UNC", 'VBB', 'VBD', 'VBG', 'VBI', 'VBN', 'VBZ', 'VDB', 'VDD', 'VDG',
        'VDI',
        'VDN', 'VDZ', 'VHB', 'VHD', 'VHG', 'VHI', 'VHN', 'VHZ', 'VM0', 'VVB',
        'VVD',
        'VVG', 'VVI', 'VVN', 'VVZ', 'XX0', 'ZZ0', 'AJ0-AV0', 'AJ0-VVN',
        'AJ0-VVD',
        'AJ0-NN1', 'AJ0-VVG', 'AVP-PRP', 'AVQ-CJS', 'CJS-PRP', 'CJT-DT0',
        'CRD-PNI', 'NN1-NP0', 'NN1-VVB',
        'NN1-VVG', 'NN2-VVZ', 'VVD-VVN', 'AV0-AJ0', 'VVN-AJ0', 'VVD-AJ0',
        'NN1-AJ0', 'VVG-AJ0', 'PRP-AVP',
        'CJS-AVQ', 'PRP-CJS', 'DT0-CJT', 'PNI-CRD', 'NP0-NN1', 'VVB-NN1',
        'VVG-NN1', 'VVZ-NN2', 'VVN-VVD']

# Algorithm:
# 1. Read training line - store word-tag, strip and split with delimeter ":"
# 2. Convert the words into a sentence and store??
# 3. Update initial prob - NPO tag
# 4. Calculate transition prob
# 5. Calculate observation probabilities - # of times NPO tag/ total # of
# sentences in file

WORD_TAG = {}
INIT_PROB = {}
TAG_DICT = {}
TRANS_TAG = {}
TRANS_PROB = {}
OBSV_PROB = {}
OBSERVED = []


def read_from_file(file_list):
    for file in file_list:
        inputfile = open(file, 'r')
        prev_tag = None
        for line in inputfile:
            # read first line and store it in input_prob and then prev var
            # in next iteration, update the transition matrix and prev word
            line = line.strip()
            # we have word and tag
            # track tag count and word-tag count
            word, tag = line.split(" : ")
            key = word + ' ' + tag
            WORD_TAG[key] = WORD_TAG.get(key, 0) + 1
            TAG_DICT[tag] = TAG_DICT.get(tag, 0) + 1
            if prev_tag is None:
                prev_tag = tag
            else:
                # have already seen 1 word-tag
                # can calculate the transition prob by storing the prev tag
                # with curr tag
                updateTransTag(prev_tag, tag, TRANS_TAG)
                prev_tag = tag
    # need to calculate the probabilities - initial, transition and observation


def updateTransTag(prev_tag, tag, trans_tag_dict):
    """
    Updates a dictionary of transition tags where the the key is made up of both
     tags and the value is the number of times both tag occur simultaneously
     in the training files.
    """
    trans_tag = prev_tag + " " + tag
    if trans_tag in trans_tag_dict:
        trans_tag_dict[trans_tag] += 1
    else:
        trans_tag_dict[trans_tag] = 1


def calculateInitProb(word_tag_dict, init_prob):
    """
    Calculates the initial probability of each each word-tag pair by dividing
    the number of occurences of the pair over the total number of occurences of
    all the tags, i.e, total number of sentences.
    """
    total = sum(TAG_DICT.values())
    for word_tag in word_tag_dict:
        init_prob[word_tag] = word_tag_dict[word_tag] / total


def calculateTransProb(trans_tag_dict, trans_prob):
    """
    Calculates the transition probability of each tag pair by dividing the
    number of occurences of the pair over the number of occurences of tag 1
    """
    for trans_tag in trans_tag_dict:
        lst = trans_tag.split()
        tag1, tag2 = lst[0], lst[1]
        trans_prob[trans_tag] = trans_tag_dict[trans_tag] / TAG_DICT[tag1]


def calculateObsProb(word_tag_dict, obsv_prob):
    """
    Calculates the observation probability from each tag to each observed word
    """
    for word_tag in word_tag_dict:
        lst = word_tag.split()
        word, tag = lst[0], lst[1]
        obsv_prob[word_tag] = word_tag_dict[word_tag] / TAG_DICT[tag]


def read_test_file(filename):
    file = open(filename, 'r')
    for line in file:
        words = line.strip()
        word_list = words.split()
        OBSERVED.extend(word_list)


def viterbi(e, s, init_prob, trans_prob, obs_prob):
    """
    Viterbi algorithm following pseudocode.

    Inputs:
    e: set of observations over time steps -> e is the ith word in the sentence
    s: set of hidden state values
    init_prob: initial probilities
    trans_mat: transition matrix
    obs_mat: observation matrix

    Pseudocode:
    # need to figure out matrix formation
    prob = np.empty((len(e), len(s)))
    prev = np.empty((len(e), len(s)))

    # determine values for time step 0
    for i in range(0, len(s) - 1):
        prob[0, i] = init_mat[i] * obs_mat[i, e(0)]
        prev[0, i] = None

    # for time steps 1 to length(E) - 1
    # find each current state's most likely prior state x
    for t in range(1, len(e) - 1):
        # looping through tags
        for i in range(0, len(s) - 1):
            # j is over all hidden state values for t-1
            # x = np.argmax(prob[t - 1, j] * trans_mat[j, i] * obs_mat[i, e(t)])
            x = np.argmax(init_mat[t-1] * trans_mat[:, i] * obs_mat[i,e[t]])
            prob[t, i] = init_mat[t - 1, x] * trans_mat[x, i] * obs_mat[i, e(t)]
            prev[t, i] = x
    return prob, prev

    trying without matrix:
    """
    prob = {}
    prev = {}

    init_word = e[0]
    # determine max value for time step 0
    path = []
    max_prob = 0
    max_state = None
    for tag in s:
        word_tag = init_word + " " + tag
        if word_tag in init_prob and word_tag in obs_prob and init_prob[
            word_tag] * obs_prob[word_tag] > max_prob:
            max_prob = init_prob[word_tag] * obs_prob[word_tag]
            max_state = tag
    # possibility of not finding max state
    if max_state is None:
        i = np.random.randint(0, len(s))
        max_state = s[i]
    path.append((init_word, max_state))
    # for time steps 1 to length(E) - 1
    # find each current state's most likely prior state x
    for obs_word in e[1:]:
        # looping through tags
        prob_of_obs_word = []
        for i in range(len(s)):
            # j is over all hidden state values for t-1
            # we keep updating the max prob each time
            # in the end we get the max prob over all hidden states
            # so we can avoid the j loop
            prev_tag = path[-1][1] + " " + s[i]
            word_tag = obs_word + " " + s[i]
            ip, op, pt = 0, 0, 0  # handles case of tag not seen
            if word_tag in init_prob:
                ip = init_prob[word_tag]
            if word_tag in obs_prob:
                op = obs_prob[word_tag]
            if prev_tag in trans_prob:
                pt = trans_prob[prev_tag]
            prob = ip * op * pt
            prob_of_obs_word.append(prob)
        # now calculate max prob to find most likely word-tag pair
        max_prob = max(prob_of_obs_word)
        # find max state by taking index of max_prob and using this on tag_list
        max_state = s[prob_of_obs_word.index(max_prob)]
        path.append((obs_word, max_state))
    return path


def write_to_file(outputfile, path):
    # things to consider:
    # if test file has blank line, output file should have blank line too?
    # path is a list of tuples - (word, tag)
    file = open(outputfile, 'w')
    for word_tag in path:
        word, tag = word_tag
        str = word + " : " + tag + '\n'
        file.write(str)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trainingfiles",
        action="append",
        nargs="+",
        required=True,
        help="The training files."
    )
    parser.add_argument(
        "--testfile",
        type=str,
        required=True,
        help="One test file."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file."
    )
    args = parser.parse_args()

    training_list = args.trainingfiles[0]
    print("training files are {}".format(training_list))

    print("test file is {}".format(args.testfile))

    print("output file is {}".format(args.outputfile))

    read_from_file(training_list)
    calculateInitProb(WORD_TAG, INIT_PROB)
    calculateTransProb(TRANS_TAG, TRANS_PROB)
    calculateObsProb(WORD_TAG, OBSV_PROB)
    read_test_file(args.testfile)
    path = viterbi(OBSERVED, TAGS, INIT_PROB, TRANS_PROB, OBSV_PROB)
    #write_to_file(outputfile, path)
    write_to_file(args.outputfile, path)

    print("Starting the tagging process.")

from collections import Counter
import cPickle as pickle
import random
import itertools

def ply_markov(entry, ply, current_dict):
    words = [word.lower().decode('ascii', 'ignore') for word in entry.split()]
    for i in xrange(0, len(words)-ply):
        current_tuple = tuple([words[j] for j in xrange(i, i+ply)])
        if current_dict.get(current_tuple, False):
            current_dict[current_tuple].update([words[i+ply]])
        else:
            current_dict[current_tuple] = Counter([words[i+ply]])
    return current_dict

def train(input_file, output_file, ply):
    master_dict = {i: {} for i in xrange(1,ply+1)}
    with open(input_file, "rb") as source:
        for line in source:
            for key, value in master_dict.iteritems():
                master_dict[key] = ply_markov(line, key, value)
    pickle.dump(master_dict, open(output_file, 'wb'))

def get_check_tuple(current_output, ply):
    last_n_list = [current_output[-i] for i in xrange(1,ply+1)]
    last_n_list.reverse()
    return tuple(last_n_list)

def append_next_word(master_dict, current_output, ply):
    ply = min(len(current_output), ply)
    ply_list = []
    for i in xrange(1, ply+1):
        check = master_dict[i].get(get_check_tuple(current_output, i),{})
        ply_list.extend([[key]*value*i for key, value in check.iteritems()])
    master_list = list(itertools.chain(*ply_list))
    current_output.append(random.choice(master_list))

def generate(input_file, output_length, ply):
    master_dict = pickle.load(open(input_file, 'rb'))
    output = []
    output.append(random.choice(master_dict[1].keys())[0])
    check_tuple = get_check_tuple(output, 1)
    for i in xrange(output_length):
        append_next_word(master_dict, output, ply)
    return " ".join(output)

#train("allData.txt", "markov.p", 2)
#print generate("markov.p", 200, 3)
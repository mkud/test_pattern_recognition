'''
Created on 29 oct 2019

@author: us170
'''

import re
from _functools import reduce
import logging
import sys
# logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# list of values to analyze
input_array = [ "A--1012332/1",
  "A--1231142/2",
  "A--1231142/1",
  "A--a1233442/2",
  "S--1231142/11"
 ]

# 20% errors allowed
available_level_error = 0.2

# track 3 groups of characters: letters, digits, others
regex_int_mask_relations = [ {"regex": "[a-zA-Z]", "int": "l"},
           {"regex": "\d", "int": "d"},
           {"regex": "[^a-zA-Z\d]", "int": "o"}]

# first stage - map all symbols in input data to internal mask presentation
def first_stage_map_to_internal_mask(fv):
    return list(map(lambda z0:  # iterate for all input list
            reduce(lambda x1, y1: x1 + y1,  # Simply convert map object to string
                 map(
                    lambda y2:  # search first element from 'regex_int_mask_relations' which regex match
                        next(filter(lambda z3: re.match(z3["regex"], y2), regex_int_mask_relations), {"int":"o"})["int"],
                     z0)
            ), fv
        ))


# stage 2 - group internal mask presentation by removing duplicate symbols (loodddddddod->lodod)
# this masks we will use for searching errors in the input data
def second_stage_int_mask_to_short_mask(fv):
    return list(map(lambda y2: reduce(lambda x, y: x if x[-1] == y else (x + y), y2), fv))

# the same plus count duplicate symbols (loodddddddod->lo{2}d{7}od)
def second_stage_2_int_mask_to_mask_with_groupby(fv):

    def temp_inc_last_cnt(in_array):
        in_array[-1]['cnt'] += 1
        return in_array

    return list(map(
                    lambda y2: 
                        reduce(lambda x, y: x + [{'symbol': y, 'cnt': 1}] if len(x) == 0 or x[-1]["symbol"] != y else temp_inc_last_cnt(x), y2, [])
                    , fv)
                )

# stage 3 - calc the popularity of all short masks to find the most popular. 
# other masks are considered erroneous
def third_stage_calc_short_mask_popularity(in_masks):
    ret = {}
    for cur_mask in in_masks:
        ret[cur_mask] = ret.get(cur_mask, 0) + 1
    return ret

# finds the mutual part in all strings of the set (at the beginning of strings). Cuts it off.
def search_mutual_in_begin(in_set):
    first_val = list(in_set)[0]
    for i in range(1, len(first_val)):
        if [x for x in in_set if x[:i] != first_val[:i]]:
            return first_val[:i - 1], set(map(lambda x: x[i - 1:], in_set))
    return None, in_set

# finds the mutual part in all strings of the set (at the tail of strings). Cuts it off.
def search_mutual_in_end(in_set):
    first_val = list(in_set)[0]
    for i in range(1, len(first_val)):
        if len([x for x in in_set if x[-i:] != first_val[-i:]]):
            return (None, in_set) if i == 1 else (first_val[-i + 1:], set(map(lambda x: x[:-i + 1], in_set)))
    return None, in_set

def main(inp):
    # first stage - map all symbols in input data to internal mask presentation
    first_stage_result = first_stage_map_to_internal_mask(inp)
    logging.debug("first_stage_result: " + str(first_stage_result))
    second_stage_short_mask = second_stage_int_mask_to_short_mask(first_stage_result)
    second_stage_mask_with_groupby = second_stage_2_int_mask_to_mask_with_groupby(first_stage_result)
    
    # stage 2 - group internal mask presentation by removing duplicate symbols (loodddddddod->lodod)
    # plus count duplicate symbols (loodddddddod->lo{2}d{7}od)
    logging.debug("-"*20)
    logging.debug("second stage:")
    logging.debug("short masks: " + str(second_stage_short_mask))
    logging.debug("masks with group by: " + str(second_stage_mask_with_groupby))

    # stage 3 - calc the popularity of all short masks to find the most popular.
    # output erroneous data
    logging.debug("-"*20)
    logging.debug("third stage:")
    short_masks_popularity = third_stage_calc_short_mask_popularity(second_stage_short_mask)
    max_popular_short_mask = max(short_masks_popularity, key=short_masks_popularity.get)
    logging.debug("current validity level - {}".format(float(short_masks_popularity[max_popular_short_mask]) / len(inp)))
    if float(short_masks_popularity[max_popular_short_mask]) / len(inp) < (1 - available_level_error):
        #TODO: this case can also be considered
        # later
        print("All is bad. Need more deep learning. Cannot find max popular short mask. Current level error - {:.3g}; target level error - {:.3g}".format(1.0 - (float(short_masks_popularity[max_popular_short_mask]) / len(inp)), available_level_error))
        return
    else:
        logging.debug("max popular short mask is: " + max_popular_short_mask)
        wrong_vals = []
        i = 0
        for cur_short_mask in second_stage_short_mask:
            if cur_short_mask != max_popular_short_mask:
                wrong_vals.append(inp[i])
            i += 1
        if len(wrong_vals):
            print("wrong vals are: " + ",".join(wrong_vals))

    # stage 4 - get all the groups of all input array. remove duplicates by set()
    # max_popular_short_mask - the main seq
    logging.debug("-"*20)
    logging.debug("fourth stage:")
    fourth_stage_result = [set() for _ in range(len(max_popular_short_mask))]
    for i in range(len(second_stage_short_mask)):
        if second_stage_short_mask[i] != max_popular_short_mask:
            continue
        current_input_value = inp[i]
        for j in range(len(max_popular_short_mask)):
            fourth_stage_result[j].add(current_input_value[:second_stage_mask_with_groupby[i][j]["cnt"]])
            current_input_value = current_input_value[second_stage_mask_with_groupby[i][j]["cnt"]:]
    logging.debug("result: " + str(fourth_stage_result))
    
    #stage 5 - analyze each group to find a mutual beginning or end
    # if found - move it to a separate group
    # this will make it possible to specify the format more accurately
    logging.debug("-"*20)
    logging.debug("fifth stage:")
    fifth_stage_result = []
    for cur_set_val in fourth_stage_result:
        if len(cur_set_val) == 1 or max([len(x) for x in cur_set_val]) == 1:
            fifth_stage_result.append(cur_set_val)
        else:
            mutual_begin_val, middle = search_mutual_in_begin(cur_set_val)
            if mutual_begin_val:
                fifth_stage_result.append(set(mutual_begin_val))
            mutual_end_val, middle = search_mutual_in_end(middle)
            fifth_stage_result.append(middle)
            if mutual_end_val:
                fifth_stage_result.append(set(mutual_end_val))
    logging.debug("result: " + str(fifth_stage_result))
    
    # collect from the resulting groups an array for the formation of regex
    # available cases: 
    # * specific value, 
    # * any char from set, 
    # * string of one type (from "regex_int_mask_relations") with len range
    logging.debug("-"*20)
    logging.debug("sixth stage:")
    finish_result = []
    for cur_set_val in fifth_stage_result:
        list_of_length = [len(x) for x in cur_set_val]
        if len(cur_set_val) == 1:
            finish_result.append(list(cur_set_val)[0])
        elif max(list_of_length) == min(list_of_length):
            if max(list_of_length) == 1:
                finish_result.append("[{}]".format(reduce(lambda x, y: x + y, cur_set_val)))
            else:
                finish_result.append("{}{{{}}}".format(next(filter(lambda z3: re.match(z3["regex"], list(cur_set_val)[0][0]), regex_int_mask_relations))["regex"], max(list_of_length)))
        else:
            finish_result.append("{}{{{},{}}}".format(next(filter(lambda z3: re.match(z3["regex"], list(cur_set_val)[0][0]), regex_int_mask_relations))["regex"], min(list_of_length), max(list_of_length)))
    logging.debug(finish_result)
    print("result: " + "^" + "".join(finish_result) + "$")
    
if __name__ == '__main__':
    main(input_array)

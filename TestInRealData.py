import os
import CompareSimilarity
import numpy as np
import matplotlib.pyplot as plt
import ast
import extract
import itertools
import threading
import time
import sys

done = False


def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)


def test_in_real_data(type_sum, question_index, average_vector, path, iwf=False, subtract_average=False, ss=True):
    """

    :param type_sum: The dimension of the selected characteristic vector, there are 9 and 35 two types
    :param question_index: Select the index of question that needs to be compared
                           That is, the index of the editable cells in the jupyter notebook
    :param average_vector:The average value of the feature vector of the selected question in the data set
    :param path:Path to store student jupyter notebook assignments
    :param idf: whether use the IWF post-processing method
    :param subtract_average: whether use the average subtraction post-processing method
    :param ss: whether standardization
    :return: a dictionary containing all comparison results
    """
    files = os.listdir(path)
    length = len(files)
    dict = {}
    for i in range(length):
        for j in range(i + 1, length):
            file_1 = os.path.join(path, files[i])
            file_2 = os.path.join(path, files[j])

            if not os.path.isdir(file_1) and not os.path.isdir(file_1):
                c = CompareSimilarity.Compare(file_1, file_2, question_index, type_sum=type_sum, path=path)
                sim_res = c.cosine_distance(iwf=iwf, subtract_average=subtract_average, ss=ss,
                                            average_vector=average_vector)
                dict[str(files[i]) + " vs " + str(files[j])] = sim_res
    return dict


# It may take a while
def check_the_distribution(type_sum, question_index, average_vector, path,
                           iwf=False, subtract_average=False, ss=True):
    result = test_in_real_data(type_sum, question_index, average_vector, path,
                               iwf, subtract_average, ss)

    val = np.array(list(result.values()))
    val_bz = val[val != None] * 100
    plt.figure(figsize=(18, 10))
    grid = plt.GridSpec(2, 4, wspace=6, hspace=0.5)
    graph = plt.subplot(grid[0:2, 0:4])
    plt.hist(val_bz, bins=100, facecolor="white", edgecolor="black")
    plt.ylabel("Frequency")
    plt.xlabel("Similarity (%)")
    graph.spines['top'].set_visible(False)
    graph.spines['right'].set_visible(False)
    graph.spines['left'].set_visible(False)
    plt.show()
    return result


def get_name_list(node):
    name_list = []
    for sub_node in ast.walk(node):
        if isinstance(sub_node, ast.Name):
            name_list.append(sub_node.id)
    return name_list


def jaccard_index(node_1, node_2):
    name_list_1 = get_name_list(node_1)
    name_list_2 = get_name_list(node_2)
    length = 0
    for value in name_list_1:
        if value in name_list_2:
            length += 1
    ji = length / (len(name_list_1) + len(name_list_2) - length)
    return ji


def suspected_pairs(res_dict, copy_and_paste=True):
    for k, v in res_dict.items():
        if v == 1:
            if not copy_and_paste:
                print(v)
            k_list = k.split(" vs ")
            code_1 = extract.get_source_without_tests(path_files + "/" + k_list[0], 3)
            code_2 = extract.get_source_without_tests(path_files + "/" + k_list[1], 3)
            node_1 = ast.parse(code_1)
            node_2 = ast.parse(code_2)
            ji = jaccard_index(node_1, node_2)
            if ji == 1 and copy_and_paste:
                print(k)


if __name__ == "__main__":
    t = threading.Thread(target=animate)
    t.start()
    path_files = "C:/Users/82569/PycharmProjects/dstion/data/Assignment 7/Root/last"
    average_vector_9 = CompareSimilarity.get_average_vector(9, 3, path=path_files, first_child=False)
    average_vector_35 = CompareSimilarity.get_average_vector(35, 3, path=path_files, first_child=False)
    res = check_the_distribution(35, 3, average_vector_35, path_files, idf=True, subtract_average=True, ss=True)
    done = True
    suspected_pairs(res, copy_and_paste=True)
import ast
import numpy as np
from sklearn.preprocessing import StandardScaler
import extract
import SumVector
import AverageVector
import NodesTypes

"""
Compare the similarity of two code fragments
"""


def get_average_vector(type_sum=9, question_index=3, first_child=False,
                       path="data/Assignment 7/Root/last"):
    av = AverageVector.CalucalateAverageVector(type_sum, question_index)
    average_vector = av.subtract_average(path, first_child)

    # print("{} {}".format("vector after subtract_average:\n", vector_after_subtract))
    return average_vector


class Compare(ast.NodeTransformer):
    def __init__(self, juypter_file_1, juypter_file_2, question_index=3, type_sum=9, path=" "):

        self.type_sum = type_sum

        self.path = path

        self.question_index = question_index

        self.nodes_type = NodesTypes.return_nodes_array(type_sum)

        self.code_1 = extract.get_source_without_tests(juypter_file_1, question_index)
        self.code_2 = extract.get_source_without_tests(juypter_file_2, question_index)
        try:
            self.node_1 = ast.parse(self.code_1)
            self.node_2 = ast.parse(self.code_2)
        except Exception:
            pass

        if type_sum == 35:
            sum_vector = np.array(
                [80641, 21977, 8191, 10157, 1476, 242303, 265217, 60918, 27235,
                 6242, 6242, 53105, 12643, 9745, 17359, 14198, 2935, 2938,
                 69784, 11081, 47510, 17974, 17639, 2325, 1948, 508, 47034,
                 1575, 2297, 5480, 837, 7262, 7262, 15368, 7630])
            self.weight_coefficient = np.log(sum(sum_vector) / sum_vector)

        elif type_sum == 9:
            sum_vector = np.array([1.26295e+05, 6.02591e+05, 2.94868e+05, 4.30670e+04, 5.44000e+02, 5.00970e+04,
                                   1.57500e+03, 9.34200e+03, 4.13970e+04])
            self.weight_coefficient = np.log(sum(sum_vector) / sum_vector)

    def generic_visit(self, node):
        """
        :param node:
        :return: node with a new field "vector"
        """
        # add fields to python objects
        node.vector = np.zeros(self.type_sum)
        ast.NodeTransformer.generic_visit(self, node)
        for general_type_index, one_general_type in enumerate(self.nodes_type):
            if (type(one_general_type)).__name__ == "list":
                if type(node) in one_general_type:
                    node.vector[general_type_index] += 1
            else:
                if type(node) == one_general_type:
                    node.vector[general_type_index] += 1
        for a in ast.iter_child_nodes(node):
            # this node will be sum of all children nodes
            # as well as case logic below.
            node.vector += a.vector
        return node

    def get_name_list(self, node):
        name_list = []
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Name):
                name_list.append(sub_node.id)
        return name_list

    def jaccard_distance(self):
        name_list_1 = self.get_name_list(self.node_1)
        name_list_2 = self.get_name_list(self.node_2)
        length = 0
        for value in name_list_1:
            if value in name_list_2:
                length += 1
        ji = (len(name_list_1) + len(name_list_2) - 2 * length) / (len(name_list_1) + len(name_list_2) - length)
        return ji

    @staticmethod
    def is_same_num_child(node_1, node_2):
        """Whether it has a common number of child nodes"""
        num_1 = 0
        num_2 = 0

        for ele in ast.iter_child_nodes(node_1):
            num_1 += 1
        for ele in ast.iter_child_nodes(node_2):
            num_2 += 1

        if num_1 == num_2:
            return True
        else:
            return False

    def child_sim_compare(self):
        """compare the simlarity of first child node """
        pass

    def term_frequency_inverse_document_frequency(self, vector):
        # print(self.sum_vector)
        vector_after_idf = vector * self.weight_coefficient / sum(vector)
        return vector_after_idf

    @staticmethod
    def standard_scaler(vector):
        scaler = StandardScaler()
        transformed_vector = vector.reshape(-1, 1)
        scaler.fit(transformed_vector)
        vector_after_ss = np.ravel(scaler.transform(transformed_vector))
        # print("{} {}".format("vector after standard_scaler:\n", vector_after_ss))
        return vector_after_ss

    def l2_norm(self, vector):
        l2 = np.sqrt(sum(vector ** 2))
        vector_after_l2 = vector / l2
        return vector_after_l2

    def cosine_distance(self, subtract_average=False, iwf=False, ss=False, average_vector=None):
        if average_vector is None:
            average_vector = []
        try:
            vector_1 = self.generic_visit(self.node_1).vector
            vector_2 = self.generic_visit(self.node_2).vector
        except Exception:
            return
        if vector_1.sum() < 15 or vector_2.sum() < 15:
            return

        assert len(vector_1) == len(vector_2)
        zero_list = np.zeros(len(vector_1))
        if (vector_1 == zero_list).all() or (vector_2 == zero_list).all():
            return float(1) if (vector_1 == vector_2).all() else float(0)

        x = vector_1
        y = vector_2

        if subtract_average:
            x -= average_vector
            y -= average_vector

        if iwf:
            x = self.term_frequency_inverse_document_frequency(x)
            y = self.term_frequency_inverse_document_frequency(y)

        if ss:
            x = self.standard_scaler(x)
            y = self.standard_scaler(y)

        res = np.array(
            [[x[i] * y[i],
              x[i] * x[i],
              y[i] * y[i]]
             for i in range(len(x))])

        cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))

        return 0.5 * cos + 0.5


if __name__ == "__main__":
    path_original = "f9a7d1_original.ipynb"
    path_1 = "f9a7d1_Primary Plagiarism_1.ipynb"
    path_2 = "f9a7d1_Intermediate plagiarism_1.ipynb"
    path_3 = "f9a7d1_Advanced plagiarism_1.ipynb"
    path_files = "data/Assignment 7/Root/last"

    c_1 = Compare(path_original, path_1, 3, type_sum=9, path=path_files)
    average_vector = get_average_vector(9, 3, path=path_files, first_child=True)
    print(c_1.cosine_distance(iwf=False, ss=False, subtract_average=True, average_vector=average_vector))

import ast
import numpy as np
from sklearn.preprocessing import StandardScaler
import extract
import SumVector
import AverageVector
import NodesTypes


def sum_vector(type_sum):
    sv = SumVector.CalculateAllVector(type_sum)
    return sv.return_vector_sum()


def avg_vector(type_sum, question_index, path):
    av = AverageVector.CalucalateAverageVector(type_sum, question_index)
    return av.subtract_average(path)


class Compare(ast.NodeTransformer):
    def __init__(self, juypter_file_1, juypter_file_2, question_index=3, type_sum=9, path=" "):

        self.type_sum = type_sum
        self.question_index = question_index

        self.nodes_type = NodesTypes.return_nodes_array(type_sum)

        self.code_1 = extract.get_source_without_tests(juypter_file_1, question_index)
        self.code_2 = extract.get_source_without_tests(juypter_file_2, question_index)

        self.node_1 = ast.parse(self.code_1)
        self.node_2 = ast.parse(self.code_2)

        self.vector_1 = self.generic_visit(self.node_1).vector
        self.vector_2 = self.generic_visit(self.node_2).vector

        if type_sum == 35:
            self.sum_vector = np.array(
                [80641, 21977, 8191, 10157, 1476, 242303, 265217, 60918, 27235,
                 6242, 6242, 53105, 12643, 9745, 17359, 14198, 2935, 2938,
                 69784, 11081, 47510, 17974, 17639, 2325, 1948, 508, 47034,
                 1575, 2297, 5480, 837, 7262, 7262, 15368, 7630])
        elif type_sum == 9:
            self.sum_vector = np.array([1.26295e+05, 6.02591e+05, 2.94868e+05, 4.30670e+04, 5.44000e+02, 5.00970e+04,
                                        1.57500e+03, 9.34200e+03, 4.13970e+04])

        if path != " ":
            av = AverageVector.CalucalateAverageVector(type_sum, question_index)
            self.average_vector = av.subtract_average(path_2)

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

    @staticmethod
    def standard_scaler(vector):
        scaler = StandardScaler()
        transformed_vector = vector.reshape(-1, 1)
        scaler.fit(transformed_vector)
        vector_after_ss = np.ravel(scaler.transform(transformed_vector))
        # print("{} {}".format("vector after standard_scaler:\n", vector_after_ss))
        return vector_after_ss

    def inverse_document_frequency(self, vector):

        vector_after_idf = vector / self.sum_vector
        # print("{} {}".format("vector after idf:\n", vector_after_idf))
        return vector_after_idf

    def subtract_average(self, vector):
        vector_after_subtract = vector - self.average_vector
        # print("{} {}".format("vector after subtract_average:\n", vector_after_subtract))
        return vector_after_subtract

    def euclidean_distance(self, idf=False, ss=False, subtract_average=False):
        pass

    def cosine_distance(self, idf=False, ss=False, subtract_average=False):
        assert len(self.vector_1) == len(self.vector_2)
        zero_list = np.zeros(len(self.vector_1))
        if (self.vector_1 == zero_list).all() or (self.vector_2 == zero_list).all():
            return float(1) if (self.vector_1 == self.vector_2).all() else float(0)

        x = self.vector_1
        y = self.vector_2

        if idf:
            x = self.inverse_document_frequency(self.vector_1)
            y = self.inverse_document_frequency(self.vector_2)

        if subtract_average:
            x = self.subtract_average(x)
            y = self.subtract_average(y)

        if ss:
            x = self.standard_scaler(x)
            y = self.standard_scaler(y)

        res = np.array(
            [[x[i] * y[i],
              x[i] * x[i],
              y[i] * y[i]]
             for i in range(len(x))])

        cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))

        if -1 <= cos <= 0:
            return 0.5 * cos + 0.5
        else:
            return cos

    def edit_tree_distance(self):
        pass

    def visit_name(self, node):
        pass

    def visit_str(self, node):
        pass


if __name__ == "__main__":
    path_original = "C:/Users/82569/Desktop/f9a7d1_original.ipynb"
    path_1 = "C:/Users/82569/Desktop/f9a7d1_Primary Plagiarism_1.ipynb"
    path_2 = "C:/Users/82569/Desktop/f9a7d1_Intermediate plagiarism_1.ipynb"
    path_3 = "C:/Users/82569/Desktop/f9a7d1_Advanced plagiarism_1.ipynb"
    path_files = "C:/Users/82569/PycharmProjects/dstion/data/Assignment 7/Root/last"

    c_1 = Compare(path_original, path_1, 3, type_sum=9, path=path_files)
    print(c_1.cosine_distance(idf=False, ss=False, subtract_average=False))

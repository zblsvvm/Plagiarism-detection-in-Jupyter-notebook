import ast
import numpy as np
import os
import extract
import NodesTypes


class CalucalateAverageVector(ast.NodeTransformer):
    def __init__(self, nodes_type_num, question_index):
        self.nodes_type = NodesTypes.return_nodes_array(nodes_type_num)
        self.length = len(self.nodes_type)
        self.question_index = question_index

    def generic_visit(self, node):
        """
        :param node:
        :return: node with a new field "vector"
        """
        # add fields to python objects

        node.vector = np.zeros(self.length)
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

    def subtract_average(self, path):
        files = os.listdir(path)
        sum_vector = np.zeros(self.length)
        num = 0
        for file in files:
            i = os.path.join(path, file)
            if not os.path.isdir(i):
                num += 1
                a_student_code = extract.get_source_without_tests(path + "/" + file, self.question_index)
                try:
                    a_student_node = ast.parse(a_student_code)
                except Exception:
                    pass
                a_student_vector = self.generic_visit(a_student_node).vector
                sum_vector += a_student_vector
        average_vector = sum_vector / num
        return average_vector

if __name__ == "__main__":
    path = "C:/Users/82569/PycharmProjects/dstion/data/Assignment 7/Root/last"
    Cal = CalucalateAverageVector(35, 3)
    print(Cal.subtract_average(path))

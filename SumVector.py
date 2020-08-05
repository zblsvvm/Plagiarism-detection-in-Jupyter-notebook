import ast
import numpy as np
import nbformat
import os
import extract
import NodesTypes


class CalculateAllVector(ast.NodeTransformer):
    def __init__(self, type_sum):
        self.type_sum = type_sum

        if type_sum == 9:
            self.nodes_type = NodesTypes.return_nodes_array(97)
        if type_sum == 35:
            self.nodes_type = NodesTypes.return_nodes_array(56)

        self.sum_vector = np.zeros(len(self.nodes_type))

    def generic_visit(self, node):
        # you are allowed to add arbitrary fields to python objects
        node.vector = np.zeros(len(self.nodes_type))
        ast.NodeTransformer.generic_visit(self, node)
        if type(node) != ast.Module:
            index = self.nodes_type.index(type(node))
            node.vector[index] += 1
        for a in ast.iter_child_nodes(node):
            # this node will be sum of all children nodes
            # as well as case logic below.
            node.vector += a.vector
        # print("{} {} {}".format("node.vector:", type(node).__name__, node.vector))
        return node

    def get_source_without_tests(self, filename):
        try:
            nb = nbformat.read(filename, 4)
        except Exception as e:
            print("{}{}{}".format("read_problem ", filename, e))
        single_file_vector = np.zeros(len(self.nodes_type))
        try:
            for c in nb.cells:
                if c['cell_type'] == 'code':
                    if 'nbgrader' in c['metadata'].keys():
                        if not c['metadata'].get('editable', True):
                            if c['metadata']['nbgrader'].get('locked', False):
                                # this is a test cell, remove
                                continue

                    # print(c)
                    if extract.sanitize(c['source']).strip() != "":
                        try:
                            node = ast.parse(extract.sanitize(c['source']))
                            single_question_vector = self.generic_visit(node).vector
                            single_file_vector += single_question_vector
                        except SyntaxError as e:
                            print("{}{}{}".format("SyntaxError ", filename, e))
                        except ValueError:
                            pass


        except UnboundLocalError as e:
            print("{}{}{}".format("UnboundLocalError ", filename, e))
        return single_file_vector

        return single_file_vector

    def traversing_dataset(self, path):
        files = os.listdir(path)
        for file in files:
            i = os.path.join(path, file)
            if os.path.isdir(i):
                self.traversing_dataset(i)
            if not os.path.isdir(i):
                self.sum_vector += self.get_source_without_tests(i)
        return self.sum_vector

    def view_value(self):
        result = self.sum_vector
        sort_index = np.argsort(-result)
        index = 0
        for i in sort_index:
            index += 1
            print("{}   {}   {}".format(index, str(self.nodes_type[i]), result[i]))

    def return_vector_sum(self):

        nodes_type = NodesTypes.return_nodes_array(self.type_sum)

        if nodes_type is None:
            return None

        result = self.sum_vector[:]
        #print(sum(result))
        nodes_sum_vector = np.array([])
        current_len = 0

        for i in nodes_type:
            if (type(i)).__name__ == "list":
                length = len(i)
            else:
                length = 1
            sum_value = sum(result[current_len:current_len + length])
            nodes_sum_vector = np.append(nodes_sum_vector, sum_value)
            current_len += length
        return nodes_sum_vector


if __name__ == "__main__":
    path3 = "data"
    k = CalculateAllVector(9)
    result = k.traversing_dataset(path3)
    print(result)
    a = k.return_vector_sum()
    print(a)

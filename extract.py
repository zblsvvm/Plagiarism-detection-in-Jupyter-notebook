import nbformat
import os
import numpy as np


def is_extra(line):
    stripped = line.strip()
    if stripped and (stripped[0] == '#' or stripped[0] == '%' or stripped[0:6] == "import"):
        return True
    return False


def sanitize(txt):
    lines = txt.split('\n')
    ok_lines = [i for i in lines if not is_extra(i)]
    return '\n'.join(ok_lines)


def get_source_without_tests(filename, question_num):
    nb = nbformat.read(filename, 4)
    single_students_all_question = {}
    index = 1
    for c in nb.cells:
        if c['cell_type'] == 'code':
            if 'nbgrader' in c['metadata'].keys():
                if not c['metadata'].get('editable', True):
                    if c['metadata']['nbgrader'].get('locked', False):
                        # this is a test cell, remove
                        continue

            # print(c)
            if sanitize(c['source']).strip() != "":
                if index <= question_num:
                    single_students_all_question["question" + str(index)] = sanitize(c['source'])
                    index += 1
    return single_students_all_question


def exact_every_students_code(path, question_num):
    files = os.listdir(path)
    every_student_code = {}
    for file in files:
        i = os.path.join(path, file)
        if not os.path.isdir(i):
            a_student_code = get_source_without_tests(path + "/" + file, question_num)
            if __name__ == "__main__":
                print(a_student_code)
            every_student_code[
                path.split('/')[2] + " " + path.split('/')[3] + " " + file.split('.')[0]] = a_student_code
    return every_student_code


if __name__ == "__main__":
    path = "testdata/Assignment 1/Assignment 1/last"
    print(exact_every_students_code(path, 4))

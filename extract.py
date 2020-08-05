import nbformat
import os



def is_extra(line):
    """
    Determine whether the scanned juyter notebook line contains the following content:
    1. Start with "#" (comment)
    2. Start with "@" (eg %matplotlib inline)
    3. start with "import"
    """
    stripped = line.strip()
    if stripped and (stripped[0] == '#' or stripped[0] == '%' or stripped[0:6] == "import"):
        return True
    return False


def sanitize(txt):
    """
    remove lines which has extra code
    """
    lines = txt.split('\n')
    ok_lines = [i for i in lines if not is_extra(i)]
    return '\n'.join(ok_lines)


def get_source_without_tests(filename, question_index):
    """
    :param filename:
    :param question_index: select the index of question that needs to be compared
    :return: dictionary containing one single student's codes in one single assignment
    """

    nb = nbformat.read(filename, 4)

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
                if index == question_index:
                    students_code = sanitize(c['source'])
                index += 1
    return students_code


def exact_every_students_code(path, question_num):
    """
    :param filename:
    :param question_num: the total number of question
    :return: a dictionary containing all student's codes in one single assignment
    """
    files = os.listdir(path)
    every_student_code = {}
    for file in files:
        i = os.path.join(path, file)
        if not os.path.isdir(i):
            a_student_code = get_source_without_tests(path + "/" + file, question_num)
            every_student_code[
                path.split('/')[2] + " " + path.split('/')[3] + " " + file.split('.')[0]] = a_student_code
    return every_student_code


if __name__ == "__main__":
    path = "testdata/Assignment 1/Assignment 1/last"
    for i in exact_every_students_code(path, 4)['Assignment 1 last 01bb4a']:
        print(exact_every_students_code(path, 4)['Assignment 1 last 01bb4a'][i])



def computeGpas(file_name):
    """
    Reads the contents of file_name, combines the grades for each student, and outputs a formatted line for each student with their GPA
    """

    input_lines = read_file(file_name)




def read_file(file_name):
    """
    Opens a given file, reads all the text, splits on newlines, and closes the file.
    """

    file = open(file_name, mode='r')
    file_text = file.read()

    file.close()

    file_lines = file_text.split('\n')

    return file_lines

class Student:

    def __init__(self, first_name, last_name, grades):
        self.first_name = first_name
        self.last_name = last_name
        self.grades = grades
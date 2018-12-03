def computeGpas(file_name):
    """
    Reads the contents of file_name, 
    combines the grades for each student, 
    and outputs all formatted student's grades in sorted order.
    """

    # list of lines from the given file
    input_lines = read_file(file_name)

    # The list of lines that have been separated and formatted successfully
    # Does not include lines with errors.
    input_courses = []

    # The list of errors that occurred while formatting lines.
    # Saved to print at end of program.
    error_lines = []

    # the current line nubmber of lines being read
    line_num = 1

    for line in input_lines:
        
        # The first value of the tuple is a true or false value indicating
        # conversion success.
        # The second value of the tuple is the tuple of values
        # converted from the given line.
        return_tuple = convert_to_grade(line)
        
        # empty line found
        if return_tuple == None:
            line_num += 1
            continue
        
        (convert_result, convert_rtn) = return_tuple

        # If convert was successful, add the converted line to the set of valid courses.
        # If convert was unsuccessful, format the error and add it to the error list.
        if convert_result:
            input_courses.append(convert_rtn)
        else:
            for error in convert_rtn:
                convert_error = "Error with line " + str(line_num) + ": " + error
                error_lines.append(convert_error)

        line_num += 1

    # A dictionary hashed by student names
    student_dict = {}

    for course_line in input_courses:

        (department, course_num, section, num_credits, first_name, last_name, grade) = course_line

        student_key = first_name + "_" + last_name

        this_course = Course(department, course_num, section, num_credits, grade)

        try:
            # Try to locate the student key and add the course.
            student_dict[student_key].add_course(this_course)
        except:
            # If the key doesn't exist, create a new student and add to the student table.
            new_student = Student(first_name, last_name)
            new_student.add_course(this_course)
            student_dict[student_key] = new_student

    # Print a formatted list of the students
    print_students(student_dict)

    # Print errors if any occurred.
    if (len(error_lines) > 0):
        print("\nErrors:")
        for error in error_lines:
            print(error)


def read_file(file_name):
    """
    Opens a given file, reads all the text, splits on newlines, and closes the file.
    """

    file = open(file_name, mode='r')
    file_text = file.read()

    file.close()

    file_lines = file_text.split('\n')

    return file_lines

def convert_to_grade(input_string):
    """
    Converts the given string to a class grade for a student.
    Checks if the given list is a valid grade line.
    Returns a tuple of conversion success, and converted tuple or error.
    Returns None if line is empty.
    """

    errors = []

    # Empty line found so return nothing.
    if input_string == '':
        return None

    # Split the list by its spaces.
    split_line = input_string.split(' ')

    # Check that the list is a valid length.
    if len(split_line) != 7: 
        errors.append("Invalid number of items on the line!")
        return (False, errors)

    (department, course_num, section, num_credits, first_name, last_name, grade) = tuple(split_line)

    # Check the department id is valid.
    for char in department:
        if (not char.isalpha()) or (not char.isupper()):
            errors.append("Invalid department ID!")
            break

    # Check valid course id by attempting to convert to int and checking that it has 3 digits.
    try:
        if (len(course_num) != 3):
            errors.append("Invalid course number! Course number must be 3 digits!")
        course_num = int(course_num)
    except:
        errors.append("Invalid course number! Must be integer!")

    # Check course section is a single alpha value.
    if (not len(section) == 1) or (not section.isalpha()) or (not section.isupper()):
        errors.append("Invalid class section!")

    # Check that the number of credits is a valid non-negative.
    try:
        num_credits = int(num_credits)
        # Check that the number of credits is non-negative.
        if num_credits < 0:
            errors.append("Number of credits must be non-negative!")
    except:
        errors.append("Invalid entry for number of credits!")

    # Check that the last name is an alpha string.
    for char in last_name:
        if not char.isalpha():
            errors.append("Invalid last name!")
            break

    # Check that the first name is an alpha string.
    for char in first_name:
        if not char.isalpha():
            errors.append("Invalid first name!")
            break

    grade_letters = {
        "A+": 4.0,
        "A": 4.0,
        "A-": 3.67,
        "B+": 3.33,
        "B": 3.0,
        "B-": 2.67,
        "C+": 2.33,
        "C": 2.0,
        "C-": 1.67,
        "D+": 1.33,
        "D": 1.0,
        "D-": 0.67,
        "F": 0.0
    }

    # Try to get the float for the grade letter if it exists in the dictionary.
    grade = grade_letters.get(grade)

    # If grade letter doesn't exist, add an error to the error list.
    if grade == None:
        errors.append("Invalid grade letter!")

    # If no errors, then conversion was successful.
    if (len(errors) > 0):
        return (False, errors)
    else:
        return (True, (department, course_num, section, num_credits, first_name, last_name, grade))

def print_students(student_dict):
    """
    Formats and prints students, GPAs, and number of credits in sorted order
    by GPA, last_name, and first_name.
    """

    # The length of the longest student name.
    max_student_name_length = 0

    # A list of the students.
    student_list = []

    # Determine the length of the longest student name.
    for student_name in student_dict:
        if len(student_name) - 1 > max_student_name_length:
            max_student_name_length = len(student_name) - 1
        student_list.append(student_dict[student_name])

    # Sort the students by their gpa, last name, and first name.
    student_list.sort(key= lambda student: (-student.get_gpa(), student.last_name, student.first_name))

    # Format the titles for each column.
    name_title = "NAME" + (" " * (max_student_name_length))
    gpa_title = " GPA" + ("  ")
    credits_title = " CREDITS"

    print(name_title + gpa_title + credits_title)

    # Format the row for each student.
    for student in student_list:

        # Format the student's name.
        student_formatted_name = student.first_name + ", " + student.last_name
        student_formatted_name += (" " * ((max_student_name_length + 4) - len(student_formatted_name)))
        
        # Format the student's gpa.
        student_formatted_gpa = str(student.get_gpa())
        student_formatted_gpa += (" " * (5 - len(student_formatted_gpa)))

        # Format the student's credits.
        student_formatted_credits = str(student.get_number_credits())
        student_formatted_credits += (" " * (7 - len(student_formatted_credits)))

        print(student_formatted_name, student_formatted_gpa, student_formatted_credits)

class Student:
    """
    Class for a student, can add courses and get gpa
    """

    def __init__(self, first_name, last_name):
        """
        Constructor for a new Student.
        """

        self.first_name = first_name
        self.last_name = last_name
        self.courses = []

    def add_course(self, course):
        """
        Adds the given course to the student's course list.
        """
        
        self.courses.append(course)

    def get_gpa(self):
        """
        Calculates the student's gpa using the list of their courses.
        """

        gpa_count = 0

        for course in self.courses:
            gpa_count += (course.num_credits * course.grade_value)

        number_credits = self.get_number_credits()

        # No gpa because student is taking only 0 credit classes.
        # Take average of the GPAs instead.
        if number_credits == 0:
            gpa_count = 0
            course_count = 0
            for course in self.courses:
                gpa_count += course.grade_value
                course_count += 1
            return (round(gpa_count/course_count, 2))
        
        final_gpa = gpa_count / number_credits

        return round(final_gpa, 2)

    def get_number_credits(self):
        """
        Returns the number of credits the student is taking.
        """

        total_credits = 0

        for course in self.courses:
            total_credits += course.num_credits
        
        return total_credits

class Course:
    """
    Class containing a course's department, section, and number of credits.
    """

    def __init__(self, department, course_num, section, num_credits, grade_value):
        """
        Constructor for a new Course.
        """

        self.department = department
        self.course_num = course_num
        self.section = section
        self.num_credits = num_credits
        self.grade_value = grade_value
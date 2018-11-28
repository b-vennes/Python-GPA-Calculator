import computeGpas as cg

def test_file_input():
    test_file = "test1.input"

    file_lines = cg.read_file(test_file)

    assert file_lines[0] == "CS 273 A 1 John Smith F"

    assert file_lines[-1] == "THE 105 A3 John Smith D+"
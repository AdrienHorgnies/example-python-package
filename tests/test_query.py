import query
import tempfile


def test_str_from_file():
    with tempfile.TemporaryFile(mode='w') as file:
        file.write("-- A comment followed by a blank line\n"
                   "\n"
                   "SELECT 'this is a test' -- inline comment\n"
                   "WHERE 1;\n"
                   "\n")
        assert query.str_from_file(file.name) == "SELECT 'this is a test' WHERE 1;"

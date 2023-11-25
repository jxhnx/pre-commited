assert "\\" not in "{{ cookiecutter.author_name }}", "Don't include backslashes in author name."

code_formatter_print_width = "{{ cookiecutter.code_formatter_print_width }}"
assert (
    code_formatter_print_width.isdigit() and float(code_formatter_print_width).is_integer()
), "Invalid value for code_formatter_print_width. Please provide an integer value."

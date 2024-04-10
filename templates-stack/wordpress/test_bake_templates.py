from pathlib import Path

import pytest

from tests.common import generate_cookiecutter_template

template_dir = Path(__file__).resolve().parent


@pytest.mark.default
def test_default():
    git_init = {"git_init": "true"}
    lint_non_default_print_width = {"code_formatter_print_width": "30", "git_init": "true"}
    no_print_width_limit = {"code_formatter_print_width": "0"}
    relaxed_rulset = {"wordpress_coding_standards": "relaxed"}
    generate_cookiecutter_template(template_dir, git_init)
    generate_cookiecutter_template(template_dir, lint_non_default_print_width)
    generate_cookiecutter_template(template_dir, no_print_width_limit)
    generate_cookiecutter_template(template_dir, relaxed_rulset)

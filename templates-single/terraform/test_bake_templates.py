from pathlib import Path

import pytest

from tests.common import generate_cookiecutter_template

template_dir = Path(__file__).resolve().parent


@pytest.mark.default
def test_default():
    git_init = {"git_init": "true"}
    lint_non_default_print_width = {"code_formatter_print_width": "30", "git_init": "true"}
    generate_cookiecutter_template(template_dir, git_init)
    generate_cookiecutter_template(template_dir, lint_non_default_print_width)

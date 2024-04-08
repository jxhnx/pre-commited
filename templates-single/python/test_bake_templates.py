from pathlib import Path

import pytest

from tests.common import generate_cookiecutter_template

template_dir = Path(__file__).resolve().parent


@pytest.mark.default
def test_default():
    git_init = {"git_init": "true"}
    generate_cookiecutter_template(template_dir, git_init)


@pytest.mark.default
def test_python_env_file_choices():
    use_venv = {"python_env": "venv", "create_python_env": "false"}
    use_conda = {"python_env": "conda", "create_python_env": "false"}
    generate_cookiecutter_template(template_dir, use_venv)
    generate_cookiecutter_template(template_dir, use_conda)


@pytest.mark.system
def test_python_env_setup():
    use_venv = {"python_env": "venv", "create_python_env": "true"}
    use_conda = {"python_env": "conda", "create_python_env": "true"}
    use_mamba = {"python_env": "mamba", "create_python_env": "true"}
    generate_cookiecutter_template(template_dir, use_conda)
    generate_cookiecutter_template(template_dir, use_venv)
    generate_cookiecutter_template(template_dir, use_mamba)

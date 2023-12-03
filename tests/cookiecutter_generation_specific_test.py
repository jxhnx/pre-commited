# All test which use not the default values
import pytest

from .cookiecutter_generation_test import generate_template as generate_specific_template


@pytest.mark.default
def test_default_template():
    git_init = {"git_init": "true"}
    generate_specific_template("default_template", git_init)


@pytest.mark.default
def test_python_env_files():
    PATH = "templates-single/python"
    use_venv = {"python_env": "venv", "create_python_env": "false"}
    use_conda = {"python_env": "conda", "create_python_env": "false"}
    generate_specific_template(PATH, use_venv)
    generate_specific_template(PATH, use_conda)

    PATH = "templates-single/python_datascience"
    use_venv = {"python_env": "venv", "create_python_env": "false"}
    use_conda = {"python_env": "conda", "create_python_env": "false"}
    generate_specific_template(PATH, use_venv)
    generate_specific_template(PATH, use_conda)


@pytest.mark.python_env
def test_python_template_envs():
    PATH = "templates-single/python"
    use_venv = {"python_env": "venv", "create_python_env": "true"}
    use_conda = {"python_env": "conda", "create_python_env": "true"}
    use_mamba = {"python_env": "mamba", "create_python_env": "true"}

    generate_specific_template(PATH, use_venv)
    generate_specific_template(PATH, use_conda)
    generate_specific_template(PATH, use_mamba)


@pytest.mark.python_env
def test_python_datascience_template_envs():
    PATH = "templates-single/python_datascience"
    use_venv = {"python_env": "venv", "create_python_env": "true"}
    use_conda = {"python_env": "conda", "create_python_env": "true"}
    use_mamba = {"python_env": "mamba", "create_python_env": "true"}

    generate_specific_template(PATH, use_venv)
    generate_specific_template(PATH, use_conda)
    generate_specific_template(PATH, use_mamba)

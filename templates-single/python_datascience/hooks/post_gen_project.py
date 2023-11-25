import os
import shutil
import subprocess
from pathlib import Path
from textwrap import dedent

import requests

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "


def yes(value):
    return str(value).lower() not in ["n", "0", "false", "f", "no", "off"]


def remove_open_source_files():
    file_names = ["LICENSE"]
    for file_name in file_names:
        os.remove(file_name)


def remove_gplv3_files():
    file_names = ["COPYING"]
    for file_name in file_names:
        os.remove(file_name)


def remove_dotgitlabciyaml_file():
    os.remove(".gitlab-ci.yaml")


def remove_dotgithub_folder():
    shutil.rmtree(".github")


def remove_environmentdotyaml_file():
    os.remove("environment.yaml")


def remove_requirementsdottxt_file():
    os.remove("requirements.txt")


def remove_gitkeeps():
    for file_path in Path.cwd().rglob("*.gitkeep"):
        file_path.unlink()


def generate_gitignore():
    print(INFO + "Fetching recent .gitignore rules..." + TERMINATOR)

    rules = ["dotenv", "windows", "macos", "linux", "python"]
    url = "https://www.toptal.com/developers/gitignore/api/" + ",".join(rules)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(WARNING + f"Error: {e}, using cached .gitignore" + TERMINATOR)
        return None

    custom_header = f"""######################################################
# Custom / project-specific .gitignore
######################################################

# Data
data/*





######################################################
# Generated .gitignore for {", ".join(rules)}
######################################################
"""

    combined_gitignore = custom_header + "\n" + response.text

    with open(".gitignore", "w") as gitignore_file:
        gitignore_file.write(combined_gitignore)


def create_virtual_environment(package_manager: str):
    print(INFO + "Creating Python environment..." + TERMINATOR)

    if package_manager == "venv":
        subprocess.run(["python", "-m", "venv", "env"])

        if os.name == "posix":  # Unix-like systems
            subprocess.run(
                ["sh", "-c", "source env/bin/activate && pip install --upgrade pip"], check=True
            )
            subprocess.run(
                ["sh", "-c", "source env/bin/activate && pip install -r requirements.txt"],
                check=True,
            )
            subprocess.run(
                ["sh", "-c", "source env/bin/activate && pre-commit install"], check=True
            )
        elif os.name == "nt":  # Windows
            subprocess.run(
                [".\\env\\Scripts\\python.exe", "-m", "pip", "install", "--upgrade", "pip"],
                check=True,
            )
            subprocess.run(
                [".\\env\\Scripts\\python.exe", "-m", "pip", "install", "-r", "requirements.txt"],
                check=True,
            )
            subprocess.run([".\\env\\Scripts\\activate"], shell=True, check=True)
            subprocess.run(
                [".\\env\\Scripts\\python.exe", "-m", "pre_commit", "install"], check=True
            )

    elif package_manager in ["conda", "mamba"]:
        prefix = "conda" if package_manager == "conda" else "mamba"
        environment_name = "{{ cookiecutter.repo_name }}"

        env_list = subprocess.run(
            [prefix, "env", "list"], capture_output=True, text=True, check=True
        )
        environments = env_list.stdout.splitlines()

        create = True
        if any(environment_name in env for env in environments):
            print(
                WARNING
                + f'Python environment not created. The conda/mamba environment "{environment_name}" seems to exist.'
                + TERMINATOR
            )
            user_input = input("Do you want to delete the old environment? (y/n): ")
            if user_input.lower() == "y":
                try:
                    subprocess.run([prefix, "env", "remove", "-n", f"{environment_name}"])
                except subprocess.CalledProcessError as e:
                    print(WARNING + f"Error: {e}" + TERMINATOR)
                    return None
            else:
                create = False

        if create:
            subprocess.run([prefix, "env", "create", "-f", "environment.yaml"])
            print(SUCCESS + "Virtual environment created!" + TERMINATOR)


def main():
    PYTHON_ENV = "{{ cookiecutter.python_env | default('None') }}"

    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_open_source_files()

    if "{{ cookiecutter.open_source_license}}" != "GPLv3":
        remove_gplv3_files()

    if "{{ cookiecutter.ci_tool }}" != "Gitlab":
        remove_dotgitlabciyaml_file()

    if "{{ cookiecutter.ci_tool }}" != "Github":
        remove_dotgithub_folder()

    if PYTHON_ENV == "venv":
        remove_environmentdotyaml_file()
        if yes("{{ cookiecutter.create_python_env }}"):
            create_virtual_environment("venv")

    if PYTHON_ENV == "conda":
        remove_requirementsdottxt_file()
        if yes("{{ cookiecutter.create_python_env }}"):
            create_virtual_environment("conda")

    if PYTHON_ENV == "mamba":
        remove_requirementsdottxt_file()
        if yes("{{ cookiecutter.create_python_env }}"):
            create_virtual_environment("mamba")

    if PYTHON_ENV == "None":
        remove_requirementsdottxt_file()
        remove_environmentdotyaml_file()

    generate_gitignore()
    remove_gitkeeps()

    if yes("{{ cookiecutter.git_init | default('false') }}"):
        print(INFO + "Initializing git repository..." + TERMINATOR)

        subprocess.call(["git", "init", "-b", "main"])
        subprocess.call(["git", "add", "*"])
        subprocess.call(["git", "commit", "-m", "Initial commit"])

    msg_vars = dict(
        activate_os_venv="source env/bin/activate"
        if os.name == "posix"
        else "env\\Scripts\\Activate",
    )

    msg_template = dedent(
        """
        Change directory into your newly created project:
            $ cd {{ cookiecutter.repo_name }}

        {% if cookiecutter.python_env == 'venv' -%}
        To activate the Python environment, run:
            $ %(activate_os_venv)s

        To deactivate the Python environment, run:
            $ deactivate
        {% endif -%}
        {% if cookiecutter.python_env == 'conda' or cookiecutter.python_env == 'mamba' -%}
        To activate the {{ cookiecutter.python_env }} environment, run:
            $ {{ cookiecutter.python_env }} activate {{ cookiecutter.repo_name }}

        To deactivate the {{ cookiecutter.python_env }} environment, run:
            $ {{ cookiecutter.python_env }} deactivate
        {% endif -%}
        """
    )
    msg = msg_template % msg_vars

    print(SUCCESS + "The cookie is cut!" + TERMINATOR)
    print(msg)


if __name__ == "__main__":
    main()

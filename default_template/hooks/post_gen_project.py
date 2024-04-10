import os
import shutil
import subprocess

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


def remove_dotgitlabciyml_file():
    os.remove(".gitlab-ci.yml")


def remove_bitbucketpipelinesyml_file():
    os.remove("bitbucket-pipelines.yml")


def remove_dotgithub_folder():
    shutil.rmtree(".github")


def generate_gitignore():
    print(INFO + "Fetching recent .gitignore rules..." + TERMINATOR)

    rules = ["dotenv", "windows", "macos", "linux"]
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







######################################################
# Generated .gitignore for {", ".join(rules)}
######################################################
"""

    combined_gitignore = custom_header + "\n" + response.text

    with open(".gitignore", "w") as gitignore_file:
        gitignore_file.write(combined_gitignore)


def run_pre_commit_subprocess():
    print(INFO + "Run pre-commit..." + TERMINATOR)
    subprocess.call(["git", "init", "-b", "main"])
    subprocess.call(["git", "add", "*"])
    subprocess.call(["pre-commit", "run", "--all-files"])
    subprocess.call(["rm", "-rf", ".git"])


def run_initial_git_commit_subprocess():
    print(INFO + "Initializing git repository..." + TERMINATOR)
    subprocess.call(["git", "init", "-b", "main"])
    subprocess.call(["git", "add", "*"])
    subprocess.call(["git", "commit", "-m", "Initial commit"])


def main():
    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_open_source_files()

    if "{{ cookiecutter.open_source_license }}" != "GPLv3":
        remove_gplv3_files()

    if "{{ cookiecutter.ci_tool }}" != "Gitlab":
        remove_dotgitlabciyml_file()

    if "{{ cookiecutter.ci_tool }}" != "Github":
        remove_dotgithub_folder()

    if "{{ cookiecutter.ci_tool }}" != "Bitbucket":
        remove_bitbucketpipelinesyml_file()

    generate_gitignore()

    if (
        "{{ cookiecutter.code_formatter_print_width }}"
        != "{{ cookiecutter.__default_code_formatter_print_width }}"
    ):
        run_pre_commit_subprocess()

    if yes("{{ cookiecutter.git_init | default('false') }}"):
        run_initial_git_commit_subprocess()

    print(SUCCESS + "The cookie is cut!" + TERMINATOR)


if __name__ == "__main__":
    main()

import json
import os
import shutil

COOKIEJSON_PATH = "cookiecutter.json"


def remove_cookiecutterjson_key(key: str):
    with open(COOKIEJSON_PATH, "r") as file:
        cookiecutter_dict = json.load(file)

    if key in cookiecutter_dict:
        del cookiecutter_dict[key]

    with open(COOKIEJSON_PATH, "w") as file:
        json.dump(cookiecutter_dict, file, indent=2)


def remove_cookiecutterjson_options(key: str, options: list[str]):
    with open(COOKIEJSON_PATH, "r") as file:
        cookiecutter_dict = json.load(file)

    for option in options:
        cookiecutter_dict[key].remove(option)

    with open(COOKIEJSON_PATH, "w") as file:
        json.dump(cookiecutter_dict, file, indent=2)


def add_cookiecutterjson_context():
    with open(COOKIEJSON_PATH, "r") as file:
        cookiecutter_dict = json.load(file)

    cookiecutter_dict["__os_name"] = f"{os.name}"

    with open(COOKIEJSON_PATH, "w") as file:
        json.dump(cookiecutter_dict, file, indent=2)


def main():
    if shutil.which("git") is None:
        remove_cookiecutterjson_key("git_init")

    remove_env_options = []
    if shutil.which("python") is None:
        remove_env_options.append("venv")
    if shutil.which("conda") is None:
        remove_env_options.append("conda")
    if shutil.which("mamba") is None:
        remove_env_options.append("mamba")

    remove_cookiecutterjson_options("python_env", remove_env_options)

    if len(remove_env_options) == 3:
        # No env option available
        remove_cookiecutterjson_key("python_env")
        remove_cookiecutterjson_key("create_python_env")

    add_cookiecutterjson_context()


if __name__ == "__main__":
    main()

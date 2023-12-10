import json
import shutil

COOKIEJSON_PATH = "cookiecutter.json"


def remove_cookiecutterjson_key(key: str):
    with open(COOKIEJSON_PATH, "r") as file:
        cookiecutter_dict = json.load(file)

    if key in cookiecutter_dict:
        del cookiecutter_dict[key]

    with open(COOKIEJSON_PATH, "w") as file:
        json.dump(cookiecutter_dict, file, indent=2)


def main():
    if shutil.which("git") is None:
        remove_cookiecutterjson_key("git_init")


if __name__ == "__main__":
    main()

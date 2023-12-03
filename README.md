# pre-committed

Collection of dev environment setups with basic pre-commit/linting configs. Contains advanced options such as:

- OS recognition and compatibility (Mac, Linux, Windows)
- Language specific .gitignore creation with API call to [gitignore.io](https://www.toptal.com/developers/gitignore)
- Python environment creation for venv, conda, mamba
- Git init

Install [cookiecutter](https://github.com/cookiecutter/cookiecutter) in your Python environment or with your package manager of choice, e.g., with `pip install cookiecutter` or `brew install cookiecutter`.

# Usage

Run, choose your template, and follow the instructions with:

```
cookiecutter https://github.com/jxhnx/pre-committed
```

The templates are usually build so that options like `git init` or environment creation with, e.g., `venv` or `conda` are only available if they are found on your system.

# Prerequisites

This repo and its templates make use of [pre-commit](https://pre-commit.com/). Check your installation with `pre-commit -V`. You can install pre-commit in you Python environment of choice, e.g. with `pip install pre-commit` or globally with your favorite package manager, e.g. with `brew install pre-commit`.

# Development

To create a new template, you can use the `default_template` directory as starting point. Copy it to `templates-single/` or `templates-stack/`, and adjust the files to your needs. Finally, register your template in the root [cookiecutter.json](./cookiecutter.json) file. You can find more information about cookiecutter in its [docs](https://cookiecutter.readthedocs.io/). Some template file types or files may have to be added (ignored) in the .prettierignore or excluded in the .pre-commit-config.yaml.

Templates are divided into two categories: single and stack. Single templates are for a single language, e.g. Python. Stack templates are for a combination of languages and frameworks, e.g. Python and Django. Furthermore, more specialized, use-case specific templates are denoted with `_usecase1`, `_usecase2`, etc.

```
├── templates-single/
│   ├── python/
│   ├── python_usecase1/
│   ├── python_usecase2/
│   ├── javascript/
│   └── ...
└── templates-stack/
    ├── python-django/
    ├── python-django_usecase1/
    └── ...
```

## Testing

Tests are written with `pytest`. Since some tests will create Python environments, it is a good idea to run them in a Docker container. To run the tests, `cd` into `tests` and run, e.g.,:

```
docker compose up test-default
```

The default test-set includes template creation with default values and a pre-commit linting check on the created repos. They use `@pytest.mark.default` and are also run in GitHub's CI.

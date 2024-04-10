# pre-committed

Collection of dev environment setups with basic pre-commit/linting configs. Contains advanced options such as:

- Language specific .gitignore creation with [gitignore.io](https://www.toptal.com/developers/gitignore)
- Python environment creation for venv, conda, mamba
- Git init

## Baked ...

`Python · PythonDatascience · Terraform · Wordpress`

# Usage

Install [cookiecutter](https://github.com/cookiecutter/cookiecutter) in your Python environment or with your package manager of choice, e.g., with `pip install cookiecutter` or `brew install cookiecutter`.

Run, choose your template, and follow the instructions with:

```
cookiecutter https://github.com/jxhnx/pre-committed
```

Available options such as `git init` and Python env creation with `venv`, `conda`, and `mamba` depend on what is found/available on your system, i.e., in your shell.

# Prerequisites

This repo and its templates make use of [pre-commit](https://pre-commit.com/). Check your installation with `pre-commit -V`. You can install pre-commit in you Python environment of choice, e.g. with `pip install pre-commit` or globally with your favorite package manager, e.g. with `brew install pre-commit`.

Make sure to run `pre-commit install` once in your repo to activate pre-commit.

# Development

To create a new template, you can use the `default_template` directory as starting point. Copy it to `templates-single/` or `templates-stack/`, and adjust the files to your needs. Finally, register your template in the root [cookiecutter.json](./cookiecutter.json) file. You can find more information about cookiecutter in its [docs](https://cookiecutter.readthedocs.io/).

Templates are divided into two categories: single and stack. Single templates are for a single language, e.g. Python. Stack templates are for a combination of languages and frameworks, e.g. Python and Django. Furthermore, more specialized, use-case specific templates are denoted with `_usecase1`, `_usecase2`, etc.

```
├── templates-single/
│   ├── python/
│   ├── python_datascience/
│   └── ...
└── templates-stack/
    ├── python-django-angular/
    ├── python-django-angular_usecase1/
    └── ...
```

## Testing

Tests are written with `pytest`. To run tests locally, use `python -m pytest default_template tests` and replace `default_template` with the template you want to test. Tests just using cookiecutter are marked with `@pytest.mark.default`, tests using additional system requirements and installs are marked with `@pytest.mark.system`.

The Github CI uses pytest in the same way and runs tests for all templates changes are detected in. This is the recommended approach since it installs template dependencies in a system independent container environment. Use [act](https://github.com/nektos/act) to run Github workflows locally, e.g., with `act -W .github/workflows/generate-templates.yaml --container-architecture linux/amd64` (you may have to remove/adjust the --container-architecture).

## Tags

- Major: Breaking changes
- Minor: New template or feature in multiple templates
- Service: Feature or fix in single template

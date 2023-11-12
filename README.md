# pre-committed

Collection of some dev environment setups with pre-commit configs.

# Usage

# Template structure

Templates are divided into two categories: single and stack. Single templates are for a single language, e.g. Python. Stack templates are for a combination of languages and frameworks, e.g. Python and Django. Furthermore, more specialized usage specific templates are denoted with `_usecase1`, `_usecase2`, etc.

- 📁 templates-single
  - 📁 python
  - 📁 python_usecase1
  - 📁 python_usecase2
  - 📁 ...
- 📁 templates-stack
  - 📁 python-djnago
  - 📁 python-django_usecase1
  - 📁 ...


# Prerequisites

You require an installation of [pre-commit](https://pre-commit.com/). Check your installation with `pre-commit -V`. You can install pre-commit in you Python environment of choice, e.g. with `pip install pre-commit` or globally with your favorite package manager, e.g. with `brew install pre-commit`.

{% set create_python_env = cookiecutter.create_python_env | default('n') -%}
{% set python_env = cookiecutter.python_env | default('None') -%}

# My Python Project

Awesome project description.

{% if create_python_env | string | lower not in ["n", "0", "false", "f", "no", "off"] -%}

## Usage instructions:

{% if python_env == 'venv' -%}
To activate the Python environment, run:

{% if cookiecutter.__os_name == 'nt' -%}
`env\Scripts\Activate`

{% elif cookiecutter.__os_name == 'posix' -%}
`source env/bin/activate`

{% endif -%}
To deactivate the Python environment, run:

`deactivate`

{% endif -%}
{% if python_env == 'conda' or python_env == 'mamba' -%}
To activate the {{ cookiecutter.python_env }} environment, run:

`{{ python_env }} activate {{ cookiecutter.repo_name }}`

To deactivate the {{ python_env }} environment, run:

`{{ python_env }} deactivate`

{% endif -%}
{% endif -%}
{% if cookiecutter.open_source_license != "Not open source" -%}

## License

License: {{cookiecutter.open_source_license}}
{% endif -%}

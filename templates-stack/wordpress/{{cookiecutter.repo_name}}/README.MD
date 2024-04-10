# {{cookiecutter.project_name}}

{{ cookiecutter.description }}

{%- if cookiecutter.open_source_license != "Not open source" %}

License: {{cookiecutter.open_source_license}}
{%- endif %}

## Local development

-   Run `cp .env.local .env` and adjust the variables for the live website (FTP) and database
-   Export data & DBs from the live website
    -   You can use the `get-data.sh` script to download & move data and db dumps accordingly. The wordpress installation is shared through the `./wordpress` directory.
    -   Replace `my-theme` in the .gitignore file with your actual theme directory name.
-   Make sure that the wp-config.php in different deployments contain the right database credentials. For local deployment, you can just use the `local-deployment.sh`. For live websites e.g., staging, adjust them once manually.
-   Make sure that the `local-init.sql` replaces the base URL correctly (e.g., port, http vs https).
-   Run `docker compose up` to start the containers
-   Use `docker compose down -v` to also discard the volumes

## Environment

-   Install pre-commit in you python/conda/mamba environment
    -   e.g., with `conda install pre-commit`
-   Use `pre-commit install` to install the pre-commit hooks
-   For linting, additional plugins are used. Install, e.g., with:

    -   `npm install @wordpress/prettier-config @wordpress/eslint-plugin --save-dev`
    -   `brew install composer` && `composer update`, which installs composer.json dependencies like phpcodesniffer with [Wordpress rulesets](https://github.com/WordPress/WordPress-Coding-Standards#composer-project-based-installation)

-   Use `pre-commit run --all-files` to run the pre-commit hooks on all files or `pre-commit run --files <files>` to run them on specific files.

import hashlib
import json
import subprocess
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter
from jinja2 import Template

TEST_OUTPUT_DIR = Path("test_output")


@pytest.fixture(scope="module")
def template_dirs():
    return get_templates()


def test_cookiecutter_json_exists(template_dirs):
    for template_dir in template_dirs:
        assert (
            template_dir / "cookiecutter.json"
        ).exists(), f"cookiecutter.json does not exist in {template_dir}"


def test_generate_templates(template_dirs):
    for template_dir in template_dirs:
        generate_template(template_dir)


@pytest.mark.order(-1)
def test_linting_generated_templates():
    generated_template_dirs = [
        template_dir for template_dir in Path("test_output").glob("*/*") if template_dir.is_dir()
    ]

    for template_dir in generated_template_dirs:
        pre_commit_config = template_dir / ".pre-commit-config.yaml"
        if pre_commit_config.exists():
            with subprocess.Popen(["bash"], stdin=subprocess.PIPE, cwd=template_dir) as proc:
                proc.stdin.write(b"rm -rf .git/\n")
                proc.stdin.write(b"git init -b main\n")
                proc.stdin.write(b"pre-commit install --config .pre-commit-config.yaml\n")

                if (template_dir / ".gitignore").exists():
                    # API-generated .gitignore fails trailing-whitespace hook and is re-formatted
                    # This should not fail the test
                    proc.stdin.write(b"git add .gitignore\n")
                    proc.stdin.write(b"pre-commit run --files .gitignore\n")

                proc.stdin.write(b"git add .\n")
                proc.stdin.write(b"pre-commit run --all-files\n")
                proc.stdin.close()
                proc.wait()
                assert proc.returncode == 0, f"Linting failed for {template_dir}"


def get_templates() -> list[Path]:
    with open("cookiecutter.json") as f:
        data = json.load(f)

    templates = data["template"]
    template_dirs = []

    for template in templates:
        template_path = template.split("(")[-1].split(")")[0]
        template_dirs.append(Path(template_path))

    return template_dirs


def generate_template(template_dir: Path or str, custom_values: dict = None):
    """Generate a template with cookiecutter and check if the project directory was created"""

    template_dir = Path(template_dir) if isinstance(template_dir, str) else template_dir
    custom_values_str = json.dumps(custom_values, sort_keys=True) + str(template_dir)
    custom_values_hash = (
        ("_" + hashlib.sha256(custom_values_str.encode()).hexdigest()[:8])
        if custom_values is not None
        else ""
    )
    output_dir = TEST_OUTPUT_DIR / template_dir.name

    with open(template_dir / "cookiecutter.json") as f:
        data = json.load(f)

    repo_name_template = Template(data.get("repo_name"))
    repo_name = f"{repo_name_template.render(cookiecutter=data)}{custom_values_hash}"

    custom_values = custom_values or {}
    custom_values.update({"repo_name": repo_name})

    cookiecutter(
        str(template_dir),
        no_input=True,
        output_dir=str(output_dir),
        extra_context=custom_values,
        overwrite_if_exists=True,
    )

    assert (
        output_dir / repo_name
    ).exists(), f"Project directory was not created for {template_dir}"

import hashlib
import json
import subprocess
from pathlib import Path

from cookiecutter.main import cookiecutter
from jinja2 import Template

from . import TEST_OUTPUT_DIR


def get_generated_templates() -> list[Path]:
    return [template_dir for template_dir in TEST_OUTPUT_DIR.glob("*/*") if template_dir.is_dir()]


def assert_linting_generated_template(generated_template_dir: Path):
    pre_commit_config = generated_template_dir / ".pre-commit-config.yaml"
    if pre_commit_config.exists():
        with subprocess.Popen(["bash"], stdin=subprocess.PIPE, cwd=generated_template_dir) as proc:
            proc.stdin.write(b"rm -rf .git/\n")
            proc.stdin.write(b"git init -b main\n")
            proc.stdin.write(b"pre-commit install --config .pre-commit-config.yaml\n")
            proc.stdin.write(b"git add .\n")
            proc.stdin.write(b"pre-commit run --all-files\n")
            proc.stdin.close()
            proc.wait()
            assert proc.returncode == 0, f"Linting failed for {generated_template_dir}"


def generate_cookiecutter_template(template_dir: Path | str, custom_values: dict = None):
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

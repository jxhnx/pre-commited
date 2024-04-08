import pytest

from .common import assert_linting_generated_template, get_generated_templates


@pytest.mark.order(-1)
@pytest.mark.default
def test_linting_generated_templates():
    for template in get_generated_templates():
        assert_linting_generated_template(template)

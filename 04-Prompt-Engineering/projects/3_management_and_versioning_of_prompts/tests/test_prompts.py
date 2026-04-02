"""
Static validation tests for all system prompts.
Validates structure, syntax and rendering without using LLM.
"""

import yaml
import pytest
import re
import string
from pathlib import Path
from typing import Dict, List, Any, Tuple


@pytest.fixture(scope="session")
def prompts_dir() -> Path:
    """Return the prompts directory."""
    return Path(__file__).parent.parent / "prompts"


@pytest.fixture(scope="session")
def registry_data(prompts_dir: Path) -> Dict[str, Any]:
    """Load and return registry.yaml data."""
    registry_path = prompts_dir / "registry.yaml"
    with open(registry_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_yaml_file(filepath: Path) -> Dict[str, Any]:
    """Load and return the contents of a YAML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def test_registry_yaml_syntax(registry_data: Dict[str, Any]):
    """Test if registry.yaml has valid syntax."""
    assert registry_data is not None, "Registry.yaml is empty"
    assert 'agents' in registry_data, "Registry must contain 'agents' key"


def test_all_yaml_files_valid(prompts_dir: Path):
    """Test if all YAML files in prompts folder are valid."""
    yaml_files = prompts_dir.glob("**/*.yaml")

    errors = []
    for yaml_file in yaml_files:
        try:
            load_yaml_file(yaml_file)
        except yaml.YAMLError as e:
            relative_path = yaml_file.relative_to(prompts_dir)
            errors.append(f"{relative_path}: {e}")

    if errors:
        error_msg = "YAML files with syntax errors:\n" + "\n".join(errors)
        pytest.fail(error_msg)


def test_registry_files_exist(prompts_dir: Path, registry_data: Dict[str, Any]):
    """Test if all prompts in registry physically exist."""
    missing_files = []
    for agent_id, agent_data in registry_data.get('agents', {}).items():
        prompt_path = prompts_dir / agent_data['path']
        if not prompt_path.exists():
            missing_files.append(f"{agent_id}: {agent_data['path']}")

    if missing_files:
        error_msg = "Missing prompt files:\n" + "\n".join(missing_files)
        pytest.fail(error_msg)


@pytest.fixture(scope="session")
def all_prompts(prompts_dir: Path, registry_data: Dict[str, Any]) -> List[Tuple[str, Path]]:
    """Return list of all prompt paths from registry."""
    prompts = []
    for agent_id, agent_data in registry_data.get('agents', {}).items():
        prompt_path = prompts_dir / agent_data['path']
        if prompt_path.exists():
            prompts.append((agent_id, prompt_path))
    return prompts


def test_prompt_structure(all_prompts):
    """Test the structure of each prompt.yaml."""
    for prompt_id, prompt_path in all_prompts:
        prompt_data = load_yaml_file(prompt_path)

        required_fields = ['id', 'version', 'template', 'input_variables']
        missing_fields = [field for field in required_fields if field not in prompt_data]

        if missing_fields:
            pytest.fail(f"Prompt {prompt_id} missing fields: {missing_fields}")

        assert isinstance(prompt_data['input_variables'], list), \
            f"Prompt {prompt_id}: input_variables must be a list"
        assert isinstance(prompt_data['template'], str), \
            f"Prompt {prompt_id}: template must be a string"
        assert prompt_data['template'].strip(), \
            f"Prompt {prompt_id}: template cannot be empty"


def test_template_variables_consistency(all_prompts):
    """Test if template variables match input_variables."""
    for prompt_id, prompt_path in all_prompts:
        prompt_data = load_yaml_file(prompt_path)

        template = prompt_data['template']
        declared_vars = set(prompt_data['input_variables'])
        template_vars = set(re.findall(r'\{(\w+)\}', template))

        undeclared = template_vars - declared_vars
        if undeclared:
            pytest.fail(f"Prompt {prompt_id} uses undeclared variables: {undeclared}")

        unused = declared_vars - template_vars
        if unused:
            print(f"\nWarning: Prompt {prompt_id} has unused variables: {unused}")


def test_fstring_syntax(all_prompts):
    """Test if template has valid f-string format syntax."""
    for prompt_id, prompt_path in all_prompts:
        prompt_data = load_yaml_file(prompt_path)
        template_str = prompt_data['template']

        try:
            formatter = string.Formatter()
            list(formatter.parse(template_str))
        except ValueError as e:
            pytest.fail(f"Prompt {prompt_id} has f-string format syntax error: {e}")


@pytest.fixture(scope="session")
def prompts_with_tests(prompts_dir: Path, registry_data: Dict[str, Any]) -> List[Tuple[str, Path, Path]]:
    """Return prompts that have test files."""
    prompts_with_tests = []
    for agent_id, agent_data in registry_data.get('agents', {}).items():
        prompt_path = prompts_dir / agent_data['path']
        test_path = prompt_path.parent / "prompt.tests.yaml"

        if prompt_path.exists() and test_path.exists():
            prompts_with_tests.append((agent_id, prompt_path, test_path))

    return prompts_with_tests


@pytest.fixture(scope="session")
def all_test_cases(prompts_with_tests: List[Tuple[str, Path, Path]]) -> List[Tuple[str, Dict[str, Any], Dict[str, Any]]]:
    """Return all test cases from all prompts."""
    test_cases = []
    for prompt_id, prompt_path, test_path in prompts_with_tests:
        prompt_data = load_yaml_file(prompt_path)
        test_data = load_yaml_file(test_path)

        for case in test_data.get('cases', []):
            case_id = f"{prompt_id}::{case['name']}"
            test_cases.append((case_id, prompt_data, case))

    return test_cases


def test_test_cases_structure(prompts_with_tests):
    """Test the structure of prompt.tests.yaml files."""
    for prompt_id, prompt_path, test_path in prompts_with_tests:
        test_data = load_yaml_file(test_path)

        assert 'cases' in test_data, f"Tests for {prompt_id} must have 'cases' key"
        assert isinstance(test_data['cases'], list), f"'cases' must be a list in {prompt_id}"

        for i, case in enumerate(test_data['cases']):
            case_name = case.get('name', f'case_{i}')
            required = ['name', 'inputs', 'expect_contains']
            missing = [field for field in required if field not in case]

            if missing:
                pytest.fail(f"Prompt {prompt_id}, case '{case_name}' is missing: {missing}")

            assert isinstance(case['inputs'], dict), \
                f"Prompt {prompt_id}, case '{case_name}': inputs must be a dict"
            assert isinstance(case['expect_contains'], list), \
                f"Prompt {prompt_id}, case '{case_name}': expect_contains must be a list"


def test_prompt_rendering_with_test_cases(all_test_cases):
    """Test if prompt renders correctly with test cases."""
    for case_id, prompt_data, test_case in all_test_cases:
        required_vars = set(prompt_data['input_variables'])
        provided_vars = set(test_case['inputs'].keys())

        invalid_vars = provided_vars - required_vars
        if invalid_vars:
            print(f"\nWarning: Case {case_id} provides unused variables: {invalid_vars}")

        render_vars = {var: test_case['inputs'].get(var, '') for var in required_vars}

        try:
            rendered = prompt_data['template'].format(**render_vars)
        except Exception as e:
            pytest.fail(f"Error rendering {case_id}: {e}")

        missing_texts = [text for text in test_case['expect_contains'] if text not in rendered]
        if missing_texts:
            pytest.fail(
                f"Case {case_id} doesn't contain expected texts:\n"
                f"Missing: {missing_texts}\n"
                f"First 500 characters of output:\n{rendered[:500]}..."
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
import yaml
from pathlib import Path
from typing import NamedTuple, Optional


class PromptInfo(NamedTuple):
    id: str
    version: str
    path: Path
    description: str
    model: Optional[str] = None


class PromptRegistry:
    def __init__(self, prompts_dir: str = "prompts", registry_filename: str = "registry.yaml"):
        self.prompts_dir = Path(__file__).parent.parent / prompts_dir
        self.registry_path = self.prompts_dir / registry_filename
        self._load_registry()

    def _load_registry(self) -> None:
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self.registry_path}")

        with open(self.registry_path, 'r', encoding='utf-8') as f:
            self.registry = yaml.safe_load(f)

        if 'agents' not in self.registry:
            raise ValueError("Registry must contain 'agents' key")

    def get_prompt(self, prompt_id: str) -> PromptInfo:
        agents = self.registry.get('agents', {})

        if prompt_id not in agents:
            available = list(agents.keys())
            raise ValueError(f"Prompt '{prompt_id}' not found. Available: {available}")

        agent_config = agents[prompt_id]

        required_fields = ['current_version', 'path', 'description']
        missing_fields = [field for field in required_fields if field not in agent_config]
        if missing_fields:
            raise ValueError(f"Missing required fields for prompt '{prompt_id}': {missing_fields}")

        prompt_path = self.prompts_dir / agent_config['path']

        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file does not exist: {prompt_path}")

        return PromptInfo(
            id=prompt_id,
            version=agent_config['current_version'],
            path=prompt_path,
            description=agent_config['description'],
            model=agent_config.get('model')
        )


registry = PromptRegistry()
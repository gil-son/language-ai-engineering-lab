import json
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ========= Configuration =========

@dataclass
class EnrichmentConfig:
    """Configuration for query enrichment"""
    model_name: str = "ollama:llama3.2"
    temperature: float = 0.0
    max_rounds: int = 10

    # Define what information we want to collect
    required_information: List[Dict[str, str]] = None

    def __post_init__(self):
        """Set default required_information if not provided."""
        if self.required_information is None:
            # Default configuration for PR review scenario
            self.required_information = [
                {"field": "pr_id", "question": "What is the PR ID?"},
                {"field": "repository", "question": "What is the repository name?"},
                {"field": "branch", "question": "What is the branch name?"},
                {"field": "concerns", "question": "What are your specific concerns?"},
                {"field": "style_guide", "question": "What style guide should be followed?"},
                {"field": "test_requirements", "question": "What are the test requirements?"},
            ]


# ========= Models =========

class EnrichedQuery(BaseModel):
    """Structure for enriched query output"""
    is_complex: bool = Field(description="Whether the query is complex")
    sub_queries: List[str] = Field(description="Breakdown into specific tasks")
    clarifications: List[str] = Field(description="Questions needing clarification")
    entities: List[str] = Field(description="Extracted entities")


# ========= Query Enricher =========

class QueryEnricher:
    """Handles query enrichment logic"""

    def __init__(self, config: EnrichmentConfig):
        self.config = config
        self.llm = init_chat_model(config.model_name, temperature=config.temperature)
        self.enrichment_chain = self._create_enrichment_chain()
        self.rewrite_chain = self._create_rewrite_chain()

    def _create_enrichment_chain(self):
        """Create the query enrichment chain"""

        # Build the list of required questions dynamically from config
        questions_text = "\n".join([
            f'  * "{info["question"]}"'
            for info in self.config.required_information
        ])

        enrichment_prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are a query refinement assistant for software development questions.

Your task is to identify missing information and generate clarifying questions.

CRITICAL: You MUST ask for ALL 6 required pieces of information. Do NOT stop early.

Required information (ALL must be explicitly provided):
1. PR ID
2. Repository name
3. Branch name
4. Specific concerns
5. Style guide
6. Test requirements

Output STRICT JSON with this structure:
{{{{
  "is_complex": bool,
  "sub_queries": [string],
  "clarifications": [string],
  "entities": [string]
}}}}

Rules:
- clarifications: MUST include questions for ANY of these that are NOT explicitly mentioned in the query:
{questions_text}
  IMPORTANT: Keep the clarifications list populated until ALL 6 items above are provided.
  Even if you have PR ID, repository, and branch, you MUST still ask for concerns, style guide, and test requirements.
- sub_queries: Break down the request into specific tasks
- entities: Extract ONLY the information that was actually provided
- is_complex: true if multiple sub-tasks are needed

NEVER set clarifications to empty [] unless ALL 6 required items are explicitly present in the query."""),
            ("user", "{question}")
        ])

        def _parse_json(raw: str) -> Dict[str, Any]:
            """Extract and parse JSON from LLM output, stripping markdown fences."""
            text = raw.strip()
            # Strip markdown code fences if present
            for fence in ["```json", "```JSON", "```Json", "```"]:
                while text.startswith(fence):
                    text = text[len(fence):].strip()
                text = text.strip()
                if text.endswith("```"):
                    text = text[:-3].strip()
            if not text:
                print(f"[DEBUG] Empty JSON output from LLM")
                return {
                    "is_complex": True,
                    "sub_queries": ["Review the PR"],
                    "clarifications": [
                        "What is the PR ID?",
                        "What is the repository name?",
                        "What is the branch name?",
                        "What are your specific concerns?",
                        "What style guide should be followed?",
                        "What are the test requirements?",
                    ],
                    "entities": [],
                }
            # If JSON is wrapped in more fences, try to find first { and last }
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                text = text[start:end+1]
            try:
                return json.loads(text)
            except json.JSONDecodeError as e:
                print(f"[DEBUG] JSON parse error: {e}")
                print(f"[DEBUG] Raw output:\n{raw[:500]}")
                # Last resort: return fallback with all clarifications
                return {
                    "is_complex": True,
                    "sub_queries": ["Review the PR"],
                    "clarifications": [
                        "What is the PR ID?",
                        "What is the repository name?",
                        "What is the branch name?",
                        "What are your specific concerns?",
                        "What style guide should be followed?",
                        "What are the test requirements?",
                    ],
                    "entities": [],
                }

        # Use StrOutputParser for raw text, then parse manually for robustness with llama3.2
        return enrichment_prompt | self.llm | StrOutputParser() | _parse_json

    def _create_rewrite_chain(self):
        """Create chain to rewrite query in natural language"""
        rewrite_prompt = ChatPromptTemplate.from_messages([
            ("system", "Rewrite the information into a single, natural, well-formed question. Be concise and clear."),
            ("user", "Original request: {original}\n\nAdditional context:\n{context}")
        ])

        return rewrite_prompt | self.llm | StrOutputParser()

    def enrich(self, query: str) -> Dict[str, Any]:
        """Enrich a query with clarifications"""
        try:
            return self.enrichment_chain.invoke({"question": query})
        except Exception as e:
            print(f"Error during enrichment: {e}")
            return {
                "is_complex": False,
                "sub_queries": [],
                "clarifications": ["Error processing query"],
                "entities": []
            }

    def generate_natural_question(self, original: str, context: List[str]) -> str:
        """Generate natural language version of enriched query"""
        if not context:
            return original

        context_text = "\n".join([f"- {info}" for info in context])

        try:
            return self.rewrite_chain.invoke({
                "original": original,
                "context": context_text
            })
        except Exception as e:
            print(f"Error generating natural question: {e}")
            # Fallback: return concatenated version
            return f"{original} | " + " | ".join(context)


# ========= Interactive Session =========

class EnrichmentSession:
    """Manages interactive enrichment session"""

    def __init__(self, enricher: QueryEnricher):
        self.enricher = enricher
        self.initial_question = ""
        self.provided_information = []
        self.round_num = 0

    def _display_enrichment(self, enriched: Dict[str, Any]):
        """Display enrichment results"""
        print(f"\n=== Round {self.round_num}: Enrichment Output ===")
        print(json.dumps(enriched, indent=2, ensure_ascii=False))

    def _collect_answers(self, clarifications: List[str]) -> List[str]:
        """Collect answers from user for clarifications"""
        print("\nPlease provide answers for the following clarifications:")
        print("(Press Enter to skip any question)")

        answers = []
        for clarification in clarifications:
            answer = input(f"  {clarification}: ").strip()
            if answer:
                answers.append(f"{clarification}: {answer}")

        return answers

    def _show_progress(self, new_answers: List[str]):
        """Show progress of enrichment"""
        if new_answers:
            print(f"\n>>> Information provided in this round:")
            for answer in new_answers:
                print(f"    - {answer}")

    def run(self, initial_question: str) -> tuple[str, Dict[str, Any]]:
        """Run interactive enrichment session"""
        self.initial_question = initial_question
        self.provided_information = []
        self.round_num = 0

        print(f"\nInitial question: '{initial_question}'")
        print("="*60)

        # Build the current query
        current_query = initial_question
        enriched = self.enricher.enrich(current_query)

        while self.round_num < self.enricher.config.max_rounds:
            self.round_num += 1
            self._display_enrichment(enriched)

            # Check if we have clarifications
            clarifications = enriched.get("clarifications", [])
            if not clarifications:
                print("\n>>> All required information has been provided!")
                break

            # Collect answers
            new_answers = self._collect_answers(clarifications)

            if new_answers:
                # Update information and query
                self.provided_information.extend(new_answers)
                current_query = self.initial_question + " | " + " | ".join(self.provided_information)

                self._show_progress(new_answers)

                # Re-enrich with updated information
                enriched = self.enricher.enrich(current_query)
            else:
                # No new information provided
                print("\n>>> No additional information provided in this round.")
                user_continue = input("Continue with remaining clarifications? (yes/no): ").strip().lower()
                if user_continue not in ['yes', 'y']:
                    print(">>> Stopping enrichment with partial information.")
                    break

        # Show final results
        print("\n=== Final Enriched Query (JSON) ===")
        print(json.dumps(enriched, indent=2, ensure_ascii=False))

        # Generate natural language version
        natural_question = self.enricher.generate_natural_question(
            self.initial_question,
            self.provided_information
        )

        print("\n=== Final Enriched Question ===")
        print(natural_question)

        return natural_question, enriched


# ========= Application =========

class QueryEnrichmentApp:
    """Main application class"""

    def __init__(self, config: Optional[EnrichmentConfig] = None):
        self.config = config or EnrichmentConfig()
        self.enricher = QueryEnricher(self.config)
        self.session = EnrichmentSession(self.enricher)

    def run_interactive(self):
        """Run interactive query enrichment"""
        print("Query Enrichment Technique")
        print("This technique transforms vague queries into detailed, specific questions")
        print("#"*60)

        try:
            print("\n" + "="*60)
            print("Interactive Query Enrichment")
            print("="*60)

            question = input("\nEnter your question (e.g., 'Review my PR'): ").strip()

            if question:
                final_question, enriched = self.session.run(question)
                return final_question, enriched
            else:
                print("No question provided.")
                return None, None

        except (EOFError, KeyboardInterrupt):
            print("\n\nProgram interrupted.")
            return None, None


# ========= Main Execution =========

if __name__ == "__main__":
    app = QueryEnrichmentApp()
    app.run_interactive()
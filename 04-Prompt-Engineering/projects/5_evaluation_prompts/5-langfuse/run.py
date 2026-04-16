from datetime import datetime
from langfuse.langchain import CallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from shared.clients import get_langfuse_client
from langfuse_helpers import parse_judge_response, format_reasoning_summary

# Initialize clients
langfuse = get_langfuse_client()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Configuration
DATASET_NAME = "code-ds"
PROMPT_A_NAME = "prompt_doc_a"
PROMPT_B_NAME = "prompt_doc_b"
PROMPT_JUDGE_NAME = "llm_judge_pairwise"

timestamp = datetime.now().strftime("%H%M")


def langfuse_prompt_to_chain(prompt_obj):
    """Convert Langfuse prompt to LangChain chain."""
    # Check if it's a text prompt (string)
    if isinstance(prompt_obj.prompt, str):
        return ChatPromptTemplate.from_messages([("user", prompt_obj.prompt)]) | llm

    # Chat prompt - convert messages (extract role and content only)
    messages = [(msg["role"], msg["content"]) for msg in prompt_obj.prompt]
    return ChatPromptTemplate.from_messages(messages) | llm

if __name__ == "__main__":
    print("="*80)
    print("LANGFUSE PAIRWISE EVALUATION")
    print("="*80)

    # 1. Load prompts from Langfuse
    print("\n1. Loading prompts from Langfuse...")
    prompt_a = langfuse.get_prompt(PROMPT_A_NAME, label="production")
    prompt_b = langfuse.get_prompt(PROMPT_B_NAME, label="production")
    prompt_judge = langfuse.get_prompt(PROMPT_JUDGE_NAME, label="evaluation")
    print(f"   Loaded: {PROMPT_A_NAME}")
    print(f"   Loaded: {PROMPT_B_NAME}")
    print(f"   Loaded: {PROMPT_JUDGE_NAME}")

    # 2. Convert to LangChain chains
    print("\n2. Creating LangChain chains...")
    chain_a = langfuse_prompt_to_chain(prompt_a)
    chain_b = langfuse_prompt_to_chain(prompt_b)
    chain_judge = langfuse_prompt_to_chain(prompt_judge)
    print("   Chains created")

    # 3. Load dataset
    print(f"\n3. Loading dataset '{DATASET_NAME}'...")
    dataset = langfuse.get_dataset(DATASET_NAME)
    items_list = list(dataset.items)
    print(f"   Dataset loaded with {len(items_list)} items")

    # 4. Run experiments
    print(f"\n4. Running pairwise evaluation (timestamp: {timestamp})...")
    print("-"*80)

    for idx, item in enumerate(items_list, 1):
        print(f"\nItem {idx}/{len(items_list)}")
        print(f"   Input: {str(item.input)[:100]}...")

        # Run Prompt A
        print("   Running Prompt A...")
        experiment_a_name = f"ExperimentA_{timestamp}"
        handler_a = CallbackHandler()
        response_a = chain_a.invoke(
            item.input,
            config={
                "callbacks": [handler_a],
                "run_name": experiment_a_name,
                "tags": ["experiment", "prompt_a"],
                "metadata": {"experiment": "DocPromptA", "prompt": "A", "timestamp": timestamp}
            }
        )
        output_a = response_a.content
        trace_id_a = handler_a.last_trace_id
        print(f"      Generated {len(output_a)} chars")

        # Run Prompt B
        print("   Running Prompt B...")
        experiment_b_name = f"ExperimentB_{timestamp}"
        handler_b = CallbackHandler()
        response_b = chain_b.invoke(
            item.input,
            config={
                "callbacks": [handler_b],
                "run_name": experiment_b_name,
                "tags": ["experiment", "prompt_b"],
                "metadata": {"experiment": "DocPromptB", "prompt": "B", "timestamp": timestamp}
            }
        )
        output_b = response_b.content
        trace_id_b = handler_b.last_trace_id
        print(f"      Generated {len(output_b)} chars")

        # Run Pairwise Judge
        print("   Running Pairwise Judge...")
        handler_judge = CallbackHandler()
        judge_inputs = {
            "code": str(item.input.get("files", "")),
            "reference": str(item.expected_output.get("reference", "")),
            "answer_a": output_a,
            "answer_b": output_b
        }
        response_judge = chain_judge.invoke(
            judge_inputs,
            config={
                "callbacks": [handler_judge],
                "run_name": f"PairwiseJudge_{timestamp}",
                "tags": ["evaluation", "judge"],
                "metadata": {"experiment": "PairwiseJudge", "type": "evaluation", "timestamp": timestamp}
            }
        )
        judge_response = response_judge.content
        trace_id_judge = handler_judge.last_trace_id

        # Parse judge decision
        decision, reasoning = parse_judge_response(judge_response)

        # Extract scores from reasoning
        score_a = reasoning.get("score_total_a", "?")
        score_b = reasoning.get("score_total_b", "?")

        # Determine winner text for display
        winner_text = experiment_a_name if decision == "A" else (experiment_b_name if decision == "B" else "TIE")

        # Score the judge run itself
        if trace_id_judge:
            langfuse.create_score(
                trace_id=trace_id_judge,
                name="Winner",
                value=winner_text,
                data_type="CATEGORICAL",
                comment=f"Scores: A={score_a}/50, B={score_b}/50\n\n{format_reasoning_summary(reasoning)}"
            )

        print(f"      Decision: {decision} (A: {score_a}/50, B: {score_b}/50)")

        # Add scores to the original runs
        print("   Adding comparison scores...")

        # Score for Prompt A
        result_a = "Won" if decision == "A" else ("Tie" if decision == "TIE" else "Lost")
        if trace_id_a:
            langfuse.create_score(
                trace_id=trace_id_a,
                name="Pairwise Result",
                value=result_a,
                data_type="CATEGORICAL",
                comment=f"{result_a} against {experiment_b_name}\n\n{format_reasoning_summary(reasoning)}"
            )

        # Score for Prompt B
        result_b = "Won" if decision == "B" else ("Tie" if decision == "TIE" else "Lost")
        if trace_id_b:
            langfuse.create_score(
                trace_id=trace_id_b,
                name="Pairwise Result",
                value=result_b,
                data_type="CATEGORICAL",
                comment=f"{result_b} against {experiment_a_name}\n\n{format_reasoning_summary(reasoning)}"
            )

        print(f"      Scores added")

    print("\n" + "="*80)
    print("EVALUATION COMPLETED!")
    print("="*80)
    print(f"\nView results in Langfuse UI:")
    print(f"  Filter by timestamp: {timestamp}")

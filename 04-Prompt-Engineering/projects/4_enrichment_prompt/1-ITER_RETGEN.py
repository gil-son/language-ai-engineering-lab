from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = init_chat_model("ollama:llama3.2", temperature=0.7)

# ========= Enhanced Prompt Templates =========

# Prompt to generate initial draft with MANY specific gaps
draft_prompt = PromptTemplate(
    input_variables=["question"],
    template=(
        "You are an expert assistant with limited initial knowledge.\n"
        "Answer the following question, but you MUST mark MANY specific details as missing.\n"
        "Use [MISSING: ...] markers for:\n"
        "- Specific version numbers and release dates\n"
        "- Technical specifications and parameters\n"
        "- Performance metrics and benchmarks\n"
        "- Comparison data between different versions\n"
        "- Implementation details and code examples\n"
        "- Real-world use cases and case studies\n"
        "- Limitations and known issues\n"
        "- Future roadmap and upcoming features\n\n"
        "Be thorough in identifying what specific information would make the answer complete.\n"
        "Start with a basic overview but mark MANY specific details as missing.\n\n"
        "Do not generate more than 5 MISSING Markers."
        "Question: {question}\n\n"
        "Answer:"
    ),
)

# Prompt to generate queries from gaps - now more specific
query_prompt = PromptTemplate(
    input_variables=["draft"],
    template=(
        "You received the following draft with gaps:\n{draft}\n\n"
        "For each [MISSING: ...] marker, provide information to fill that gap.\n"
        "Format each as: 'For [MISSING: topic]: provide the actual information'\n"
        "Be specific and provide real data when possible.\n"
        "Example: 'For [MISSING: version numbers]: LangChain is at version 0.1.0, LangGraph at 0.2.0'\n"
        "List information for each gap, maximum 5 items."
    ),
)

# Prompt to fill gaps gradually based on complexity
fill_prompt = PromptTemplate(
    input_variables=["question", "draft", "queries", "iteration"],
    template=(
        "Original question: {question}\n\n"
        "Current draft (iteration {iteration}):\n{draft}\n\n"
        "Information to help fill the gaps:\n{queries}\n\n"
        "CRITICAL INSTRUCTIONS:\n"
        "1. You MUST replace AT LEAST 1-2 [MISSING: ...] markers with concrete information\n"
        "2. ACTUALLY REPLACE the text '[MISSING: xyz]' with real content - don't keep the marker\n"
        "3. Use the information above to guide what content to add\n"
        "4. Do NOT add any new [MISSING:] markers - only fill or keep existing ones\n"
        "5. If you cannot fill a gap with certainty, keep it as [MISSING: ...]\n\n"
        "Example of what to do:\n"
        "- WRONG: '[MISSING: version numbers and release dates]' (keeping the marker)\n"
        "- RIGHT: 'LangChain version 0.1.0 was released in January 2024' (replacing with content)\n\n"
        "Important: This is iteration {iteration}. You MUST make progress by filling gaps.\n\n"
        "Rewrite the ENTIRE answer with the [MISSING:] markers replaced:"
    ),
)

# New prompt to identify additional gaps after filling
expansion_prompt = PromptTemplate(
    input_variables=["draft"],
    template=(
        "Review this draft answer:\n{draft}\n\n"
        "Identify areas that could benefit from MORE specific information.\n"
        "Add new [MISSING: ...] markers for:\n"
        "- Technical details that were glossed over\n"
        "- Specific examples that would clarify concepts\n"
        "- Comparative data that would add context\n"
        "- Implementation specifics that developers would need\n\n"
        "Return the same text but with ADDITIONAL [MISSING: ...] markers for deeper details:"
    ),
)

# ========= Create Runnable Chains =========

draft_chain = draft_prompt | llm | StrOutputParser()
query_chain = query_prompt | llm | StrOutputParser()
fill_chain = fill_prompt | llm | StrOutputParser()
expansion_chain = expansion_prompt | llm | StrOutputParser()

# ========= Enhanced Main Function =========

def iter_retgen_multi(question: str, max_iters: int = 10, target_completeness: float = 0.95):
    """
    Perform iterative retrieval and generation with multiple natural rounds.
    Continues until all gaps are filled or max iterations reached.

    Args:
        question: The question to answer
        max_iters: Maximum number of iterations to refine the answer
        target_completeness: Target completeness (0-1), stops when achieved

    Returns:
        The final refined answer
    """

    # Generate initial draft with many gaps
    draft = draft_chain.invoke({"question": question})
    print("\n=== Initial Draft (with many gaps) ===")
    print(draft)

    # Count initial gaps
    initial_gaps = draft.count("[MISSING:")
    print(f"\n Initial gaps identified: {initial_gaps}")

    actual_iterations = 0
    consecutive_no_progress = 0

    # Iterative refinement - continue until complete or max iterations
    for iteration in range(max_iters):
        actual_iterations = iteration + 1
        current_gaps = draft.count("[MISSING:")

        # Check if we've reached completion
        if current_gaps == 0:
            print("\n All gaps filled!")

            # Only expand in early iterations, not indefinitely
            if iteration < 2:  # Only expand in first couple iterations
                print("Checking for areas to expand...")
                draft = expansion_chain.invoke({"draft": draft})
                current_gaps = draft.count("[MISSING:")

                if current_gaps == 0:
                    print(" Answer is comprehensive and complete!")
                    break
                else:
                    print(f" Identified {current_gaps} new areas for expansion")
                    consecutive_no_progress = 0  # Reset counter
            else:
                print("✅ Answer is complete after multiple refinements!")
                break  # Stop after filling all gaps in later iterations

        print(f"\n{'='*60}")
        print(f" ITERATION {iteration + 1}")
        print(f" Current gaps to address: {current_gaps}")
        print('='*60)

        # Generate queries for missing information
        queries = query_chain.invoke({"draft": draft})
        print("\n=== Generated Queries ===")
        queries_list = queries.split('\n')
        for i, query in enumerate(queries_list[:10], 1):  # Show max 10 queries
            if query.strip():
                print(f"{i}. {query.strip()}")
        if len(queries_list) > 10:
            print(f"   ... and {len(queries_list) - 10} more queries")

        # Fill gaps with new information (gradual filling based on iteration)
        draft = fill_chain.invoke({
            "question": question,
            "draft": draft,
            "queries": queries,
            "iteration": iteration + 1
        })

        # Show refined answer
        print("\n=== Refined Answer ===")
        print(draft[:500] + "..." if len(draft) > 500 else draft)  # Show preview

        # Report progress
        new_gaps = draft.count("[MISSING:")
        filled = current_gaps - new_gaps
        print(f"\nProgress: Filled {filled} gaps, {new_gaps} remaining")

        # Check if we're making progress
        if filled == 0:
            consecutive_no_progress += 1
            if consecutive_no_progress >= 3:
                print("\nNo progress in 3 consecutive iterations. Stopping.")
                break
        else:
            consecutive_no_progress = 0

    print(f"\n{'='*60}")
    print(f" REFINEMENT COMPLETE after {actual_iterations} iterations")
    print(f"{'='*60}")

    return draft


# ========= Main Execution =========

if __name__ == "__main__":
    # Using a complex technical question that naturally requires multiple iterations
    demonstration_question = (
        "Explain about the LangChain and LangGraph"
    )

    print(f"'{demonstration_question}'")
    print("#"*60)

    # Run with more iterations to ensure completion
    final_answer = iter_retgen_multi(demonstration_question, max_iters=10)

    print("\n" + "="*60)
    print("FINAL COMPLETE ANSWER:")
    print("="*60)
    print(final_answer)

    # Final statistics
    final_gaps = final_answer.count("[MISSING:")
    initial_length = len(demonstration_question)
    final_length = len(final_answer)

    print("\n" + "="*60)
    print(f"FINAL STATISTICS:")
    print(f"   - Remaining gaps: {final_gaps}")
    print(f"   - Answer expansion: {final_length / initial_length:.1f}x original question length")
    print("="*60)
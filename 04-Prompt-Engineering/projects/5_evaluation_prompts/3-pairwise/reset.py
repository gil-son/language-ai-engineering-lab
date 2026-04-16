from langsmith import Client
from dotenv import load_dotenv

load_dotenv()

DATASET_NAME = "pairwise_initial_comparison"
PROMPT_A_ID = "pairwise_comparison_security"
PROMPT_B_ID = "pairwise_comparison_performance"

def reset():
    client = Client()

    # Deletar dataset
    try:
        client.delete_dataset(dataset_name=DATASET_NAME)
        print(f" Dataset deletado: {DATASET_NAME}")
    except Exception as e:
        print(f"  Dataset não encontrado: {DATASET_NAME}")

    # Deletar prompts
    try:
        client.delete_prompt(PROMPT_A_ID)
        print(f" Prompt deletado: {PROMPT_A_ID}")
    except Exception as e:
        print(f"  Prompt não encontrado: {PROMPT_A_ID}")

    try:
        client.delete_prompt(PROMPT_B_ID)
        print(f" Prompt deletado: {PROMPT_B_ID}")
    except Exception as e:
        print(f"  Prompt não encontrado: {PROMPT_B_ID}")

if __name__ == "__main__":
    print("  Limpando recursos do Experimento 1...")
    reset()

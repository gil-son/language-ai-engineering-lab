from dotenv import load_dotenv
load_dotenv()

from langsmith import Client

DATASET_NAME = "evaluation_basic_dataset"
client = Client()

try:
    dataset = client.read_dataset(dataset_name=DATASET_NAME)
    client.delete_dataset(dataset_id=dataset.id)
    print(f"Dataset deleted: {DATASET_NAME}")
except Exception as e:
    print(f"Dataset not found or already deleted: {DATASET_NAME}")

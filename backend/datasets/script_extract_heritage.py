import os
import json
import ast
from datasets import load_dataset
from tqdm import tqdm

def load_and_process_osm_data(dataset_name="ns2agi/antwerp-osm-navigator"):
    print(f"Loading dataset: {dataset_name}")
    dataset = load_dataset(dataset_name)
    train_split = dataset["train"]
    node_dataset = train_split.filter(lambda example:
                                      example["type"] == "node")
    return node_dataset

def extract_heritage_data(dataset, output_dir="data/heritage_dataset"):
    print("\nFiltering records with heritage tag '4'...")
    heritage_records = []

    total_records = len(dataset)

    for record in tqdm(dataset, total=total_records, desc="Filtering", unit="record"):
        try:
            tags = ast.literal_eval(record['tags'])

            # Check for heritage tag with value '4'
            if tags.get('heritage') == '4':
                heritage_records.append(record)

        except Exception as e:
            print(f"Error processing record {record['id']}: {e}")

    # Save results for heritage records
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, "heritage_entries.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(heritage_records, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(heritage_records)} heritage records with 'heritage' = '4' to {file_path}")

if __name__ == "__main__":
    dataset = load_and_process_osm_data()

    output_dir = "../maps_dataset"

    # Run the extraction process for heritage tag '4'
    extract_heritage_data(dataset, output_dir)

    print("\nScript finished.")

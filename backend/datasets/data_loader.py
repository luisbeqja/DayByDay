import os
import json
import ast
from datasets import load_dataset
from tqdm import tqdm
from collections import defaultdict


def load_and_process_osm_data(dataset_name="ns2agi/antwerp-osm-navigator"):
    print(f"Loading dataset: {dataset_name}")
    dataset = load_dataset(dataset_name)
    train_split = dataset["train"]
    node_dataset = train_split.filter(lambda example:
                                      example["type"] == "node")
    return node_dataset


def extract_data(dataset, amenity_categories, shop_categories,
                 output_dir="data/maps_dataset"):
    print("\nFiltering categories for amenities and shops")
    filtered_amenities = defaultdict(list)
    filtered_shops = defaultdict(list)
    total_records = len(dataset)

    for record in tqdm(dataset, total=total_records, desc="Filtering",
                       unit="record"):
        try:
            tags = ast.literal_eval(record['tags'])

            # Check for amenities
            if 'amenity' in tags and tags['amenity'] in amenity_categories:
                filtered_amenities[tags['amenity']].append(record)

            # Check for shops
            if 'shop' in tags and tags['shop'] in shop_categories:
                filtered_shops[tags['shop']].append(record)

        except Exception as e:
            print(f"Error processing record {record['id']}: {e}")

    # Save results for amenities and shops
    os.makedirs(output_dir, exist_ok=True)

    # Save amenities data
    for category, records in filtered_amenities.items():
        file_path = os.path.join(output_dir, f"{category}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(records)} entries for amenity '{category}' "
              f"to {file_path}")

    # Save shops data
    for category, records in filtered_shops.items():
        file_path = os.path.join(output_dir, f"{category}.json")
        if os.path.exists(file_path):
            print(f"Skipping existing file: {file_path}")
            continue
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(records)} entries for shop '{category}' "
              f"to {file_path}")


if __name__ == "__main__":
    dataset = load_and_process_osm_data()

    # These categories were identified as student-relevant
    amenity_categories = {
        "bar", "biergarten", "cafe", "fast_food", "ice_cream", "pub",
        "restaurant", "wine_bar", "library", "coworking_space",
        "cinema", "arts_centre", "theatre", "events_venue"
    }

    shop_categories = {
        "bakery", "coffee", "chocolate", "tea", "supermarket",
        "clothes", "shoes", "books",
        "fashion_accessories", "gift"
    }

    output_dir = "data/maps_dataset"

    # Run the optimized extraction process
    extract_data(dataset, amenity_categories, shop_categories, output_dir)

    print("\nScript finished.")

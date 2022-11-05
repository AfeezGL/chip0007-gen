import csv
import json
import os
import sys
from hashlib import sha256
from pathlib import Path


def start(input_csv_path):

    try:
        with open(os.path.relpath(input_csv_path), "r", encoding="utf-8") as input_csv:
            csvreader = csv.DictReader(input_csv)
            with open("./output.csv", "w", encoding="utf-8") as output_csv:
                output_writer = csv.DictWriter(
                    output_csv, fieldnames=[*csvreader.fieldnames, "Hash"]
                )
                output_writer.writeheader()
                for row in csvreader:
                    data = {
                        "format": "CHIP-0007",
                        "name": row["Name"],
                        "description": row["Description"],
                        "minting_tool": "Team x",
                        "sensitive_content": False,
                        "series_number": row["Series Number"],
                        "series_total": 526,
                        "attributes": [
                            {
                                "trait_type": "gender",
                                "value": row["Gender"],
                            }
                        ],
                        "collection": {
                            "name": "Zuri NFT Tickets for Free Lunch",
                            "id": row["UUID"],
                            "attributes": [
                                {
                                    "type": "description",
                                    "value": "Rewards for accomplishments during HNGi9.",
                                }
                            ],
                        },
                    }

                    Path("./outputs").mkdir(parents=True, exist_ok=True)
                    json_path = f"./outputs/{row['Name']}.json"
                    with open(json_path, "w", encoding="utf-8") as json_output:
                        json_output.write(json.dumps(data))

                    json_file_hash = sha256(open(json_path, "rb").read()).hexdigest()
                    row.setdefault("Hash", json_file_hash)
                    output_writer.writerow(row)
    except FileNotFoundError:
        print("File not found.")


if __name__ == "__main__":
    start(sys.argv[1])

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
            # Create an output csv file with the input csv header and new header 'Hash'
            with open("./output.csv", "w", encoding="utf-8") as output_csv:
                output_writer = csv.DictWriter(
                    output_csv, fieldnames=[*csvreader.fieldnames, "Hash"]
                )
                output_writer.writeheader()
                for row in csvreader:
                    # turn attributes into an list
                    attributes = row["Attributes"].split(";")
                    normalized_attributes = []
                    for attribute in attributes:
                        if len(attribute.split(":")) == 2:
                            attribute_dict = {
                                "trait_type": attribute.split(":")[0].strip(),
                                "value": attribute.split(":")[1].strip(),
                            }
                            normalized_attributes.append(attribute_dict)
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
                            },
                            *normalized_attributes,
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

                    # Create outputs directory if it doesn't exist.
                    # Outputs directory stores our json files.
                    Path("./outputs").mkdir(parents=True, exist_ok=True)
                    json_path = f"./outputs/{row['Name']}.json"
                    with open(json_path, "w", encoding="utf-8") as json_output:
                        json_output.write(json.dumps(data))

                    json_file_hash = sha256(open(json_path, "rb").read()).hexdigest()
                    # Add hash field to row and save row to the output csv
                    row.setdefault("Hash", json_file_hash)
                    output_writer.writerow(row)
        print("Success, check output.csv file in the current directory for results.")
    except FileNotFoundError:
        print("Wrong csv file provided, please check the file path provided again.")


if __name__ == "__main__":
    start(sys.argv[1])

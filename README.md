# Description

This script takes in a csv file with rows of nft metadata then generates a CHIP-007 JSON for each row, creates sha256 hash of the json and adds the hash to the row.

## Usage instruction

Run `python chip.py /absolute/path/to/csv/file` in the script directory.
Example `python chip.py /home/afeez/Downloads/nft.csv`
Output will be found in the current directory as output.csv.

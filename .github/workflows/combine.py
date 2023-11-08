import json
import sys

def merge_json(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    merged_data = {**data1, **data2}

    with open(file1, 'w') as outfile:
        json.dump(merged_data, outfile, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        # print("Usage: python merge_json.py <main_file.json> <branch_file.json>") 
        sys.exit('wrong number of arguments')

    merge_json(sys.argv[1],sys.argv[2])


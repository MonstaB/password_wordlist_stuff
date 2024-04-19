import argparse
from tqdm import tqdm
import os
import multiprocessing


def remove_duplicates(file1_list, file2):
    # Set up a set to store lines from all file1
    lines_to_keep = set()

    # Process each file1
    for file1 in file1_list:
        process_file1(file1, lines_to_keep)

    # Process file2 after processing all file1
    process_file2(file2, lines_to_keep)

def process_file1(file1, lines_to_keep):
    # Read file1 line by line
    try:
        with open(file1, 'r', encoding='latin-1') as f1:
            for line in tqdm(f1, desc=f"Processing {file1}", unit=" lines"):
                lines_to_keep.add(line.strip())
    except UnicodeDecodeError:
        print(f"Failed to read {file1} with utf-8 encoding. Trying latin-1 encoding...")
        with open(file1, 'r', encoding='utf-8') as f1:
            for line in tqdm(f1, desc=f"Processing {file1}", unit=" lines"):
                lines_to_keep.add(line.strip())

def process_file2(file2, lines_to_keep):
    total_stripped = 0
    temp_file = "temp.txt"

    # Process file2
    try:
        with open(file2, 'r', encoding='utf-8') as f2, open(temp_file, 'w', encoding='utf-8') as temp:
            for line in tqdm(f2, desc="Processing file2", unit=" lines"):
                if line.strip() not in lines_to_keep:
                    temp.write(line)
                else:
                    total_stripped += 1
        # Replace file2 with the temp file
        os.replace(temp_file, file2)
    except UnicodeDecodeError:
        print(f"Failed to read {file2} with utf-8 encoding. Trying latin-1 encoding...")
        with open(file2, 'r', encoding='latin-1') as f2, open(temp_file, 'w', encoding='latin-1') as temp:
            for line in tqdm(f2, desc="Processing file2", unit=" lines"):
                if line.strip() not in lines_to_keep:
                    temp.write(line)
                else:
                    total_stripped += 1
        # Replace file2 with the temp file
        os.replace(temp_file, file2)

    # Print total stripped lines information
    print(f"\nTotal lines stripped from {file2}: {total_stripped}")

def main():
    parser = argparse.ArgumentParser(description='Remove lines from file2 that are present in file1.')
    parser.add_argument('file1', nargs='+', help='path to the first file(s)')
    parser.add_argument('file2', help='path to the second file')

    args = parser.parse_args()

    remove_duplicates(args.file1, args.file2)

if __name__ == "__main__":
    main()

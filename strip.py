import argparse
import os

from tqdm import tqdm


def remove_duplicates_from_chunk(chunk, lines_to_keep):
    processed_lines = []
    for line in chunk:
        if line.strip() not in lines_to_keep:
            processed_lines.append(line)
    return processed_lines


def process_chunk(chunk, lines_to_keep, temp_file, max_lines_per_file):
    processed_lines = remove_duplicates_from_chunk(chunk, lines_to_keep)
    with open(temp_file, 'a', encoding='utf-8') as temp:
        for line in tqdm(processed_lines, desc="Writing temp file", unit=" line"):
            temp.write(line)
    return len(processed_lines)




def process_file2(file2, lines_to_keep):
    temp_file_base = file2
    temp_file_suffix = ".temp"  # Define temp file suffix
    max_lines_per_file = 50000000
    total_stripped = 0
    file_index = 0
    lines_processed = 0

    print(f"Reading and processing {file2}...")
    try:
        with open(file2, 'r', encoding='utf-8') as f2:
            chunk = []
            for line in tqdm(f2, desc="Processing lines", unit=" line"):
                lines_processed += 1
                chunk.append(line)
                if len(chunk) >= max_lines_per_file:
                    temp_file = f"{temp_file_base}_{file_index}{temp_file_suffix}"
                    num_lines_stripped = process_chunk(chunk, lines_to_keep, temp_file, max_lines_per_file)
                    total_stripped += num_lines_stripped
                    chunk.clear()
                    file_index += 1
                    print(f"Temporary files created: {file_index}", end='\r')  # Update temp file counter

            # Process the remaining lines in the last chunk
            if chunk:
                temp_file = f"{temp_file_base}_{file_index}{temp_file_suffix}"
                num_lines_stripped = process_chunk(chunk, lines_to_keep, temp_file, max_lines_per_file)
                total_stripped += num_lines_stripped

        print(f"\nProcessed all lines from {file2}")
    except UnicodeDecodeError:
        print(f"Failed to read {file2} with utf-8 encoding. Trying latin-1 encoding...")
        with open(file2, 'r', encoding='latin-1') as f2:
            chunk = []
            for line in tqdm(f2, desc="Processing lines", unit=" line"):
                lines_processed += 1
                chunk.append(line)
                if len(chunk) >= max_lines_per_file:
                    temp_file = f"{temp_file_base}_{file_index}{temp_file_suffix}"
                    num_lines_stripped = process_chunk(chunk, lines_to_keep, temp_file, max_lines_per_file)
                    total_stripped += num_lines_stripped
                    chunk.clear()
                    file_index += 1
                    print(f"Temporary files created: {file_index}", end='\r')  # Update temp file counter

            # Process the remaining lines in the last chunk
            if chunk:
                temp_file = f"{temp_file_base}_{file_index}{temp_file_suffix}"
                num_lines_stripped = process_chunk(chunk, lines_to_keep, temp_file, max_lines_per_file)
                total_stripped += num_lines_stripped

        print(f"\nProcessed all lines from {file2}")

    # Combine temporary files
    combined_file_name = f"{file2}"
    combined_line_count = combine_temp_files(temp_file_base, file_index, combined_file_name, temp_file_suffix)

    # Print total stripped lines information
    print(f"\nTotal lines stripped from {file2}: {total_stripped}")

    # Print original and combined file line counts
    print(f"Original file line count: {lines_processed}")
    print(f"Combined file line count: {combined_line_count}")
    print(f"Lines removed: {lines_processed - combined_line_count}")


def combine_temp_files(temp_file_base, num_files, combined_file_name, temp_file_suffix):
    combined_line_count = 0
    with open(combined_file_name, 'w', encoding='utf-8') as combined_file:
        for i in tqdm(range(num_files + 1), desc="Combining files"):
            temp_file = f"{temp_file_base}_{i}{temp_file_suffix}"
            with open(temp_file, 'r', encoding='utf-8') as temp:
                for line in temp:
                    combined_file.write(line)
                    combined_line_count += 1
            os.remove(temp_file)
    print(f"Combined all temporary files into {combined_file_name}")
    return combined_line_count


def write_chunk_to_temp_file(chunk_lines, temp_dir, large_file, chunk_count):
    chunk_file_path = os.path.join(temp_dir, f"{os.path.basename(large_file)}_chunk{chunk_count}")
    with open(chunk_file_path, 'w', encoding='utf-8') as chunk_file:
        chunk_file.writelines(chunk_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Remove lines from a file (file2) that are present in other files (file1).')
    parser.add_argument('-f', '--file1', help='path to the first file')
    parser.add_argument('-c', '--combined', nargs='+', help='path to the first file(s) done combined')
    parser.add_argument('-s', '--sequential', nargs='+', help='process large files sequentially and in chunks')
    parser.add_argument('-o', '--file2', help='path to the second file')
    args = parser.parse_args()

    # Read all lines from file1 and combine them into a set
    if args.combined:
        lines_to_keep = set()
        for file1 in args.combined:
            try:
                print(f"Reading {file1}...")
                with open(file1, 'r', encoding='utf-8') as f1:
                    lines_to_keep.update(line.strip() for line in f1)
                print(f"Read {file1}")

            except UnicodeDecodeError:
                print(f"Failed to read {file1} with utf-8 encoding. Trying latin-1 encoding...")
                with open(file1, 'r', encoding='latin-1') as f1:
                    lines_to_keep.update(line.strip() for line in f1)
                print(f"Read {file1} with latin-1 encoding")
                # Process file2
        process_file2(args.file2, lines_to_keep)
    elif args.file1:
        lines_to_keep = set()
        try:
            print(f"Reading {args.file1}...")
            with open(args.file1, 'r', encoding='utf-8') as f1:
                lines_to_keep.update(line.strip() for line in f1)
            print(f"Read {args.file1}")

        except UnicodeDecodeError:
            print(f"Failed to read {args.file1} with utf-8 encoding. Trying latin-1 encoding...")
            with open(args.file1, 'r', encoding='latin-1') as f1:
                lines_to_keep.update(line.strip() for line in f1)
            print(f"Read {args.file1} with latin-1 encoding")
            # Process file2

        process_file2(args.file2, lines_to_keep)

    elif args.sequential:
        for large_file in args.sequential:
            temp_dir = "temp_chunks"
            os.makedirs(temp_dir, exist_ok=True)
            with open(large_file, 'r', encoding='utf-8') as f:
                chunk_count = 0
                chunk_lines = []
                for line in f:
                    chunk_lines.append(line)
                    if len(chunk_lines) >= 100000000:
                        write_chunk_to_temp_file(chunk_lines, temp_dir, large_file, chunk_count)
                        chunk_lines = []
                        chunk_count += 1
                if chunk_lines:
                    write_chunk_to_temp_file(chunk_lines, temp_dir, large_file, chunk_count)

            # Process each chunk file sequentially
            for chunk_file in sorted(os.listdir(temp_dir)):
                lines_to_keep = set()
                try:
                    print(f"Reading {chunk_file}...")
                    with open(os.path.join(temp_dir, chunk_file), 'r', encoding='utf-8') as f1:
                        lines_to_keep.update(line.strip() for line in f1)
                    print(f"Read {chunk_file}")
                except UnicodeDecodeError:
                    print(f"Failed to read {chunk_file} with utf-8 encoding. Trying latin-1 encoding...")
                    with open(os.path.join(temp_dir, chunk_file), 'r', encoding='latin-1') as f1:
                        lines_to_keep.update(line.strip() for line in f1)
                    print(f"Read {chunk_file} with latin-1 encoding")
                # Process file2
                process_file2(args.file2, lines_to_keep)


if __name__ == "__main__":
    main()

import argparse
from tqdm import tqdm


def convert_to_utf8(input_file, output_file):
    with open(input_file, 'rb') as infile:
        total_bytes = infile.seek(0, 2)  # Get total size of the input file
        infile.seek(0)  # Reset file pointer to the beginning
        with open(output_file, 'w', encoding='utf-8') as outfile:
            progress_bar = tqdm(total=total_bytes, unit='B', unit_scale=True, desc="Converting")
            for line in infile:
                decoded_line = line.decode('latin-1')  # Decode using 'latin-1'
                outfile.write(decoded_line)
                progress_bar.update(len(line))
            progress_bar.close()


def main():
    parser = argparse.ArgumentParser(description='Convert file to UTF-8 encoding.')
    parser.add_argument('input_file', help='path to the input file')
    parser.add_argument('output_file', help='path to the output file')

    args = parser.parse_args()

    convert_to_utf8(args.input_file, args.output_file)
    print("Conversion completed successfully.")


if __name__ == "__main__":
    main()

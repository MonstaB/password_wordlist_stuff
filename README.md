# File Line Removal Tool

This is a Python script that removes lines from a file (`file2`) that are present in other files (`file1` or combined files).

## Features

- Removes duplicate lines from `file2` based on the content of one or more other files.
- Supports processing large files sequentially and in chunks for efficient memory usage.
- Provides progress bars using tqdm library for better visualization of the process.


### Prerequisites

- Python 3.x
- tqdm library

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/MonstaB/file-line-removal-tool.git
    ```

2. Install dependencies:

    ```sh
    pip install tqdm
    ```

### Command-line Arguments

The script accepts the following command-line arguments:

- `-f, --file1`: Path to the first file.
- `-c, --combined`: Path to the first file(s) small files to be combined.
- `-s, --sequential`: Process large file(s) sequentially and in chunks.
- `-o, --file2`: Path to the second file (target file).

### Running the Script

To run the script, execute the following command in your terminal:

```bash
python script.py -f <file1_path> -o <file2_path>
```
Replace <file1_path> with the path to the first file or files, and <file2_path> with the path to the second file.

### Example Usages
Removing lines from file2 that are present in a single file file1:
```
python script.py -f file1.txt -o file2.txt
```
Removing lines from file2 that are present in multiple files (combined):
```
python script.py -c file1_1.txt file1_2.txt -o file2.txt
```
Processing large files sequentially and in chunks:
```
python script.py -s large_file.txt large_file_2.txt-o file2.txt
```
## Output
The script generates temporary files during processing, which are combined into the final output file (file2) after line removal. It also provides information about the number of lines stripped from file2 and the original and combined file line counts.

## Note
The script handles encoding issues gracefully, attempting both UTF-8 and Latin-1 encodings when reading files.
For large files, it processes them sequentially and in chunks to optimize memory usage.

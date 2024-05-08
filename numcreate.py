import argparse

def generate_numbers(num_amount, sequence):
    start = 0
    end = 10 ** num_amount

    for num in range(start, end):
        num_str = str(num).zfill(num_amount)
        valid = True
        for i, c in enumerate(sequence):
            if c.isdigit() and int(c) != int(num_str[i]):
                valid = False
                break
        if valid:
            yield num_str

def main():
    parser = argparse.ArgumentParser(description='Generate numbers based on provided sequence and length')
    parser.add_argument('-n', type=int, help='Number amount')
    parser.add_argument('-s', type=str, help='Sequence where a ? represents numbers between 0 and 9, and if a number is declared, that number shall only appear in that place')
    parser.add_argument('-o', type=str, help='Output file to write to')

    args = parser.parse_args()

    if not args.n or not args.s or not args.o:
        print("Please provide all arguments: -n, -s, -o")
        return

    numbers = generate_numbers(args.n, args.s)

    with open(args.o, 'w') as outfile:
        for num in numbers:
            outfile.write(num + '\n')

    print(f"Numbers generated successfully and written to {args.o}")

if __name__ == "__main__":
    main()

import argparse

def remove_lines(input_file, output_file, num_lines_to_remove):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        file.writelines(lines[num_lines_to_remove:])

def main():
    parser = argparse.ArgumentParser(description='Remove first N lines from a file.')
    parser.add_argument('-i', '--input', required=True, help='Input file name')
    parser.add_argument('-o', '--output', required=True, help='Output file name')
    parser.add_argument('-n', '--num-lines', type=int, default=1000, help='Number of lines to remove')

    args = parser.parse_args()

    remove_lines(args.input, args.output, args.num_lines)

if name == "main":
    main()

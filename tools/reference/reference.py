def process_input(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    formatted_lines = [f"\\cite{{{line.strip()}}}" for line in lines]

    output_text = ' '.join(formatted_lines)

    with open(output_file, 'w') as f:
        f.write(output_text)


if __name__ == "__main__":
    INPUT = "input/1"
    OUTPUT = "output/1"
    process_input(INPUT, OUTPUT)

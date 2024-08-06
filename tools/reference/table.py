def process_input(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    formatted_lines = [f"& {line.strip()} & & \\\\" for line in lines]
    formatted_lines = [line + "\n\cline{2-4}\n" if index < len(formatted_lines) - 1 else line + "\n" for index, line in enumerate(formatted_lines)]

    with open(output_file, 'w') as f:
        f.writelines(formatted_lines)


if __name__ == "__main__":
    INPUT = "input/1"
    OUTPUT = "output/1"
    process_input(INPUT, OUTPUT)

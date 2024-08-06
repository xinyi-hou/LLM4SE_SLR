def process_input(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    formatted_lines = []

    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            formatted_lines.append(f"{parts[0]} ({parts[1]})")
        else:
            formatted_lines.append(parts[0])

    # Joining the lines in groups of 2, and adding necessary formatting
    formatted_output = []
    for i in range(0, len(formatted_lines), 2):
        if i + 1 < len(formatted_lines):
            formatted_output.append(f"& {formatted_lines[i]} & {formatted_lines[i+1]} & \\\\\n")
        else:
            formatted_output.append(f"& {formatted_lines[i]} & & \\\\\n")

    # Adding the horizontal line
    if len(formatted_lines) > 1:
        formatted_output[-1] += "\\hline\n"

    with open(output_file, 'w') as f:
        f.writelines(formatted_output)


if __name__ == "__main__":
    INPUT = "input/1"
    OUTPUT = "output/1"
    process_input(INPUT, OUTPUT)

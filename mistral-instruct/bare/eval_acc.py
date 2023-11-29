import re

def extract_numbers_from_file(file_path):
    # Regex patterns to match numbers in the specified format
    addition_pattern = r'(\d+)\s*\+\s*(\d+)'
    a_number_pattern = r'a:\s*(\d+)'

    # Read the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Find and extract numbers for the addition
    addition_match = re.search(addition_pattern, content)
    if addition_match:
        num1, num2 = addition_match.groups()
    else:
        num1, num2 = None, None

    # Find and extract the number following 'a:'
    a_number_match = re.search(a_number_pattern, content)
    if a_number_match:
        a_number = a_number_match.group(1)
    else:
        a_number = None

    return num1, num2, a_number

# Example usage
#file_path = 'path_to_your_file.txt'
#numbers = extract_numbers_from_file(file_path)
#print("Extracted numbers:", numbers)

prompt_template = """answer the following:
{num1} + {num2}
a:"""

filename_template = "{num1}_digit/{num2}_digit/t_{idx:02}.txt"
f_out = open("acc_results.txt", "w")
for i in [1, 2, 3, 4, 5, 6, 8, 10, 12]:
    accuracies = []
    for j in range(1, 13):
        num_correct = 0
        num_trials = 100
        if (i == 1) and (j == 1):
            num_trials = 50
        for k in range(num_trials):
            filename = filename_template.format(num1=i, num2=j, idx=k)
            #print(i, j, k, filename)
            num1, num2, answer = extract_numbers_from_file(filename)
            is_correct = int(num1) + int(num2) == int(answer)
            print(num1, num2, answer, is_correct)
            if is_correct:
                num_correct += 1
        if (i == 1) and (j == 1):
            accuracies = [(float(x) / 50) * 100 for x in accuracies]
            num_correct = int((float(num_correct) / 50) * 100)
        accuracies.append(num_correct)
    str_acc = [str(int(x)) for x in accuracies]
    print(f"{i}: {' '.join(str_acc)}")
    f_out.write(f"{i}: {' '.join(str_acc)}\n\n")

f_out.close()
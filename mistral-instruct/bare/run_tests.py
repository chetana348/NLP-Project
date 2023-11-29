import subprocess
import random
import os
from typing import Tuple

def generate_random_n_digit_number(n):
    """
    Generates a random n-digit number.

    :param n: Number of digits in the number.
    :return: A random n-digit number.
    """
    # Ensure the first digit is not zero
    first_digit = random.randint(1, 9)

    # Generate the remaining n-1 digits, which can include zero
    remaining_digits = [random.randint(0, 9) for _ in range(n - 1)]

    # Combine the digits to form the number
    digits = [first_digit] + remaining_digits
    return int(''.join(map(str, digits)))

def get_random_pair(used_pairs: set, i: int, j: int) -> Tuple[int, int]:
    nums_used = True
    while nums_used:
        num1 = generate_random_n_digit_number(i)
        num2 = generate_random_n_digit_number(j)
        pair = (num1, num2)
        nums_used = pair in used_pairs
    used_pairs.add(pair)
    return pair

prompt_template = """answer the following:
{num1} + {num2}
a:"""

filename_template = "{num1}_digit/{num2}_digit/t_{idx:02}.txt"

for i in [1, 2, 3, 4, 5, 6, 8, 10, 12]:
    for j in range(1, i+1):
        used_pairs = set()
        num_trials = 100
        if (i == 1) and (j == 1):
            num_trials = 50
        for k in range(num_trials):
            num1, num2 = get_random_pair(used_pairs, i, j)
            filename = filename_template.format(num1=i, num2=j, idx=k)
            print(i, j, k, filename)
            directory = os.path.dirname(filename)
            if not os.path.exists(directory):
                os.makedirs(directory)
            prompt = prompt_template.format(num1=num1, num2=num2)
            modelpath = "/Users/jackwimbish/uab/nlp/project/mistral-instruct/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
            prg_path = "/Users/jackwimbish/uab/nlp/project/mistral-instruct/llama.cpp/build/bin/main"
            command = f"""{prg_path} --color --model "{modelpath}" -t 7 -b 24 -n -1 --temp 0 -ngl 1 -p $'{prompt}' > {filename}"""
            process = subprocess.run(command, shell=True, executable='/bin/zsh', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Get the output and error (if any)
            output = process.stdout.decode()
            error = process.stderr.decode()
            # Print output and error
            print("Output:", output)
            print("Error:", error)

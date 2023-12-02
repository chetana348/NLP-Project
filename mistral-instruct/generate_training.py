import subprocess
import random
import os
from typing import Tuple
import json

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

max_digit_length = 6
def get_digit_lengths():
    dl1 = random.randint(1, max_digit_length)
    dl2 = random.randint(1, max_digit_length)
    return (dl1, dl2)

def get_random_pair(used_pairs: set) -> Tuple[int, int]:
    nums_used = True
    while nums_used:
        dl1, dl2 = get_digit_lengths()
        num1 = generate_random_n_digit_number(dl1)
        num2 = generate_random_n_digit_number(dl2)
        pair = (num1, num2)
        nums_used = pair in used_pairs
    used_pairs.add(pair)
    return pair

#prompt_template = """answer the following:
#{num1} + {num2}
#a:"""

num_examples = 5000

examples = []
used_pairs = set()
for i in range(num_examples):
    num1, num2 = get_random_pair(used_pairs)
    js = {"num1": num1, "num2": num2, "result": num1 + num2}
    examples.append(js)

split_idx = int(num_examples * 0.8)
train_examples = examples[:split_idx]
val_examples = examples[split_idx:]

f_out = open("finetune_dataset.jsonl", "w")
for js in train_examples:
    f_out.write(json.dumps(js) + '\n')
f_out.close()

f_out = open("finetune_dataset_val.jsonl", "w")
for js in val_examples:
    f_out.write(json.dumps(js) + '\n')
f_out.close()

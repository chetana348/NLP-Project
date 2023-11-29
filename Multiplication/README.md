# Multiplication with GPT2

This project showcases the capability of training a versatile neural model to execute intricate arithmetic operations without specifically tailoring the model architecture for the task. Our model successfully achieves 100% accuracy in performing 5-digit by 5-digit decimal multiplication. To illustrate, we fine-tune the GPT-2 model using a substantial dataset of generated expressions that articulate the step-by-step procedure of multiplication. For instance, inputting `23456x34567` should yield the accurate result of `810803552`.

See the [Algorithm](#Algorithm) section for an explanation of the inner mechanics.

## Training

Install the required packages using `pip install -r requirements.txt`.

Customize `Train and Test.ipynb` based on your requirements and edit the following lines:

* Edit `devices=` to the number of GPUs on your machine.
* Edit `batch_size=` (16 is the default) to fit the memory size of your GPU.
* Adjust `accumulate_grad_batches=` (8 is the default) accordingly to control the effective batch size. It was observed that larger batch sizes train faster and more stable.
* Optional argument is `resume_from_checkpoint` to resume training from a previous checkpoint. PyTorch Lightning should automatically save checkpoints during training.
* Also adjust the hyperparameters in `main.py` as needed. 

Then run the training cell. It takes around 100 epochs (10000000 samples) to converge, at which point it should reach 100% accuracy.

## Testing

Edit the testing cell of `Train and Test.ipynb` to the path of your model or pre-trained model (best_model. kept).

Give it prompts in the format of `xxxxx*xxxxx;`. The first digit must not be zero. For example: `12345*54321;`.


## Algorithm


```
   39
x  96
-----
  234
 351
-----
 3744
```

Multiplications can be computed vertically. We first decompose the multiplier into digits, and multiply each digit by the multiplicand, then we shift these results by the position of the digit and sum them together. There are two things left to do:

* Single digit multiplication. In the above example we need to compute `39*6=234` and `39*9=351`. This is again done by decomposing the *multiplicand* into digits, mutiply each digit by the multiplier, and sum them together. The last unit of computation, single-digit by single-digit multiplication, can be done by looking up the [multiplication table](https://en.wikipedia.org/wiki/Multiplication_table).

* While the process of summing up the inputs may seem trivial, the GPT-3 model is known to struggle with multi-operation arithmetic (see "Single Digit Three Ops" performance in the original GPT-3 paper). We need to break it up, and compute the sum of  two numbers at a time. We compute the number from right to left, and compute the carry first and then the actual digit. To make the task even easier for the model, the model finds the appropriate digit first and then computes the carry digit and the ones digit, so it doesn't have to worry about where to find the digits to perform the operation. When the two numbers are of differing number of digits, the missing digits are supplied with zero. However, the operation does not stop when the digits of both numbers are used up, since the most significant digit can be carried, like `9999+101`. Instead, the operation stops when the two digits and the carry are all zero. The sequence for `9999+101` looks like: (spaces added for clarity, they don't exist in actual training samples)

  ```
  9999+101;9100 9010 9111 9010 0011 000=10100
  ```

The full sequence for `39*96` is:

```
39*96;39*6;9*6;=54;3*6;=18;5+18;58030112000=23;=234;39*9;9*9;=81;3*9;=27;8+27;87050213000=35;=351;23+351;310425070303000=374;=3744$
```



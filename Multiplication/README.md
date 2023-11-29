# GPT2 Multiplication

This project showcases the capability of training a versatile neural model to execute intricate arithmetic operations without specifically tailoring the model architecture for the task. Our model successfully achieves 100% accuracy in performing 5-digit by 5-digit decimal multiplication. To illustrate, we fine-tune the GPT-2 model using a substantial dataset of generated expressions that articulate the step-by-step procedure of multiplication. For instance, inputting 23456*34567 should yield the accurate result of 810803552.

See [Algorithm](#Algorithm) section for algorithm used for multiplication.

## Training

Install the required packages with `pip install -r requirements.txt`.

Customize `train.py` based on your requirements. However, considering the computational resources, the default values are shown below. 

* `gpus=1`
* `batch_size=16`.
* `accumulate_grad_batches=8` accordingly. It was observed that larger batch sizes train faster and more stable.
* You have the option to include the argument resume_from_checkpoint in the command, pointing to a checkpoint file, to continue training from a prior checkpoint. PyTorch Lightning is configured to automatically save checkpoints during 
training.
*  Additionally, you may consider modifying hyperparameters in the main.py file. Given the relatively straightforward nature of the task, a smaller model could be sufficient, leading to faster training times. Adjusting hyperparameters 
tailored to the simplicity of the task can optimize the training process.

Then run `python train.py`. It typically takes around 100 epochs (10000000 samples) until it converges, at which point it should reach 100% accuracy.

## Test
Edit the path to your trained model or the pre-trained model (best_model.ckpt) in test.py.

Run `python test.py` and give it prompts in the format of `xxxxx*xxxxx;`. Replace `x` with numbers (the first digit must not be zero). For example: `12345*54321`.


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

The multiplication process involves breaking down the task into two main components:

*Single Digit Multiplication: The multiplier is decomposed into digits, and each digit is multiplied by the corresponding digit in the multiplicand. This process is repeated for each digit, and the results are summed together. In cases where single-digit multiplication is required (e.g., 39 * 6 or 39 * 9), the multiplicand is also decomposed into digits, and the multiplication is performed, with the final result obtained by summing these individual products. The lookup of single-digit multiplication values is facilitated by referring to the multiplication table.

*Summation of Results: The model needs to compute the sum of two numbers at a time. This is achieved by processing the numbers from right to left, calculating the carry first and then determining the actual digit. The model simplifies the task by finding the appropriate digit first and subsequently computing both the carry and the ones digit. To further facilitate the model's understanding, missing digits are padded with zeros when the numbers have different numbers of digits. The summation operation continues until all digits and the carry are zero. For instance, in the case of 9999 + 101, the operation progresses until the point where all digits and the carry become zero.

The sequence for `9999+101` looks like: 

  ```
  9999+101;9100 9010 9111 9010 0011 000=10100
  ```

The full sequence for `39*96` is:

```
39*96;39*6;9*6;=54;3*6;=18;5+18;58030112000=23;=234;39*9;9*9;=81;3*9;=27;8+27;87050213000=35;=351;23+351;310425070303000=374;=3744$
```



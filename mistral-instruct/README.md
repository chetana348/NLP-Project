# Addition with Mistral Instruct

This folder contains the code to run addition trials and evaluate results for the Mistral Instruct base model, the base model using a structured one-shot prompt, and a fine-tuned model. All .ipynb files are meant to be run on a Jupyter notebook on a GPU-enabled node on Cheaha with a conda kernel. Commands to install the needed python libraries are included, so start with a new conda environment for best results.

## Base Model

The code to generate trial prompts, run them through Mistral Instruct, and evaluate the results for accuracy is all contained in `mistral_math_rawmodel.ipynb`. All prompts and responses are recorded in the folder results_raw, which will be created when the trials are run.

## Base Model with One-Shot Structured Prompts

The code to generate trial prompts, run them through Mistral Instruct, and evaluate the results for accuracy is all contained in `mistral_math_structprompt.ipynb`. All prompts and responses are recorded in the folder results_struct_prompt, which will be created when the trials are run. The text files prompt_6_1.txt through prompt_6_6.txt contain the one-shot prompt templates for operands having a 6 digit LHS and a 1-6 digit RHS.

## Fine-Tuned With Generated Data

The code to generate the training and validation datasets is in `generate_training.py`. `finetune_dataset.jsonl` and `finetune_dataset_val.jsonl` are the results of running `generate_training.py`, though you can run it again to generate fresh data if you wish. The code to fine-tune the model, run inference on the fine-tuned model, and evaluate the results for accuracy is in `math_finetune_cheaha.ipynb`. Checkpoint LoRA adapters will be saved in the folder `mistral-math-finetune`.

The code in here uses a batch size of 2, which could probably be safely increased, and runs for 500 epochs. The first time I ran this code I didn't see loss decreasing past the checkpoint at 325, but the second time both training and validation losses seemed t obe slowly decreasing even at checkpoint 500, so running for more training epochs may produce better results.


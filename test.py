#importing the os module
import os
from transformers import AutoTokenizer, pipeline, logging # type: ignore
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
import argparse

#to get the current working directory
directory = os.getcwd()

model_name = "TheBloke/WizardCoder-15B-1.0-GPTQ"

use_triton = False # NVIDIA Triton Inference Server

tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

model = AutoGPTQForCausalLM.from_quantized(model_name,
        use_safetensors=True,
        device="cpu", # "cuda:0",
        use_triton=use_triton,
        quantize_config=None)

# Prevent printing spurious transformers error when using pipeline with AutoGPTQ
logging.set_verbosity(logging.CRITICAL)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

prompt_template = "<|system|>\n<|end|>\n<|user|>\n{query}<|end|>\n<|assistant|>"
prompt = prompt_template.format(query="How do I sort a list in Python?")
# We use a special <|end|> token with ID 49155 to denote ends of a turn
outputs = pipe(prompt,
              max_new_tokens=256,
              do_sample=True,
              temperature=0.2,
              top_k=50,
              top_p=0.95,
              eos_token_id=49155
            )
# You can sort a list in Python by using the sort() method. Here's an example:\n\n```\nnumbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]\nnumbers.sort()\nprint(numbers)\n```\n\nThis will sort the list in place and print the sorted list.
print(outputs[0]['generated_text'])
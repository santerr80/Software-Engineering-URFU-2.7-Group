from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='gpt2')

set_seed(42)

generator("Hello, I'm a language model, ", max_lenght=40, num_return_sequences=5)


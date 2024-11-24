# WORKING

import os
import json
import torch
import threading
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


input_file = 'input.json'
output_file = 'output.json'  

# Read the input JSON file and add 'index' to each item to preserve order
with open(input_file, 'r', encoding='utf-8') as f:
    input_items = json.load(f)

for idx, item in enumerate(input_items):
    item['index'] = idx

# Initialize the tokenizer (shared among threads)
tokenizer_en2vi = AutoTokenizer.from_pretrained("vinai/vinai-translate-en2vi-v2", src_lang="en_XX")

# Create batches that do not exceed 1024 tokens
def create_batches(input_items, max_tokens=1024):
    batches = []
    current_batch = []
    current_tokens = 0

    for item in input_items:
        question = item['question']
        answer = item['answer']
        # Count tokens for question and answer
        question_tokens = len(tokenizer_en2vi.encode(question, add_special_tokens=False))
        answer_tokens = len(tokenizer_en2vi.encode(answer, add_special_tokens=False))
        item_tokens = question_tokens + answer_tokens

        if current_tokens + item_tokens <= max_tokens:
            current_batch.append(item)
            current_tokens += item_tokens
        else:
            batches.append(current_batch)
            current_batch = [item]
            current_tokens = item_tokens

    if current_batch:
        batches.append(current_batch)

    return batches

# Create batches
batches = create_batches(input_items)

# Distribute batches to 3 threads (round-robin assignment)
batch_lists = [[], [], []]
for idx, batch in enumerate(batches):
    batch_lists[idx % 3].append(batch)

# Function to process batches
def process_batches(batch_list, device, thread_id, output_list):
    print(f"Thread {thread_id} starting on device {device}")
    # Initialize the model in the thread
    model_en2vi = AutoModelForSeq2SeqLM.from_pretrained("vinai/vinai-translate-en2vi-v2")
    model_en2vi.to(device)

    # Define the translation function within the thread
    def translate_en2vi(en_texts: list) -> list:
        input_ids = tokenizer_en2vi(
            en_texts, padding=True, truncation=True, return_tensors="pt"
        ).to(device)
        output_ids = model_en2vi.generate(
            **input_ids,
            decoder_start_token_id=tokenizer_en2vi.lang_code_to_id["vi_VN"],
            num_return_sequences=1,
            num_beams=5,
            early_stopping=True
        )
        vi_texts = tokenizer_en2vi.batch_decode(output_ids, skip_special_tokens=True)
        return vi_texts

    for batch in batch_list:
        batch_questions = [item['question'] for item in batch]
        batch_answers = [item['answer'] for item in batch]

        # Translate questions and answers
        translated_questions = translate_en2vi(batch_questions)
        translated_answers = translate_en2vi(batch_answers)

        # Update items with translations
        for i, item in enumerate(batch):
            item['question'] = translated_questions[i]
            item['answer'] = translated_answers[i]
            # Append the translated item to the thread's output list
            output_list.append(item)

    print(f"Thread {thread_id} finished")

# Create a list to collect outputs from all threads
threads_output = []

# Create a lock for appending to the shared output list
output_lock = threading.Lock()

# Start threads
threads = []
if torch.cuda.is_available():
    num_gpus = torch.cuda.device_count()
    available_devices = [f'cuda:{i}' for i in range(min(3, num_gpus))]
    # If less than 3 GPUs, duplicate devices
    while len(available_devices) < 3:
        available_devices.append(available_devices[-1])
else:
    available_devices = ['cpu'] * 3

for i in range(3):
    device = available_devices[i]
    batch_list = batch_lists[i]
    # Each thread will have its own output list
    thread_output = []
    t = threading.Thread(target=process_batches, args=(batch_list, device, i, thread_output))
    threads.append((t, thread_output))
    t.start()

# Wait for all threads to finish and collect their outputs
all_outputs = []
for t, thread_output in threads:
    t.join()
    # Append thread outputs to the all_outputs list
    all_outputs.extend(thread_output)

print("All threads have finished processing.")

# Sort all_outputs based on 'index' to preserve the original order
all_outputs.sort(key=lambda x: x['index'])

# Remove 'index' field before writing to output file
for item in all_outputs:
    del item['index']

# Write the outputs to the JSON file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_outputs, f, ensure_ascii=False, indent=2)

print("Translation completed and saved to", output_file)



# TOKEN COUNTER
# from transformers import AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained("vinai/vinai-translate-en2vi-v2", src_lang="en_XX")

# import json

# # Load the input items
# with open('input.json', 'r', encoding='utf-8') as f:
#     input_items = json.load(f)

# total_tokens = 0
# for item in input_items:
#     question = item['question']
#     answer = item['answer']
#     question_tokens = len(tokenizer.encode(question, add_special_tokens=False))
#     answer_tokens = len(tokenizer.encode(answer, add_special_tokens=False))
#     item_tokens = question_tokens + answer_tokens
#     total_tokens += item_tokens

# print("Total tokens in input file:", total_tokens)

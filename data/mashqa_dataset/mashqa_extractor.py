import json
import uuid

# Load the original JSON file - name to be changed for different file
with open('val_webmd_squad_v2_nonconsec.json', 'r') as f:
    data = json.load(f)

# List to hold the extracted information
extracted_data = []

# Loop through the data and extract the question, answer, and context
for article in data['data']:
    for paragraph in article['paragraphs']:
        context = paragraph['context']  # Extract context
        for qa in paragraph['qas']:
            question = qa['question']  # Extract question
            for answer in qa['answers']:
                extracted_item = {
                    'id': str(uuid.uuid4()),  # Generate unique identifier
                    'question': question,
                    'answer': answer['text'],  # Extract the answer text
                    'context': context
                }
                extracted_data.append(extracted_item)

# Save the extracted data to a new JSON file - name changed accordingly
with open('extracted_val_webmd_squad_v2_nonconsec.json', 'w') as f:
    json.dump(extracted_data, f, indent=4)

print("Extraction complete. Saved to 'extracted_val_webmd_squad_v2_nonconsec.json'.")

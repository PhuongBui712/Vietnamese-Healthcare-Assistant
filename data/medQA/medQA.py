import json
import uuid

def transform_data(input_file, output_file):
    transformed_data = {}

    # Read the JSONL file line by line
    with open(input_file, 'r') as f:
        for line in f:
            item = json.loads(line.strip())
            
            # Generate a unique key
            unique_key = str(uuid.uuid4())
            
            # Transform the structure
            transformed_data[unique_key] = {
                "Question": item["question"],
                "Contexts": [],  # Leave empty as per requirement
                "Answers": [item["answer"]]
            }

    # Write the transformed data to an output JSON file
    with open(output_file, 'w') as f:
        json.dump(transformed_data, f, indent=4)

# Specify the input and output file paths
input_file = 'train.jsonl'  # Replace with your JSONL file path
output_file = 'medQA.json'

# Call the function to transform data
transform_data(input_file, output_file)

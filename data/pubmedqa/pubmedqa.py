import json
import uuid

def extract_and_save_information(input_file, output_file):
    # Open and load the JSON file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Dictionary to hold the extracted data with UUIDs as keys
    extracted_data = {}
    
    # Iterate through each item in the JSON file
    for item_id, item_content in data.items():
        # Extract the relevant fields
        question = item_content.get("QUESTION", "N/A")
        contexts = item_content.get("CONTEXTS", [])
        long_answer = item_content.get("LONG_ANSWER", "N/A")

        # Generate a unique UUID for each entry
        unique_id = str(uuid.uuid4())
        
        # Add the extracted information to the new dictionary
        extracted_data[unique_id] = {
            "Question": question,
            "Contexts": contexts,
            "Answer": long_answer
        }
    
    # Save the extracted data into a new JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(extracted_data, file, indent=4, ensure_ascii=False)
    
    print(f"Data has been successfully extracted and saved to {output_file}")

# Path to your input JSON file
input_file = 'ori_pqal.json'

# Path to the output JSON file
output_file = 'pubmedqa.json'

# Run the extraction and save process
extract_and_save_information(input_file, output_file)
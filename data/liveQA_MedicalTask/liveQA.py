import json
import xml.etree.ElementTree as ET
import uuid

def extract_information_from_xml(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    extracted_data = {}

    for question in root.findall('NLM-QUESTION'):
        question_text = question.find('MESSAGE').text
        sub_questions = question.findall('.//SUB-QUESTION')
        
        for sub_question in sub_questions:
            # Generate a unique UUID for each entry
            unique_id = str(uuid.uuid4())
            
            # Extract annotations as context
            annotations = sub_question.find('.//ANNOTATIONS')
            context = {
                "Focus": annotations.find('FOCUS').text,
                "Type": annotations.find('TYPE').text
            }
            
            # Extract answers
            answers = [answer.text for answer in sub_question.findall('.//ANSWER')]
            
            # Structure the data
            extracted_data[unique_id] = {
                "Question": question_text,
                "Contexts": [context],
                "Answers": answers
            }

    return extracted_data

def save_to_json(data, output_file):
    # Save the extracted data to a JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Path to the input XML file
xml_file = 'TREC-2017-LiveQA-Medical-Train-2.xml'

# Path to the output JSON file
output_file = 'liveQA_data_2.json'

# Extract data and save to JSON
extracted_data = extract_information_from_xml(xml_file)
save_to_json(extracted_data, output_file)

print(f"Data has been successfully extracted and saved to {output_file}")

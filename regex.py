import json

def parse_analysis_response(response_text):
    parsed_data = {}
    # Split the response into lines
    lines = response_text.split('\n')

    # Initialize variables to keep track of the current key and value
    current_key = None
    current_value = ""

    for line in lines:
        # Check if the line starts with a number indicating a new section
        if line[:2].isdigit() and line[2] == '.':
            # If there's an existing key, save the current content to parsed_data
            if current_key is not None:
                parsed_data[current_key] = current_value.strip()

            # Reset the current key and value for the new section
            current_key = line.split(':', 1)[0].split('.', 1)[1].strip()
            current_value = line.split(':', 1)[1].strip() if ':' in line else ''
        else:
            # Continue accumulating the value for the current key
            current_value += (' ' + line.strip())

    # Save the last key-value pair
    if current_key is not None:
        parsed_data[current_key] = current_value.strip()

    return json.dumps(parsed_data, indent=4)

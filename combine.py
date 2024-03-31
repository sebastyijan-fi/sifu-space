import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def combine_data(answers_file, questions_file="q.json"):
    logging.info(f"Combining data from {answers_file} and {questions_file}")

    # Load answers from the provided JSON file
    logging.info(f"Loading answers from {answers_file}")
    with open(answers_file, "r") as file:
        answers = json.load(file)

    # Load questions from the static q.json file
    logging.info(f"Loading questions from {questions_file}")
    with open(questions_file, "r") as file:
        questions = json.load(file)

    # Initialize a dictionary to store the combined data
    combined_data = {}

    # Combine answers with corresponding questions
    logging.info("Combining answers with questions")
    for key, value in answers.items():
        combined_data[value] = questions.get(key, [])

    logging.info("Data combination completed successfully")

    # Save the combined data to a JSON file
    with open('combined_data.json', 'w') as outfile:
        json.dump(combined_data, outfile, indent=4)
        logging.info("Combined data saved to combined_data.json")

    return combined_data

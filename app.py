import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import uuid
import logging
from dotenv import load_dotenv
import os
from combine import combine_data
from logic import process_combined_data

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# List of questions
questions = [
    "Basic Business Idea: Describe the business concept.",
    "Key Objectives: List the objectives.",
    "Core Product or Service: Define the product or service.",
    "Target Audience: Identify the target audience.",
    "Key Value Proposition: State the value proposition.",
    "Major Revenue Streams: Describe potential revenue streams.",
    "Primary Costs: Detail the primary costs.",
    "Notable Features or Benefits: Outline notable features or benefits.",
    "Key Challenges or Problems Addressed: List key challenges or problems.",
    "Basic Competitive Advantage: Explain the competitive advantage."
]

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if not request.json or 'imageUrl' not in request.json:
            app.logger.error("No image URL provided in the request")
            return 'No image URL provided', 400

        image_url = request.json['imageUrl']

        parsed_responses = {}
        for question in questions:
            image_message = {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "This image depicts a user-uploaded sketch outlining an initial business idea, incorporating both textual descriptions and visual elements. Your task is to deliver a succinct analysis, providing only the response without any additional information or context. ONLY RESPOND WITH THE ANSWER NOTHING ELSE, must reply! Max 50 words " + question
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    },
                ]
            }

            analysis_response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[image_message],
            )

            response_text = analysis_response.choices[0].message.content.strip()
            parsed_responses[question] = response_text
            app.logger.info(f"Extracted response for question: {question}")

        call_id = str(uuid.uuid4())
        json_file_path = f"{call_id}.json"
        app.logger.info(f"Writing parsed responses to {json_file_path}")
        with open(json_file_path, "w") as json_file:
            json.dump(parsed_responses, json_file, indent=4)
        app.logger.info(f"Successfully wrote parsed responses to {json_file_path}")

        app.logger.info("Combining data")
        combined_data = combine_data(json_file_path)
        app.logger.info("Data combined successfully")

        app.logger.info("Processing combined data")
        process_combined_data(combined_data)
        app.logger.info("Combined data processed successfully")

        return 'Combined data processed successfully', 200

    except Exception as e:
        error_msg = f"Error processing image: {e}"
        app.logger.error(error_msg)
        app.logger.error(f"Type of problematic data: {type(e).__name__}")
        app.logger.error(f"Value: {e.args}")
        return jsonify(error=error_msg), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)

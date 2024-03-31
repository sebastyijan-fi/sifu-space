from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import base64
import uuid
import json
import os
import logging
from dotenv import load_dotenv
from regex import parse_analysis_response

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image file provided', 400

    image_file = request.files['image']
    image_data = base64.b64encode(image_file.read()).decode('utf-8')
    data_url = f"data:image/jpeg;base64,{image_data}"

    try:
        image_message = {
            "role": "user",
            "content": [
{
    "type": "text",
    "text": "This image is a user-uploaded sketch representing an initial business idea, combining both text and drawings. Please provide a concise analysis directly following each numbered item, without additional elaboration or context. Format your response with each point's number followed by the answer: 1. Basic Business Idea: Describe the business concept. 2. Key Objectives: List the objectives. 3. Core Product or Service: Define the product or service. 4. Target Audience: Identify the target audience. 5. Key Value Proposition: State the value proposition. 6. Major Revenue Streams: Describe potential revenue streams. 7. Primary Costs: Detail the primary costs. 8. Notable Features or Benefits: Outline notable features or benefits. 9. Key Challenges or Problems Addressed: List key challenges or problems. 10. Basic Competitive Advantage: Explain the competitive advantage."
}
,
                {"type": "image_url", "image_url": {"url": data_url}},
            ]
        }

        analysis_response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[image_message],
        )

        # Log the complete response to the terminal
        logging.info(f"OpenAI API Response: {analysis_response.choices[0].message}")

        # Ensure the response is correctly accessed
        response_content = analysis_response.choices[0].message.content  # Access content directly, without ['content']
        response_text = response_content if response_content else ""

        # Generate a unique ID for the call and parse the response
        call_id = str(uuid.uuid4())
        parsed_response = parse_analysis_response(response_text)
        
        # Save the parsed response to a JSON file
        with open(f"{call_id}.json", "w") as json_file:
            json_file.write(parsed_response)

        # Return the call ID and the parsed response
        return jsonify({"call_id": call_id, "data": json.loads(parsed_response)}), 200

    except Exception as e:
        app.logger.error(f"Error uploading image: {str(e)}")
        return 'Internal Server Error', 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

import base64
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.ERROR)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image file provided', 400

    image_file = request.files['image']
    image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct a data URL for the image
    data_url = f"data:image/jpeg;base64,{image_data}"

    try:
        image_message = {
            "role": "user",
            "content": [
                {
  "type": "text",
  "text": "This image is a user-uploaded sketch representing an initial business idea, combining both text and drawings. Analyze the visual content and extract key elements in a structured, factual manner suitable for further analysis. Avoid speculation and provide concise, clear points for each element: 1. Basic Business Idea: Describe the business concept. 2. Key Objectives: List the objectives. 3. Core Product or Service: Define the product or service. 4. Target Audience: Identify the target audience. 5. Key Value Proposition: State the value proposition. 6. Major Revenue Streams: Describe potential revenue streams. 7. Primary Costs: Detail the primary costs. 8. Notable Features or Benefits: Outline notable features or benefits. 9. Key Challenges or Problems Addressed: List key challenges or problems. 10. Basic Competitive Advantage: Explain the competitive advantage."
}
,
                {"type": "image_url", "image_url": {"url": data_url}},
            ]
        }

        # Upload the image data to the OpenAI API for analysis
        analysis_response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[image_message],
        )

        # Process the analysis response from OpenAI
        return jsonify(analysis_response.choices[0].message.content), 200

    except Exception as e:
        app.logger.error(f"Error uploading image: {str(e)}")
        return 'Internal Server Error', 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

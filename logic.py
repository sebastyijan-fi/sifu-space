import anthropic
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_opus = os.getenv("CLAUDE-KEY")
client = anthropic.Anthropic(api_key=api_opus)

def process_combined_data(combined_data):
    results = {}

    for business_concept, sub_questions in combined_data.items():
        results[business_concept] = {}
        for sub_question in sub_questions:
            prompt = (
                f"You have been tasked with providing detailed responses to the following questions:\n\n"
                f"Task: Provide extensive responses to the questions related to the given business concept and objectives.\n\n"
                f"Business Concept: {business_concept}\n\n"
                f"Objective: {sub_question}\n\n"
                f"Please ensure your response is insightful, analytical, and offers valuable recommendations. Make sure to answer in MD format."
            )

            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0.0,
                system=(
                    "As an AI assistant, your role is to provide comprehensive and insightful responses to the given questions. "
                    "Analyze carefully, and offer in-depth analysis, insights, and recommendations. "
                    "Use a professional and engaging writing style to deliver your responses and reply only with the answer. Make sure to answer in MD format."
                ),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extracting text from ContentBlock
            if isinstance(message.content, list):
                # Assuming message.content is a list of ContentBlock objects
                content_text = " ".join([content_block.text for content_block in message.content if hasattr(content_block, 'text')])
            else:
                # Defaulting to empty string if the content is not as expected
                content_text = ""

            results[business_concept][sub_question] = content_text

            with open('processed_data.json', 'w') as f:
                json.dump(results, f, indent=4)

            print(content_text)
            time.sleep(2)
